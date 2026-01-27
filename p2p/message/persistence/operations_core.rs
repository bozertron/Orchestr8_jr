use crate::p2p::message::routing::{DeliveryStatus, TransportMethod};
use crate::p2p::message::types::*;
use anyhow::Result;
use libp2p::PeerId;

use super::events_core::{PersistenceEvent, PersistenceEventType};
use super::operations_verification::OperationsVerification;
use super::{EventProcessor, PersistenceOperations, PersistenceQueries};

pub use super::operations_core_helpers::OperationsStats;

/// Core operations implementation for message storage with event integration
#[derive(Clone)]
pub struct OperationsCoreImpl {
    operations: PersistenceOperations,
    verification: OperationsVerification,
    event_processor: EventProcessor,
}

impl OperationsCoreImpl {
    /// Create new operations core implementation
    pub fn new(
        operations: PersistenceOperations,
        queries: PersistenceQueries,
        event_processor: EventProcessor,
    ) -> Self {
        let verification = OperationsVerification::new(queries, event_processor.clone());
        Self {
            operations,
            verification,
            event_processor,
        }
    }

    /// Get event processor (accessor pattern)
    pub fn event_processor(&self) -> &EventProcessor {
        &self.event_processor
    }

    /// Store sent message with routing integration (Task 3.4 integration)
    pub async fn store_sent_message(
        &self,
        message_id: &MessageId,
        to: &PeerId,
        message: &P2PMessage,
        transport_method: &TransportMethod,
    ) -> Result<()> {
        // Store message and delivery status
        self.operations
            .store_sent_message(message_id, to, message, transport_method)
            .await?;

        // Verify persistence with read-back confirmation
        self.verification
            .verify_message_persisted(message_id, message)
            .await?;

        // Emit persistence event
        self.event_processor
            .emit_persistence_event(PersistenceEvent {
                event_type: PersistenceEventType::MessageStored,
                message_id: message_id.clone(),
                peer_id: Some(to.clone()),
                timestamp: chrono::Utc::now().timestamp(),
                metadata: Some(format!("transport:{:?}", transport_method)),
            })
            .await?;

        Ok(())
    }

    /// Store received message with sender information
    pub async fn store_received_message(
        &self,
        message: &P2PMessage,
        from: &PeerId,
        message_id: Option<MessageId>,
    ) -> Result<MessageId> {
        let final_message_id = self
            .operations
            .store_received_message(message, from, message_id)
            .await?;

        // Emit persistence event
        self.event_processor
            .emit_persistence_event(PersistenceEvent {
                event_type: PersistenceEventType::MessageStored,
                message_id: final_message_id.clone(),
                peer_id: Some(from.clone()),
                timestamp: chrono::Utc::now().timestamp(),
                metadata: Some("direction:received".to_string()),
            })
            .await?;

        Ok(final_message_id)
    }

    /// Update delivery status (routing system integration)
    pub async fn update_delivery_status(
        &self,
        message_id: &MessageId,
        peer_id: &PeerId,
        status: &DeliveryStatus,
        error_message: Option<&str>,
    ) -> Result<()> {
        self.operations
            .update_delivery_status(message_id, peer_id, status, error_message)
            .await?;

        // Emit status update event
        self.event_processor
            .emit_persistence_event(PersistenceEvent {
                event_type: PersistenceEventType::DeliveryStatusUpdated,
                message_id: message_id.clone(),
                peer_id: Some(peer_id.clone()),
                timestamp: chrono::Utc::now().timestamp(),
                metadata: Some(format!("status:{:?}", status)),
            })
            .await?;

        Ok(())
    }

    /// Delete message and all related records
    pub async fn delete_message(&self, message_id: &MessageId) -> Result<bool> {
        let deleted = self.operations.delete_message(message_id).await?;

        if deleted {
            // Emit deletion event
            self.event_processor
                .emit_persistence_event(PersistenceEvent {
                    event_type: PersistenceEventType::MessageDeleted,
                    message_id: message_id.clone(),
                    peer_id: None,
                    timestamp: chrono::Utc::now().timestamp(),
                    metadata: None,
                })
                .await?;
        }

        Ok(deleted)
    }
    /// Batch store multiple messages with event emission
    pub async fn batch_store_messages(
        &self,
        messages: Vec<(MessageId, PeerId, P2PMessage, TransportMethod)>,
    ) -> Result<Vec<MessageId>> {
        let mut stored_ids = Vec::new();

        for (message_id, peer_id, message, transport_method) in messages {
            self.store_sent_message(&message_id, &peer_id, &message, &transport_method)
                .await?;
            stored_ids.push(message_id);
        }

        Ok(stored_ids)
    }
    /// Batch update delivery statuses
    pub async fn batch_update_delivery_status(
        &self,
        updates: Vec<(MessageId, PeerId, DeliveryStatus, Option<String>)>,
    ) -> Result<()> {
        for (message_id, peer_id, status, error_message) in updates {
            self.update_delivery_status(&message_id, &peer_id, &status, error_message.as_deref())
                .await?;
        }

        Ok(())
    }
}
