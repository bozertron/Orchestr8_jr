use crate::p2p::message::persistence::events_core::{PersistenceEvent, PersistenceEventType};
use crate::p2p::message::routing::DeliveryStatus;
use crate::p2p::message::storage;
use crate::p2p::message::types::*;
use anyhow::Result;
use libp2p::PeerId;

impl super::service_operations::ServiceOperationsImpl {
    /// Emit message stored event (push-based architecture)
    pub(super) async fn emit_message_stored_event(
        &self,
        message_id: &MessageId,
        peer_id: Option<PeerId>,
        metadata: Option<String>,
    ) -> Result<()> {
        self.core()
            .event_processor()
            .emit_persistence_event(PersistenceEvent {
                event_type: PersistenceEventType::MessageStored,
                message_id: message_id.clone(),
                peer_id,
                timestamp: chrono::Utc::now().timestamp(),
                metadata,
            })
            .await
    }

    /// Emit delivery status updated event (push-based architecture)
    pub(super) async fn emit_delivery_status_updated_event(
        &self,
        message_id: &MessageId,
        peer_id: &PeerId,
        status: &DeliveryStatus,
        error_message: Option<&str>,
    ) -> Result<()> {
        let metadata = format!(
            "status:{:?}{}",
            status,
            error_message
                .map(|e| format!(",error:{}", e))
                .unwrap_or_default()
        );

        self.core()
            .event_processor()
            .emit_persistence_event(PersistenceEvent {
                event_type: PersistenceEventType::DeliveryStatusUpdated,
                message_id: message_id.clone(),
                peer_id: Some(*peer_id),
                timestamp: chrono::Utc::now().timestamp(),
                metadata: Some(metadata),
            })
            .await
    }

    /// Emit message deleted event (push-based architecture)
    pub(super) async fn emit_message_deleted_event(&self, message_id: &MessageId) -> Result<()> {
        self.core()
            .event_processor()
            .emit_persistence_event(PersistenceEvent {
                event_type: PersistenceEventType::MessageDeleted,
                message_id: message_id.clone(),
                peer_id: None,
                timestamp: chrono::Utc::now().timestamp(),
                metadata: None,
            })
            .await
    }

    /// Convert stored messages to P2P messages for API compatibility
    pub fn convert_stored_messages_to_api(stored_messages: Vec<StoredMessage>) -> Vec<P2PMessage> {
        stored_messages.into_iter().map(|sm| sm.message).collect()
    }

    /// Convert P2P messages to stored message format with peer context
    pub(super) fn convert_stored_messages_to_stored_api(
        messages: Vec<P2PMessage>,
        peer_id: &PeerId,
    ) -> Result<Vec<storage::StoredMessage>> {
        Ok(messages
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
            .collect())
    }
}
