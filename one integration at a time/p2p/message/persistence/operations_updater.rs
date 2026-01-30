use crate::p2p::message::routing::{DeliveryStatus, TransportMethod};
use crate::p2p::message::types::*;
use anyhow::Result;
use libp2p::PeerId;

use super::events_core::{PersistenceEvent, PersistenceEventType};
use super::{EventProcessor, PersistenceOperations, PersistenceQueries};

/// Delivery status update operations with read-modify-write patterns
pub struct OperationsUpdater {
    operations: PersistenceOperations,
    queries: PersistenceQueries,
    event_processor: EventProcessor,
}

impl OperationsUpdater {
    /// Create new operations updater
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

    /// Mark delivery as failed with read-modify-write operation
    pub async fn mark_delivery_failed(
        &self,
        message_id: &MessageId,
        peer_id: &PeerId,
        error_message: &str,
    ) -> Result<()> {
        if self.should_mark_failed(message_id, peer_id).await? {
            let transport = self.get_transport_for_peer(message_id, peer_id).await?;
            self.update_delivery_to_failed(message_id, peer_id, error_message)
                .await?;
            self.emit_delivery_failure_event(message_id, peer_id, &transport)
                .await?;
        }
        Ok(())
    }

    /// Check if delivery should be marked as failed
    async fn should_mark_failed(&self, message_id: &MessageId, peer_id: &PeerId) -> Result<bool> {
        let status = self.get_delivery_status(message_id, peer_id).await?;
        Ok(!matches!(status, Some(DeliveryStatus::Failed(_))))
    }

    /// Get current delivery status for peer
    async fn get_delivery_status(
        &self,
        message_id: &MessageId,
        peer_id: &PeerId,
    ) -> Result<Option<DeliveryStatus>> {
        let statuses = self.queries.get_delivery_status(message_id).await?;
        Ok(statuses
            .iter()
            .find(|(pid, _, _)| pid == peer_id)
            .map(|(_, status, _)| status.clone()))
    }

    /// Get transport method for peer delivery
    async fn get_transport_for_peer(
        &self,
        message_id: &MessageId,
        peer_id: &PeerId,
    ) -> Result<TransportMethod> {
        let statuses = self.queries.get_delivery_status(message_id).await?;
        statuses
            .iter()
            .find(|(pid, _, _)| pid == peer_id)
            .map(|(_, _, transport)| transport.clone())
            .ok_or_else(|| anyhow::anyhow!("Peer status not found"))
    }

    /// Update delivery status to failed
    async fn update_delivery_to_failed(
        &self,
        message_id: &MessageId,
        peer_id: &PeerId,
        error_message: &str,
    ) -> Result<()> {
        self.operations
            .update_delivery_status(
                message_id,
                peer_id,
                &DeliveryStatus::Failed(error_message.to_string()),
                None,
            )
            .await
    }

    /// Emit delivery failure event
    async fn emit_delivery_failure_event(
        &self,
        message_id: &MessageId,
        peer_id: &PeerId,
        transport: &TransportMethod,
    ) -> Result<()> {
        self.event_processor
            .emit_persistence_event(PersistenceEvent {
                event_type: PersistenceEventType::DeliveryStatusUpdated,
                message_id: message_id.clone(),
                peer_id: Some(peer_id.clone()),
                timestamp: chrono::Utc::now().timestamp(),
                metadata: Some(format!("status:Failed,transport:{:?}", transport)),
            })
            .await
    }

    /// Mark delivery as successful with read-modify-write operation
    pub async fn mark_delivery_successful(
        &self,
        message_id: &MessageId,
        peer_id: &PeerId,
    ) -> Result<()> {
        if self.should_mark_successful(message_id, peer_id).await? {
            let transport = self.get_transport_for_peer(message_id, peer_id).await?;
            self.update_delivery_to_successful(message_id, peer_id)
                .await?;
            self.emit_delivery_success_event(message_id, peer_id, &transport)
                .await?;
        }
        Ok(())
    }

    /// Check if delivery should be marked as successful
    async fn should_mark_successful(
        &self,
        message_id: &MessageId,
        peer_id: &PeerId,
    ) -> Result<bool> {
        let status = self.get_delivery_status(message_id, peer_id).await?;
        Ok(!matches!(status, Some(DeliveryStatus::Delivered)))
    }

    /// Update delivery status to successful
    async fn update_delivery_to_successful(
        &self,
        message_id: &MessageId,
        peer_id: &PeerId,
    ) -> Result<()> {
        self.operations
            .update_delivery_status(message_id, peer_id, &DeliveryStatus::Delivered, None)
            .await
    }

    /// Emit delivery success event
    async fn emit_delivery_success_event(
        &self,
        message_id: &MessageId,
        peer_id: &PeerId,
        transport: &TransportMethod,
    ) -> Result<()> {
        self.event_processor
            .emit_persistence_event(PersistenceEvent {
                event_type: PersistenceEventType::DeliveryStatusUpdated,
                message_id: message_id.clone(),
                peer_id: Some(peer_id.clone()),
                timestamp: chrono::Utc::now().timestamp(),
                metadata: Some(format!("status:Delivered,transport:{:?}", transport)),
            })
            .await
    }
}
