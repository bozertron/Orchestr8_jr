use crate::p2p::message::routing::{DeliveryStatus, TransportMethod};
use crate::p2p::message::types::*;
use anyhow::{Context, Result};
use libp2p::PeerId;

use super::{queries_analytics::MessageStats, queries_helpers::MessageFilter};
use super::{EventProcessor, PersistenceOperations, PersistenceQueries};

// Import modular operations components
use super::operations_core::OperationsCoreImpl;
use super::operations_impl::OperationsImplCore;

/// Service operations implementation for message storage and retrieval
#[derive(Clone)]
pub struct ServiceOperationsImpl {
    core: OperationsCoreImpl,
    implementation: OperationsImplCore,
}

impl ServiceOperationsImpl {
    /// Create new service operations implementation
    pub fn new(
        operations: PersistenceOperations,
        queries: PersistenceQueries,
        event_processor: EventProcessor,
    ) -> Self {
        Self {
            core: OperationsCoreImpl::new(
                operations.clone(),
                queries.clone(),
                event_processor.clone(),
            ),
            implementation: OperationsImplCore::new(operations, queries, event_processor),
        }
    }

    /// Get core operations (accessor pattern)
    pub(super) fn core(&self) -> &OperationsCoreImpl {
        &self.core
    }
    /// Store sent message with routing integration (Task 3.4 integration)
    pub async fn store_sent_message(
        &self,
        message_id: &MessageId,
        to: &PeerId,
        message: &P2PMessage,
        transport_method: &TransportMethod,
    ) -> Result<()> {
        self.core
            .store_sent_message(message_id, to, message, transport_method)
            .await
            .context("Failed to store sent message in persistence operations")?;

        // Emit event using helper (push-based architecture)
        self.emit_message_stored_event(
            message_id,
            Some(*to),
            Some(format!("transport:{:?}", transport_method)),
        )
        .await?;

        tracing::debug!("Message stored with event emission: {}", message_id);
        Ok(())
    }

    /// Store received message with sender information
    pub async fn store_received_message(
        &self,
        message: &P2PMessage,
        from: &PeerId,
        message_id: Option<MessageId>,
    ) -> Result<MessageId> {
        let msg_id = self
            .core
            .store_received_message(message, from, message_id)
            .await?;

        // Emit event using helper (push-based architecture)
        self.emit_message_stored_event(
            &msg_id,
            Some(*from),
            Some("direction:received".to_string()),
        )
        .await?;

        Ok(msg_id)
    }

    /// Update delivery status (routing system integration)
    pub async fn update_delivery_status(
        &self,
        message_id: &MessageId,
        peer_id: &PeerId,
        status: &DeliveryStatus,
        error_message: Option<&str>,
    ) -> Result<()> {
        self.core
            .update_delivery_status(message_id, peer_id, status, error_message)
            .await?;

        // Emit event using helper (push-based architecture)
        self.emit_delivery_status_updated_event(message_id, peer_id, status, error_message)
            .await?;

        Ok(())
    }

    /// Get message by ID
    pub async fn get_message(&self, message_id: &MessageId) -> Result<Option<P2PMessage>> {
        self.implementation.get_message(message_id).await
    }

    /// Get messages with filtering
    pub async fn get_messages_filtered(&self, filter: &MessageFilter) -> Result<Vec<P2PMessage>> {
        self.implementation.get_messages_filtered(filter).await
    }

    /// Get message history for a peer
    pub async fn get_message_history(
        &self,
        peer_id: &PeerId,
        limit: Option<usize>,
    ) -> Result<Vec<StoredMessage>> {
        let messages = self
            .implementation
            .get_messages_by_peer(peer_id, limit.map(|l| l as u32))
            .await?;
        Self::convert_stored_messages_to_stored_api(messages, peer_id)
    }

    /// Search messages using full-text search
    pub async fn search_messages(
        &self,
        query: &str,
        limit: Option<u32>,
    ) -> Result<Vec<P2PMessage>> {
        self.implementation.search_messages(query, limit).await
    }

    /// Get delivery status for message
    pub async fn get_delivery_status(
        &self,
        message_id: &MessageId,
    ) -> Result<Vec<(PeerId, DeliveryStatus, TransportMethod)>> {
        self.implementation.get_delivery_status(message_id).await
    }

    /// Delete message and all related records
    pub async fn delete_message(&self, message_id: &MessageId) -> Result<bool> {
        let deleted = self.core.delete_message(message_id).await?;

        if deleted {
            // Emit event using helper (push-based architecture)
            self.emit_message_deleted_event(message_id).await?;
        }

        Ok(deleted)
    }

    /// Get message statistics
    pub async fn get_statistics(&self) -> Result<MessageStats> {
        self.implementation.get_statistics().await
    }
}
