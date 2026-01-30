use crate::p2p::message::persistence::queries_analytics::MessageStats;
use crate::p2p::message::persistence::queries_helpers::MessageFilter;
use crate::p2p::message::routing::{DeliveryStatus, TransportMethod};
use crate::p2p::message::types::*;
use crate::p2p::MessageEvent;
use anyhow::Result;
use libp2p::PeerId;

impl super::service_core::PersistenceService {
    // Message operations delegation
    /// Store sent message with routing integration (Task 3.4 integration)
    pub async fn store_sent_message(
        &self,
        message_id: &MessageId,
        to: &PeerId,
        message: &P2PMessage,
        transport_method: &TransportMethod,
    ) -> Result<()> {
        self.operations_impl
            .store_sent_message(message_id, to, message, transport_method)
            .await
    }
    /// Store received message with sender information
    pub async fn store_received_message(
        &self,
        message: &P2PMessage,
        from: &PeerId,
        message_id: Option<MessageId>,
    ) -> Result<MessageId> {
        self.operations_impl
            .store_received_message(message, from, message_id)
            .await
    }
    /// Update delivery status (routing system integration)
    pub async fn update_delivery_status(
        &self,
        message_id: &MessageId,
        peer_id: &PeerId,
        status: &DeliveryStatus,
        error_message: Option<&str>,
    ) -> Result<()> {
        self.operations_impl
            .update_delivery_status(message_id, peer_id, status, error_message)
            .await
    }
    /// Get message by ID
    pub async fn get_message(&self, message_id: &MessageId) -> Result<Option<P2PMessage>> {
        self.operations_impl.get_message(message_id).await
    }
    /// Get messages with filtering
    pub async fn get_messages_filtered(&self, filter: &MessageFilter) -> Result<Vec<P2PMessage>> {
        self.operations_impl.get_messages_filtered(filter).await
    }
    /// Search messages using full-text search
    pub async fn search_messages(
        &self,
        query: &str,
        limit: Option<u32>,
    ) -> Result<Vec<P2PMessage>> {
        self.operations_impl.search_messages(query, limit).await
    }
    /// Get delivery status for message
    pub async fn get_delivery_status(
        &self,
        message_id: &MessageId,
    ) -> Result<Vec<(PeerId, DeliveryStatus, TransportMethod)>> {
        self.operations_impl.get_delivery_status(message_id).await
    }
    /// Delete message and all related records
    pub async fn delete_message(&self, message_id: &MessageId) -> Result<bool> {
        self.operations_impl.delete_message(message_id).await
    }
    /// Get message statistics
    pub async fn get_statistics(&self) -> Result<MessageStats> {
        self.operations_impl.get_statistics().await
    }
    /// Get message history for a peer
    pub async fn get_message_history(
        &self,
        peer_id: &PeerId,
        limit: Option<usize>,
    ) -> Result<Vec<P2PMessage>> {
        let stored_messages = self
            .operations_impl
            .get_message_history(peer_id, limit)
            .await?;
        Ok(
            super::service_operations::ServiceOperationsImpl::convert_stored_messages_to_api(
                stored_messages,
            ),
        )
    }

    // Event processing delegation
    /// Get unprocessed events for external processing
    pub async fn get_unprocessed_events(&self, limit: Option<u32>) -> Result<Vec<MessageEvent>> {
        let persistence_events = self.maintenance_impl.get_unprocessed_events(limit).await?;
        // Convert PersistenceEvent to MessageEvent
        let message_events = persistence_events
            .into_iter()
            .map(|pe| {
                // This is a simplified conversion - in a real implementation,
                // we'd need proper conversion logic based on event type
                use crate::p2p::message::types::core::P2PMessage;
                use libp2p::PeerId;
                let peer = pe.peer_id.unwrap_or_else(|| PeerId::random());
                // Create a placeholder message since we only have the message_id
                let placeholder_message = P2PMessage::DeliveryConfirmation {
                    message_id: pe.message_id,
                    timestamp: chrono::Utc::now(),
                };
                MessageEvent::MessageReceived {
                    from: peer,
                    message: placeholder_message,
                }
            })
            .collect();
        Ok(message_events)
    }

    /// Mark events as processed
    pub async fn mark_events_processed(&self, message_ids: &[MessageId]) -> Result<()> {
        self.maintenance_impl
            .mark_events_processed(message_ids)
            .await
    }
    // Maintenance operations delegation
    /// Cleanup old events and optimize database
    pub async fn maintenance_cleanup(
        &self,
        older_than_days: u32,
    ) -> Result<super::service_maintenance::MaintenanceResult> {
        self.maintenance_impl
            .maintenance_cleanup(older_than_days)
            .await
    }
    /// Health check for persistence service
    pub async fn health_check(&self) -> Result<super::service_maintenance::PersistenceHealth> {
        self.maintenance_impl.health_check().await
    }
}
