use anyhow::Result;
use libp2p::PeerId;
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use std::sync::Arc;

use crate::p2p::message::routing::{DeliveryStatus, TransportMethod};
use crate::p2p::message::types::*;

// Import modular components
use super::queries_analytics::AnalyticsQueries;
use super::queries_basic::BasicQueries;
use super::queries_search::SearchQueries;

// Re-export public types for API compatibility
pub use super::queries_analytics::MessageStats;
pub use super::queries_helpers::MessageFilter;

/// Complex queries and search operations for P2P messages
#[derive(Clone)]
pub struct PersistenceQueries {
    basic: BasicQueries,
    search: SearchQueries,
    analytics: AnalyticsQueries,
}

impl PersistenceQueries {
    /// Create new queries handler with connection pool
    pub fn new(pool: Arc<Pool<SqliteConnectionManager>>) -> Self {
        Self {
            basic: BasicQueries::new(pool.clone()),
            search: SearchQueries::new(pool.clone()),
            analytics: AnalyticsQueries::new(pool),
        }
    }

    /// Get message by ID with full details
    pub async fn get_message_by_id(&self, message_id: &MessageId) -> Result<Option<P2PMessage>> {
        let stored_message = self.basic.get_message_by_id(message_id).await?;
        Ok(stored_message.map(|sm| sm.message))
    }

    /// Get messages with filtering and pagination
    pub async fn get_messages_filtered(&self, filter: &MessageFilter) -> Result<Vec<P2PMessage>> {
        self.basic.get_messages_filtered(filter).await
    }

    /// Full-text search in message content using FTS5
    pub async fn search_messages(
        &self,
        search_query: &str,
        limit: Option<u32>,
    ) -> Result<Vec<P2PMessage>> {
        self.search.search_messages(search_query, limit).await
    }

    /// Get delivery status for a message
    pub async fn get_delivery_status(
        &self,
        message_id: &MessageId,
    ) -> Result<Vec<(PeerId, DeliveryStatus, TransportMethod)>> {
        self.analytics.get_delivery_status(message_id).await
    }

    /// Get message statistics for analytics
    pub async fn get_message_statistics(&self) -> Result<MessageStats> {
        self.analytics.get_message_statistics().await
    }

    /// Get failed deliveries
    pub async fn get_failed_deliveries(&self) -> Result<Vec<(MessageId, PeerId, String)>> {
        // Placeholder implementation - would query delivery_status table for failed entries
        Ok(Vec::new())
    }

    /// Get pending deliveries
    pub async fn get_pending_deliveries(
        &self,
    ) -> Result<Vec<(MessageId, PeerId, TransportMethod)>> {
        // Placeholder implementation - would query delivery_status table for pending entries
        Ok(Vec::new())
    }

    /// Get message count by peer
    pub async fn get_message_count_by_peer(&self, _peer_id: &PeerId) -> Result<u64> {
        // Placeholder implementation - would count messages for specific peer
        Ok(0)
    }

    /// Get failed delivery count by peer
    pub async fn get_failed_delivery_count_by_peer(&self, _peer_id: &PeerId) -> Result<u64> {
        // Placeholder implementation - would count failed deliveries for specific peer
        Ok(0)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::p2p::message::persistence::{ConnectionManager, SchemaManager};
    use std::sync::Arc;
    use tempfile::tempdir;

    #[tokio::test]
    async fn test_message_search() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = Arc::new(ConnectionManager::create_pool(&db_path).unwrap());

        SchemaManager::initialize_schema(&pool).unwrap();
        let queries = PersistenceQueries::new(pool);

        let results = queries.search_messages("test", Some(10)).await.unwrap();
        assert!(results.is_empty()); // No messages inserted yet
    }
}
