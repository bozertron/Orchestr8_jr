use super::delivery::DeliveryTracker;
use super::errors::RoutingError;
use super::operations::DeliveryOperations;
use super::retry::{RetryConfig, RetryManager};
use super::transport::TransportManager;
use super::DeliveryStatus;
use crate::p2p::message::persistence::PersistenceService;
use crate::p2p::message::types::{EncryptedMessage, MessageId};
use crate::p2p::{MessageConfig, MessageEvent};
use libp2p::PeerId;
use std::sync::Arc;
use std::time::Duration;
use tokio::sync::{mpsc, RwLock};
use uuid::Uuid;
/// Message routing service for encrypted P2P message delivery
pub struct RoutingService {
    config: MessageConfig,
    transport_manager: Arc<RwLock<TransportManager>>,
    delivery_tracker: Arc<RwLock<DeliveryTracker>>,
    retry_manager: RetryManager,
    event_sender: mpsc::UnboundedSender<MessageEvent>,
    persistence: PersistenceService,
}
impl RoutingService {
    /// Create new routing service
    pub async fn new(
        config: &MessageConfig,
        event_sender: mpsc::UnboundedSender<MessageEvent>,
    ) -> Result<Self, String> {
        let delivery_timeout = Duration::from_secs(30); // 30 second delivery timeout
        let delivery_tracker = DeliveryTracker::new(event_sender.clone(), delivery_timeout);
        let delivery_tracker = Arc::new(RwLock::new(delivery_tracker));
        // Start background timeout watcher (every 5 seconds)
        DeliveryTracker::start_timeout_watcher(delivery_tracker.clone(), Duration::from_secs(5));

        let retry_config = RetryConfig::default();
        let retry_manager = RetryManager::new(retry_config);

        // Initialize persistence service
        let persistence = PersistenceService::new(config, event_sender.clone())
            .await
            .map_err(|e| format!("Persistence init failed: {}", e))?;

        Ok(Self {
            config: config.clone(),
            transport_manager: Arc::new(RwLock::new(TransportManager::new())),
            delivery_tracker,
            retry_manager,
            event_sender,
            persistence,
        })
    }
    /// Route encrypted message to peer with delivery confirmation
    pub async fn route_message(
        &self,
        to: PeerId,
        encrypted_message: EncryptedMessage,
    ) -> Result<MessageId, String> {
        let message_id = Uuid::new_v4();
        let transport = self
            .prepare_transport(to, message_id, &encrypted_message)
            .await?;
        self.execute_and_persist(to, message_id, encrypted_message, transport)
            .await?;
        Ok(message_id)
    }

    async fn prepare_transport(
        &self,
        to: PeerId,
        message_id: MessageId,
        encrypted_message: &EncryptedMessage,
    ) -> Result<crate::p2p::message::TransportMethod, String> {
        DeliveryOperations::validate_message_size(encrypted_message, self.config.max_message_size)?;
        DeliveryOperations::select_and_prepare_transport(
            &self.transport_manager,
            &self.delivery_tracker,
            to,
            message_id,
        )
        .await
        .map_err(|e| {
            RoutingError::TransportError(format!("select transport failed: {}", e)).to_string()
        })
    }
    async fn execute_and_persist(
        &self,
        to: PeerId,
        message_id: MessageId,
        encrypted_message: EncryptedMessage,
        transport: crate::p2p::message::TransportMethod,
    ) -> Result<(), String> {
        let res = DeliveryOperations::execute_delivery_with_retry(
            &self.retry_manager,
            self.transport_manager.clone(),
            self.delivery_tracker.clone(),
            to,
            message_id,
            encrypted_message,
            transport,
        )
        .await;
        match res {
            Ok(()) => {
                self.emit_sent_event(to, message_id).await?;
                self.persist_status(to, message_id, DeliveryStatus::Sent, None)
                    .await
            }
            Err(e) => {
                let err_s = format!("{}", e);
                let _ = self
                    .persist_status(
                        to,
                        message_id,
                        DeliveryStatus::Failed(err_s.clone()),
                        Some(err_s.clone()),
                    )
                    .await;
                Err(RoutingError::TransportError(format!("delivery failed: {}", err_s)).to_string())
            }
        }
    }
    /// Handle delivery confirmation from peer
    pub async fn handle_delivery_confirmation(&self, message_id: MessageId) -> Result<(), String> {
        let delivery_tracker = self.delivery_tracker.write().await;
        delivery_tracker
            .update_status(message_id, DeliveryStatus::Delivered)
            .await?;
        // Service-level event emission
        self.emit_delivered_event(message_id).await?;
        // Persist delivered status if we know the peer
        let peer_opt = {
            let tracker = self.delivery_tracker.read().await;
            tracker.get_peer(&message_id).await
        };
        if let Some(peer) = peer_opt {
            self.persist_status(peer, message_id, DeliveryStatus::Delivered, None)
                .await?;
        }
        Ok(())
    }

    /// Get delivery status for message
    pub async fn get_delivery_status(
        &self,
        message_id: MessageId,
    ) -> Result<Option<DeliveryStatus>, String> {
        let delivery_tracker = self.delivery_tracker.read().await;
        Ok(delivery_tracker.get_status(&message_id).await)
    }

    async fn persist_status(
        &self,
        peer_id: PeerId,
        message_id: MessageId,
        status: DeliveryStatus,
        error: Option<String>,
    ) -> Result<(), String> {
        self.persistence
            .update_delivery_status(&message_id, &peer_id, &status, error.as_deref())
            .await
            .map_err(|e| format!("Persistence status update failed: {}", e))?;
        Ok(())
    }

    /// Update WebRTC connection status
    pub async fn update_webrtc_connection(
        &self,
        peer_id: PeerId,
        channel_id: Option<String>,
    ) -> Result<(), String> {
        let mut transport_manager = self.transport_manager.write().await;
        transport_manager.update_webrtc_connection(peer_id, channel_id);
        Ok(())
    }

    /// Update libp2p connection status
    pub async fn update_libp2p_connection(
        &self,
        peer_id: PeerId,
        connected: bool,
    ) -> Result<(), String> {
        let mut transport_manager = self.transport_manager.write().await;
        transport_manager.update_libp2p_connection(peer_id, connected);
        Ok(())
    }
    /// Check for delivery timeouts (should be called periodically)
    pub async fn check_delivery_timeouts(&self) -> Result<(), String> {
        let delivery_tracker = self.delivery_tracker.write().await;
        delivery_tracker.check_timeouts().await
    }
    async fn emit_sent_event(&self, to: PeerId, message_id: MessageId) -> Result<(), String> {
        self.event_sender
            .send(MessageEvent::MessageSent { to, message_id })
            .map_err(|_| "Event channel closed".to_string())?;
        Ok(())
    }
    async fn emit_delivered_event(&self, message_id: MessageId) -> Result<(), String> {
        self.event_sender
            .send(MessageEvent::MessageDelivered { message_id })
            .map_err(|_| "Event channel closed".to_string())?;
        Ok(())
    }
}
