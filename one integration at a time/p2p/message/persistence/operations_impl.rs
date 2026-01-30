use crate::p2p::message::routing::{DeliveryStatus, TransportMethod};
use crate::p2p::message::types::*;
use anyhow::Result;
use libp2p::PeerId;

use super::events_core::{PersistenceEvent, PersistenceEventType};
use super::operations_impl_helpers::OperationsImplHelpers;
use super::queries_analytics::MessageStats;
use super::queries_helpers::MessageFilter;
use super::{EventProcessor, PersistenceOperations, PersistenceQueries};

/// Implementation operations for message retrieval and query operations
#[derive(Clone)]
pub struct OperationsImplCore {
    operations: PersistenceOperations,
    queries: PersistenceQueries,
    event_processor: EventProcessor,
    status_manager: std::sync::Arc<super::operations_status::OperationsStatusManager>,
}

impl OperationsImplCore {
    /// Create new operations implementation core
    pub fn new(
        operations: PersistenceOperations,
        queries: PersistenceQueries,
        event_processor: EventProcessor,
    ) -> Self {
        let status_manager =
            std::sync::Arc::new(super::operations_status::OperationsStatusManager::new(
                operations.clone(),
                queries.clone(),
                event_processor.clone(),
            ));

        Self {
            operations,
            queries,
            event_processor,
            status_manager,
        }
    }

    /// Get message by ID
    pub async fn get_message(&self, message_id: &MessageId) -> Result<Option<P2PMessage>> {
        let message = self.queries.get_message_by_id(message_id).await?;

        if message.is_some() {
            // Emit retrieval event
            self.event_processor
                .emit_persistence_event(PersistenceEvent {
                    event_type: PersistenceEventType::MessageRetrieved,
                    message_id: message_id.clone(),
                    peer_id: None,
                    timestamp: chrono::Utc::now().timestamp(),
                    metadata: None,
                })
                .await?;
        }

        Ok(message)
    }
    /// Get messages with filtering
    pub async fn get_messages_filtered(&self, filter: &MessageFilter) -> Result<Vec<P2PMessage>> {
        self.queries.get_messages_filtered(filter).await
    }

    /// Search messages using full-text search
    pub async fn search_messages(
        &self,
        query: &str,
        limit: Option<u32>,
    ) -> Result<Vec<P2PMessage>> {
        let results = self.queries.search_messages(query, limit).await?;

        // Emit search event
        self.event_processor
            .emit_persistence_event(PersistenceEvent {
                event_type: PersistenceEventType::SearchPerformed,
                message_id: MessageId::new_v4(), // Placeholder for search events
                peer_id: None,
                timestamp: chrono::Utc::now().timestamp(),
                metadata: Some(format!("query:{}, results:{}", query, results.len())),
            })
            .await?;

        Ok(results)
    }
    /// Get delivery status for message
    pub async fn get_delivery_status(
        &self,
        message_id: &MessageId,
    ) -> Result<Vec<(PeerId, DeliveryStatus, TransportMethod)>> {
        self.queries.get_delivery_status(message_id).await
    }

    /// Get message statistics
    pub async fn get_statistics(&self) -> Result<MessageStats> {
        self.queries.get_message_statistics().await
    }

    /// Get messages by peer
    pub async fn get_messages_by_peer(
        &self,
        peer_id: &PeerId,
        limit: Option<u32>,
    ) -> Result<Vec<P2PMessage>> {
        OperationsImplHelpers::get_messages_by_peer_filtered(&self.queries, peer_id, limit).await
    }

    /// Get recent messages
    pub async fn get_recent_messages(&self, limit: Option<u32>) -> Result<Vec<P2PMessage>> {
        OperationsImplHelpers::get_recent_messages_filtered(&self.queries, limit).await
    }

    /// Get messages by type
    pub async fn get_messages_by_type(
        &self,
        message_type: &str,
        limit: Option<u32>,
    ) -> Result<Vec<P2PMessage>> {
        OperationsImplHelpers::get_messages_by_type_filtered(&self.queries, message_type, limit)
            .await
    }

    /// Get failed deliveries
    pub async fn get_failed_deliveries(&self) -> Result<Vec<(MessageId, PeerId, String)>> {
        self.queries.get_failed_deliveries().await
    }

    /// Get pending deliveries
    pub async fn get_pending_deliveries(
        &self,
    ) -> Result<Vec<(MessageId, PeerId, TransportMethod)>> {
        self.queries.get_pending_deliveries().await
    }

    /// Get message count by peer
    pub async fn get_message_count_by_peer(&self, peer_id: &PeerId) -> Result<u64> {
        self.queries.get_message_count_by_peer(peer_id).await
    }

    /// Export messages to JSON
    pub async fn export_messages_json(&self, filter: &MessageFilter) -> Result<String> {
        let messages = self.get_messages_filtered(filter).await?;
        serde_json::to_string_pretty(&messages)
            .map_err(|e| anyhow::anyhow!("Failed to serialize messages: {}", e))
    }

    /// Update delivery status with validation (delegates to status manager)
    pub async fn update_delivery_with_validation(
        &self,
        message_id: &MessageId,
        peer_id: &PeerId,
        new_status: DeliveryStatus,
        error_message: Option<&str>,
    ) -> Result<()> {
        self.status_manager
            .clone()
            .update_delivery_with_validation(message_id, peer_id, new_status, error_message)
            .await
    }

    /// Store sent message using operations field
    pub async fn store_sent_message_via_operations(
        &self,
        message_id: &MessageId,
        to: &PeerId,
        message: &P2PMessage,
        transport: &TransportMethod,
    ) -> Result<()> {
        self.operations
            .store_sent_message(message_id, to, message, transport)
            .await
    }

    /// Get operations reference
    pub fn get_operations(&self) -> &PersistenceOperations {
        &self.operations
    }
}
