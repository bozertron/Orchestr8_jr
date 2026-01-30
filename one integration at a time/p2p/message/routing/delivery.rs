use super::{DeliveryInfo, DeliveryStatus, TransportMethod};
use crate::p2p::message::types::MessageId;
use crate::p2p::MessageEvent;
use libp2p::PeerId;
use std::collections::HashMap;
use std::sync::Arc;
use std::time::{Duration, Instant};
use tokio::sync::{mpsc, RwLock};

/// Delivery tracker for managing message delivery status with concurrent access
pub struct DeliveryTracker {
    deliveries: Arc<RwLock<HashMap<MessageId, DeliveryInfo>>>,
    event_sender: mpsc::UnboundedSender<MessageEvent>,
    delivery_timeout: Duration,
}

impl DeliveryTracker {
    /// Create new delivery tracker
    pub fn new(
        event_sender: mpsc::UnboundedSender<MessageEvent>,
        delivery_timeout: Duration,
    ) -> Self {
        Self {
            deliveries: Arc::new(RwLock::new(HashMap::new())),
            event_sender,
            delivery_timeout,
        }
    }

    /// Start tracking delivery for a message
    pub async fn start_tracking(
        &self,
        message_id: MessageId,
        to: PeerId,
        transport: TransportMethod,
    ) -> Result<(), String> {
        let delivery_info = DeliveryInfo {
            message_id,
            to,
            status: DeliveryStatus::Pending,
            transport,
            created_at: Instant::now(),
            attempts: 0,
            last_attempt: None,
        };

        let mut deliveries = self.deliveries.write().await;
        deliveries.insert(message_id, delivery_info);
        Ok(())
    }

    /// Update delivery status
    pub async fn update_status(
        &self,
        message_id: MessageId,
        status: DeliveryStatus,
    ) -> Result<(), String> {
        let deliveries = self.deliveries.read().await;
        let to = if let Some(delivery) = deliveries.get(&message_id) {
            delivery.to
        } else {
            return Ok(());
        };

        drop(deliveries); // Release read lock before taking write lock

        // Update the status
        {
            let mut deliveries = self.deliveries.write().await;
            if let Some(delivery) = deliveries.get_mut(&message_id) {
                delivery.status = status.clone();
            }
        }

        self.emit_status_event(message_id, status, to).await?;
        Ok(())
    }

    /// Emit appropriate event based on status
    async fn emit_status_event(
        &self,
        message_id: MessageId,
        status: DeliveryStatus,
        to: PeerId,
    ) -> Result<(), String> {
        match status {
            DeliveryStatus::Sent => self.emit_sent_event(to, message_id).await,
            DeliveryStatus::Delivered => self.emit_delivered_event(message_id).await,
            DeliveryStatus::Failed(ref error) => {
                self.emit_failed_event(message_id, error.clone()).await
            }
            DeliveryStatus::Timeout => self.emit_timeout_event(message_id).await,
            _ => Ok(()),
        }
    }

    async fn emit_sent_event(&self, to: PeerId, message_id: MessageId) -> Result<(), String> {
        self.send_event(MessageEvent::MessageSent { to, message_id })
            .await
    }

    async fn emit_delivered_event(&self, message_id: MessageId) -> Result<(), String> {
        self.send_event(MessageEvent::MessageDelivered { message_id })
            .await?;
        let mut deliveries = self.deliveries.write().await;
        deliveries.remove(&message_id);
        Ok(())
    }

    async fn emit_failed_event(&self, message_id: MessageId, error: String) -> Result<(), String> {
        self.send_event(MessageEvent::MessageFailed { message_id, error })
            .await?;
        let mut deliveries = self.deliveries.write().await;
        deliveries.remove(&message_id);
        Ok(())
    }

    async fn emit_timeout_event(&self, message_id: MessageId) -> Result<(), String> {
        let error_msg = "Delivery timeout".to_string();
        self.send_event(MessageEvent::MessageFailed {
            message_id,
            error: error_msg,
        })
        .await?;
        let mut deliveries = self.deliveries.write().await;
        deliveries.remove(&message_id);
        Ok(())
    }

    /// Increment attempt count
    pub async fn increment_attempts(&self, message_id: MessageId) -> Result<u32, String> {
        let mut deliveries = self.deliveries.write().await;
        if let Some(delivery) = deliveries.get_mut(&message_id) {
            delivery.attempts += 1;
            delivery.last_attempt = Some(Instant::now());
            Ok(delivery.attempts)
        } else {
            Err("Message not found in delivery tracker".to_string())
        }
    }

    /// Get delivery status
    pub async fn get_status(&self, message_id: &MessageId) -> Option<DeliveryStatus> {
        let deliveries = self.deliveries.read().await;
        deliveries.get(message_id).map(|d| d.status.clone())
    }

    /// Get peer for a message id (recipient)
    pub async fn get_peer(&self, message_id: &MessageId) -> Option<PeerId> {
        let deliveries = self.deliveries.read().await;
        deliveries.get(message_id).map(|d| d.to)
    }

    /// Check for timed out deliveries
    pub async fn check_timeouts(&self) -> Result<(), String> {
        let now = Instant::now();
        let mut timed_out = Vec::new();

        // Check which messages have timed out
        {
            let deliveries = self.deliveries.read().await;
            for (message_id, delivery) in deliveries.iter() {
                if delivery.status == DeliveryStatus::Pending
                    || delivery.status == DeliveryStatus::Sent
                {
                    if now.duration_since(delivery.created_at) > self.delivery_timeout {
                        timed_out.push(*message_id);
                    }
                }
            }
        }

        // Update timeout statuses
        for message_id in timed_out {
            self.update_status(message_id, DeliveryStatus::Timeout)
                .await?;
        }

        Ok(())
    }

    /// Send event through channel
    async fn send_event(&self, event: MessageEvent) -> Result<(), String> {
        self.event_sender
            .send(event)
            .map_err(|_| "Event channel closed".to_string())?;
        Ok(())
    }
    /// Start a background timeout watcher loop that periodically checks for timed out deliveries
    /// Uses Arc<RwLock<DeliveryTracker>> to coordinate concurrent access from service layer
    pub fn start_timeout_watcher(tracker: Arc<RwLock<Self>>, interval: Duration) {
        tokio::spawn(async move {
            loop {
                {
                    let t = tracker.write().await;
                    // check_timeouts emits MessageEvent::MessageFailed for timeouts
                    let _ = t.check_timeouts().await;
                }
                tokio::time::sleep(interval).await;
            }
        });
    }
}
