use super::events_core::{PersistenceEvent, PersistenceEventType};
use super::{EventProcessor, PersistenceQueries};
use crate::p2p::message::types::*;
use anyhow::Result;

/// Message persistence verification for data integrity
#[derive(Clone)]
pub struct OperationsVerification {
    queries: PersistenceQueries,
    event_processor: EventProcessor,
}

impl OperationsVerification {
    /// Create new operations verification
    pub fn new(queries: PersistenceQueries, event_processor: EventProcessor) -> Self {
        Self {
            queries,
            event_processor,
        }
    }

    /// Verify message persistence with read-back confirmation
    pub async fn verify_message_persisted(
        &self,
        message_id: &MessageId,
        original_message: &P2PMessage,
    ) -> Result<()> {
        let stored_message = self.retrieve_stored_message(message_id).await?;

        self.verify_message_content(message_id, original_message, &stored_message)
            .await
    }

    /// Retrieve stored message from database
    async fn retrieve_stored_message(&self, message_id: &MessageId) -> Result<P2PMessage> {
        self.queries
            .get_message_by_id(message_id)
            .await?
            .ok_or_else(|| anyhow::anyhow!("Message not found: {}", message_id))
    }

    /// Verify stored message content matches original
    async fn verify_message_content(
        &self,
        message_id: &MessageId,
        original_message: &P2PMessage,
        stored_message: &P2PMessage,
    ) -> Result<()> {
        if self.messages_match(original_message, stored_message) {
            Ok(())
        } else {
            self.emit_verification_failure(message_id, "data_mismatch")
                .await?;
            Err(anyhow::anyhow!(
                "Message persistence verification failed: data mismatch for message {}",
                message_id
            ))
        }
    }

    /// Check if two messages have matching core properties
    fn messages_match(&self, original: &P2PMessage, stored: &P2PMessage) -> bool {
        stored.message_type() == original.message_type()
            && stored.message_id() == original.message_id()
            && stored.timestamp() == original.timestamp()
    }

    /// Emit verification failure event
    async fn emit_verification_failure(&self, message_id: &MessageId, reason: &str) -> Result<()> {
        self.event_processor
            .emit_persistence_event(PersistenceEvent {
                event_type: PersistenceEventType::MessageDeleted,
                message_id: message_id.clone(),
                peer_id: None,
                timestamp: chrono::Utc::now().timestamp(),
                metadata: Some(format!("verification_failed:{}", reason)),
            })
            .await
    }
}
