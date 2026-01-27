use anyhow::{Context, Result};
use libp2p::PeerId;
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use std::sync::Arc;

use super::queries_delivery_helpers::DeliveryQueryHelpers;
use crate::p2p::message::routing::{DeliveryStatus, TransportMethod};
use crate::p2p::message::types::MessageId;

/// Delivery status query operations (Task 3.5 Priority 3)
#[derive(Clone)]
pub struct DeliveryQueries {
    pool: Arc<Pool<SqliteConnectionManager>>,
}

/// Delivery status information
#[derive(Debug, Clone)]
pub struct DeliveryInfo {
    pub message_id: MessageId,
    pub peer_id: PeerId,
    pub status: DeliveryStatus,
    pub transport_method: TransportMethod,
    pub attempt_count: u32,
    pub last_attempt_at: Option<i64>,
    pub next_retry_at: Option<i64>,
    pub error_message: Option<String>,
    pub created_at: i64,
    pub updated_at: i64,
}

impl DeliveryQueries {
    /// Create new delivery queries handler
    pub fn new(pool: Arc<Pool<SqliteConnectionManager>>) -> Self {
        Self { pool }
    }

    /// Get delivery status for a message
    pub async fn get_message_delivery_status(
        &self,
        message_id: &MessageId,
    ) -> Result<Vec<DeliveryInfo>> {
        let pool = self.pool.clone();
        let message_id_str = message_id.to_string();

        tokio::task::spawn_blocking(move || {
            DeliveryQueryHelpers::query_delivery_status(&pool, &message_id_str)
        })
        .await
        .context("Task join error")?
    }

    /// Get pending deliveries (for retry processing)
    pub async fn get_pending_deliveries(&self, limit: Option<u32>) -> Result<Vec<DeliveryInfo>> {
        let pool = self.pool.clone();
        let limit = limit.unwrap_or(100);

        tokio::task::spawn_blocking(move || {
            DeliveryQueryHelpers::query_pending_deliveries(&pool, limit)
        })
        .await
        .context("Task join error")?
    }

    /// Get failed deliveries for analysis
    pub async fn get_failed_deliveries(&self, limit: Option<u32>) -> Result<Vec<DeliveryInfo>> {
        let pool = self.pool.clone();
        let limit = limit.unwrap_or(100);

        tokio::task::spawn_blocking(move || {
            DeliveryQueryHelpers::query_failed_deliveries(&pool, limit)
        })
        .await
        .context("Task join error")?
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_delivery_queries_creation() {
        let manager = SqliteConnectionManager::memory();
        let pool = Pool::new(manager).unwrap();
        let queries = DeliveryQueries::new(Arc::new(pool));
        // Queries created successfully
    }
}
