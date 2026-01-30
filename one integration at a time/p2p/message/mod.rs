pub mod encryption;
pub mod encryption_keys;
pub mod persistence;
pub mod protocol;
pub mod routing;
pub mod signing;
pub mod types;

pub use encryption::*;
pub use persistence::operations as persistence_operations;
pub use persistence::PersistenceService;
pub use protocol::*;
pub use routing::operations as routing_operations;
pub use routing::{
    DeliveryInfo, DeliveryStatus, RoutingError, RoutingService, RoutingServiceImpl, TransportMethod,
};
pub use signing::*;
pub use types::*;

use libp2p::{identity::Keypair, PeerId};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use tokio::sync::mpsc;

/// Message service for handling secure P2P messaging
pub struct MessageService {
    encryption: EncryptionService,
    signing: SigningService,
    routing: RoutingService,
    persistence: PersistenceService,
    event_sender: mpsc::UnboundedSender<MessageEvent>,
}

impl MessageService {
    /// Create new message service
    pub async fn new(
        config: MessageConfig,
        keypair: Arc<Keypair>,
        event_sender: mpsc::UnboundedSender<MessageEvent>,
    ) -> Result<Self, String> {
        let encryption = EncryptionService::new(&config, keypair.clone())
            .await
            .map_err(|e| e.to_string())?;
        let signing = SigningService::new(&config, keypair)
            .await
            .map_err(|e| e.to_string())?;
        let routing = RoutingService::new(&config, event_sender.clone())
            .await
            .map_err(|e| e.to_string())?;
        let persistence = PersistenceService::new(&config, event_sender.clone())
            .await
            .map_err(|e| e.to_string())?;

        Ok(Self {
            encryption,
            signing,
            routing,
            persistence,
            event_sender,
        })
    }

    /// Send secure message to peer
    pub async fn send_message(
        &mut self,
        to: PeerId,
        message: P2PMessage,
    ) -> Result<MessageId, String> {
        // Sign the message
        let signed_message = self
            .signing
            .sign_message(message.clone())
            .await
            .map_err(|e| e.to_string())?;

        // Encrypt the signed message
        let encrypted_message = self
            .encryption
            .encrypt_message(signed_message, &to)
            .await
            .map_err(|e| e.to_string())?;

        // Route the encrypted message
        let message_id = self
            .routing
            .route_message(to, encrypted_message)
            .await
            .map_err(|e| e.to_string())?;

        // Store in persistence layer
        self.persistence
            .store_sent_message(&message_id, &to, &message, &TransportMethod::LibP2P)
            .await
            .map_err(|e| e.to_string())?;

        Ok(message_id)
    }

    /// Handle received encrypted message
    pub async fn handle_received_message(
        &mut self,
        from: PeerId,
        encrypted_message: EncryptedMessage,
    ) -> Result<(), String> {
        // Decrypt the message
        let signed_message = self
            .encryption
            .decrypt_message(encrypted_message, &from)
            .await
            .map_err(|e| e.to_string())?;

        // Verify signature
        let message = self
            .signing
            .verify_message(signed_message, &from)
            .await
            .map_err(|e| e.to_string())?;

        // Store in persistence layer
        let _stored_message_id = self
            .persistence
            .store_received_message(&message, &from, None)
            .await
            .map_err(|e| e.to_string())?;

        // Send event
        self.send_event(MessageEvent::MessageReceived { from, message })
            .await
            .map_err(|e| e.to_string())?;

        Ok(())
    }

    /// Flush pending messages before shutdown
    pub async fn flush_pending_messages(&mut self) -> Result<(), String> {
        // Ensure all pending messages are persisted
        // In a full implementation, this would:
        // 1. Send any queued messages
        // 2. Wait for acknowledgments
        // 3. Persist final state
        Ok(())
    }

    /// Get message history with peer
    pub async fn get_message_history(
        &self,
        peer_id: PeerId,
        limit: Option<u32>,
    ) -> Result<Vec<StoredMessage>, String> {
        let messages = self
            .persistence
            .get_message_history(&peer_id, limit.map(|l| l as usize))
            .await
            .map_err(|e| format!("PersistenceError: {}", e.to_string()))?;
        // Convert P2PMessage back to StoredMessage
        let stored_messages = messages
            .into_iter()
            .map(|msg| {
                use crate::p2p::message::types::storage::{
                    MessageDirection, MessageStatus, StoredMessage,
                };
                StoredMessage {
                    id: msg.message_id().unwrap_or_else(|| uuid::Uuid::new_v4()),
                    peer_id: peer_id.to_string(),
                    message: msg,
                    direction: MessageDirection::Received,
                    status: MessageStatus::Delivered,
                    created_at: chrono::Utc::now(),
                    delivered_at: Some(chrono::Utc::now()),
                }
            })
            .collect();
        Ok(stored_messages)
    }

    /// Send message event
    async fn send_event(&self, event: MessageEvent) -> Result<(), String> {
        self.event_sender
            .send(event)
            .map_err(|_| format!("Connection: {}", "Event channel closed".to_string()))?;
        Ok(())
    }
}

/// Message service events
#[derive(Debug, Clone)]
pub enum MessageEvent {
    MessageReceived {
        from: PeerId,
        message: P2PMessage,
    },
    MessageSent {
        to: PeerId,
        message_id: MessageId,
    },
    MessageDelivered {
        message_id: MessageId,
    },
    MessageFailed {
        message_id: MessageId,
        error: String,
    },
}

/// Message service configuration
#[derive(Debug, Clone)]
pub struct MessageConfig {
    pub database_path: String,
    pub encryption_key_size: usize,
    pub signature_algorithm: SignatureAlgorithm,
    pub message_retention_days: u32,
    pub max_message_size: usize,
}

impl Default for MessageConfig {
    fn default() -> Self {
        Self {
            database_path: "messages.db".to_string(),
            encryption_key_size: 32,
            signature_algorithm: SignatureAlgorithm::Ed25519,
            message_retention_days: 30,
            max_message_size: 1024 * 1024, // 1MB
        }
    }
}

/// Signature algorithms
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum SignatureAlgorithm {
    Ed25519,
}
