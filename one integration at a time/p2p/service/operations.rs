use crate::p2p::message::{MessageId, MessageService, P2PMessage};
use anyhow::{Context, Result};
use libp2p::PeerId;
use std::sync::Arc;
use tokio::sync::RwLock;
use tracing::debug;

/// P2P service operations for message handling
pub struct ServiceOperations;

impl ServiceOperations {
    /// Send message through message service
    pub async fn send_message(
        message_service: Arc<RwLock<Option<MessageService>>>,
        peer_id: PeerId,
        text: String,
    ) -> Result<MessageId> {
        debug!("Sending message to peer: {}", peer_id);

        // Get mutable message service
        let mut service_guard = message_service.write().await;

        let service = service_guard
            .as_mut()
            .context("Message service not initialized")?;

        // Create chat message
        let message = P2PMessage::Chat {
            id: uuid::Uuid::new_v4(),
            text,
            timestamp: chrono::Utc::now(),
            reply_to: None,
        };

        // Send message
        service
            .send_message(peer_id, message)
            .await
            .map_err(|e| anyhow::anyhow!("Failed to send message: {}", e))
    }
}
