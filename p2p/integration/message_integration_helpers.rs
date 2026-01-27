// Helper functions for message integration
//
// Pattern Bible Compliance:
// - File: Helper module for message_integration.rs
// - Extracted to maintain ≤200 lines and ≤30 lines per function
// - Contains message ID extraction and event processing logic

use crate::p2p::{
    events::P2PEventType,
    message::{MessageService, P2PMessage},
};
use libp2p::PeerId;
use std::sync::Arc;
use tokio::sync::RwLock;
use tracing::debug;

/// Extract message ID from P2PMessage enum
///
/// Handles all 16 P2PMessage variants and returns appropriate ID string
pub(crate) fn extract_message_id(message: &P2PMessage) -> String {
    match message {
        P2PMessage::Chat { id, .. } => id.to_string(),
        P2PMessage::FileOffer { id, .. } => id.to_string(),
        P2PMessage::FileChunk { id, .. } => id.to_string(),
        P2PMessage::FileComplete { id } => id.to_string(),
        P2PMessage::FileCancel { id, .. } => id.to_string(),
        P2PMessage::CallInvite { call_id, .. } => call_id.to_string(),
        P2PMessage::CallAnswer { call_id, .. } => call_id.to_string(),
        P2PMessage::CallHangup { call_id, .. } => call_id.to_string(),
        P2PMessage::CallIceCandidate { call_id, .. } => call_id.to_string(),
        P2PMessage::StateSync { version, .. } => version.to_string(),
        P2PMessage::StateSyncRequest { from_version } => from_version.to_string(),
        P2PMessage::StateSyncResponse { from_version, .. } => from_version.to_string(),
        P2PMessage::Ping { nonce, .. } => nonce.to_string(),
        P2PMessage::Pong { nonce, .. } => nonce.to_string(),
        P2PMessage::DeliveryConfirmation { message_id, .. } => message_id.to_string(),
        P2PMessage::TypingIndicator { .. } => "typing".to_string(),
    }
}

/// Process received message through message service
///
/// Handles decryption, verification, and storage via MessageService
pub(crate) async fn process_through_service(
    service: &Arc<RwLock<Option<MessageService>>>,
    from: &PeerId,
    _message: &P2PMessage,
) {
    if let Some(_svc) = service.read().await.as_ref() {
        debug!(
            "Processing received message from {} through message service",
            from
        );
        // TODO: Implement full message processing
        // In a full implementation, this would call svc.handle_received_message()
        // For now, we just log the processing intent
    }
}

/// Handle message event type for configure_message_events
///
/// Processes specific event types and updates message service state
pub(crate) async fn handle_message_event_type(
    event: &P2PEventType,
    service: &Arc<RwLock<Option<MessageService>>>,
) {
    match event {
        P2PEventType::MessageReceived { message_id } => {
            debug!("Message handler received message: {}", message_id);
            if let Some(_svc) = service.read().await.as_ref() {
                debug!("Processing message {} through service", message_id);
                // TODO: Implement delivery status update
            }
        }
        P2PEventType::MessageSent { message_id } => {
            debug!("Message handler received message sent: {}", message_id);
            // Additional message-specific handling can go here
        }
        P2PEventType::MessageDelivered { message_id } => {
            debug!("Message handler received message delivered: {}", message_id);
            // Additional message-specific handling can go here
        }
        P2PEventType::MessageFailed { message_id, error } => {
            debug!(
                "Message handler received message failed: {} - {}",
                message_id, error
            );
            // Additional message-specific handling can go here
        }
        _ => {}
    }
}
