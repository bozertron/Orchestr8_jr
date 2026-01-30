use crate::p2p::message::routing::{DeliveryStatus, TransportMethod};
use crate::p2p::message::types::*;
use anyhow::Result;
use libp2p::PeerId;

use super::{EventProcessor, PersistenceOperations, PersistenceQueries};

/// Delivery status operations with read-modify-write validation
pub struct OperationsStatusManager {
    operations: PersistenceOperations,
    queries: PersistenceQueries,
    event_processor: EventProcessor,
}

impl OperationsStatusManager {
    /// Create new status operations manager
    pub fn new(
        operations: PersistenceOperations,
        queries: PersistenceQueries,
        event_processor: EventProcessor,
    ) -> Self {
        Self {
            operations,
            queries,
            event_processor,
        }
    }

    /// Perform delivery status update with validation
    pub async fn update_delivery_with_validation(
        &self,
        message_id: &MessageId,
        peer_id: &PeerId,
        new_status: DeliveryStatus,
        error_message: Option<&str>,
    ) -> Result<()> {
        let (can_update, transport) = self
            .retrieve_and_validate_status(message_id, peer_id, &new_status)
            .await?;

        if can_update {
            self.operations
                .update_delivery_status(message_id, peer_id, &new_status, error_message)
                .await?;

            self.event_processor
                .emit_persistence_event(super::events_core::PersistenceEvent {
                    event_type: super::events_core::PersistenceEventType::DeliveryStatusUpdated,
                    message_id: message_id.clone(),
                    peer_id: Some(peer_id.clone()),
                    timestamp: chrono::Utc::now().timestamp(),
                    metadata: Some(format!("status:{:?},transport:{:?}", new_status, transport)),
                })
                .await?;
        }

        Ok(())
    }

    /// Retrieve current status and validate transition
    async fn retrieve_and_validate_status(
        &self,
        message_id: &MessageId,
        peer_id: &PeerId,
        new_status: &DeliveryStatus,
    ) -> Result<(bool, TransportMethod)> {
        let current_statuses = self.queries.get_delivery_status(message_id).await?;
        let current_info = current_statuses.iter().find(|(pid, _, _)| pid == peer_id);

        match current_info {
            Some((_, current_status, transport)) => {
                let can_transition = Self::can_transition_status(current_status, new_status);
                Ok((can_transition, transport.clone()))
            }
            None => Ok((false, TransportMethod::LibP2P)),
        }
    }

    /// Validate delivery status transitions
    fn can_transition_status(current: &DeliveryStatus, new: &DeliveryStatus) -> bool {
        match (current, new) {
            (DeliveryStatus::Pending, _) => true,
            (DeliveryStatus::Sent, DeliveryStatus::Delivered) => true,
            (DeliveryStatus::Sent, DeliveryStatus::Failed(_)) => true,
            (DeliveryStatus::Sent, DeliveryStatus::Timeout) => true,
            (DeliveryStatus::Delivered, _) => false,
            (DeliveryStatus::Failed(_), _) => false,
            (DeliveryStatus::Timeout, _) => false,
            _ => false,
        }
    }
}
