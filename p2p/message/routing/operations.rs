use super::delivery::DeliveryTracker;
use super::retry::RetryManager;
use super::transport::TransportManager;
use super::TransportMethod;
use crate::p2p::message::types::{EncryptedMessage, MessageId};

use libp2p::PeerId;
use std::sync::Arc;
use tokio::sync::RwLock;

/// Delivery operations for routing service
pub struct DeliveryOperations;

impl DeliveryOperations {
    /// Select transport and prepare delivery tracking
    pub async fn select_and_prepare_transport(
        transport_manager: &Arc<RwLock<TransportManager>>,
        delivery_tracker: &Arc<RwLock<DeliveryTracker>>,
        to: PeerId,
        message_id: MessageId,
    ) -> Result<TransportMethod, String> {
        // Select transport method
        let transport = {
            let tm = transport_manager.read().await;
            tm.select_transport(&to).await?
        };

        // Start delivery tracking
        {
            let dt = delivery_tracker.write().await;
            dt.start_tracking(message_id, to, transport.clone()).await?;
        }

        Ok(transport)
    }

    /// Execute delivery with retry logic
    pub async fn execute_delivery_with_retry(
        retry_manager: &RetryManager,
        transport_manager: Arc<RwLock<TransportManager>>,
        delivery_tracker: Arc<RwLock<DeliveryTracker>>,
        to: PeerId,
        message_id: MessageId,
        encrypted_message: EncryptedMessage,
        transport: TransportMethod,
    ) -> Result<(), String> {
        retry_manager
            .execute_with_retry_ctx(
                transport_manager,
                delivery_tracker,
                to,
                message_id,
                encrypted_message,
                transport,
            )
            .await
    }

    /// Validate encrypted message size
    pub fn validate_message_size(
        encrypted_message: &EncryptedMessage,
        max_size: usize,
    ) -> Result<(), String> {
        let serialized_size = serde_json::to_vec(encrypted_message)
            .map_err(|e| format!("Size validation failed: {}", e))?
            .len();

        if serialized_size > max_size {
            return Err(format!(
                "Message too large: {} > {}",
                serialized_size, max_size
            ));
        }

        Ok(())
    }
}
