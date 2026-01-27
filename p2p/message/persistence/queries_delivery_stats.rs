#[path = "queries_delivery_stats_helpers.rs"]
mod queries_delivery_stats_helpers;

use anyhow::{Context, Result};
use queries_delivery_stats_helpers::{
    build_delivery_statistics, execute_period_status_queries, execute_status_queries,
};
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use std::sync::Arc;

/// Delivery statistics query operations (Task 3.5 Priority 3)
#[derive(Clone)]
pub struct DeliveryStatisticsQueries {
    pool: Arc<Pool<SqliteConnectionManager>>,
}

/// Delivery statistics
#[derive(Debug, Clone)]
pub struct DeliveryStatistics {
    pub pending: u32,
    pub sent: u32,
    pub delivered: u32,
    pub failed: u32,
    pub timeout: u32,
    pub total: u32,
}

impl DeliveryStatisticsQueries {
    /// Create new delivery statistics queries handler
    pub fn new(pool: Arc<Pool<SqliteConnectionManager>>) -> Self {
        Self { pool }
    }

    /// Get delivery statistics
    pub async fn get_delivery_statistics(&self) -> Result<DeliveryStatistics> {
        let pool = self.pool.clone();

        tokio::task::spawn_blocking(move || Self::query_delivery_statistics(&pool))
            .await
            .context("Task join error")?
    }

    /// Get delivery statistics for a specific time range
    pub async fn get_delivery_statistics_for_period(
        &self,
        start_timestamp: i64,
        end_timestamp: i64,
    ) -> Result<DeliveryStatistics> {
        let pool = self.pool.clone();

        tokio::task::spawn_blocking(move || {
            Self::query_delivery_statistics_for_period(&pool, start_timestamp, end_timestamp)
        })
        .await
        .context("Task join error")?
    }

    /// Query delivery statistics
    fn query_delivery_statistics(
        pool: &Pool<SqliteConnectionManager>,
    ) -> Result<DeliveryStatistics> {
        let conn = pool.get().context("Failed to get database connection")?;

        let (pending, sent, delivered, failed, timeout) = execute_status_queries(&conn)?;

        Ok(build_delivery_statistics(
            pending, sent, delivered, failed, timeout,
        ))
    }

    /// Query delivery statistics for a specific time period
    fn query_delivery_statistics_for_period(
        pool: &Pool<SqliteConnectionManager>,
        start_timestamp: i64,
        end_timestamp: i64,
    ) -> Result<DeliveryStatistics> {
        let conn = pool.get().context("Failed to get database connection")?;

        let (pending, sent, delivered, failed, timeout) =
            execute_period_status_queries(&conn, start_timestamp, end_timestamp)?;

        Ok(build_delivery_statistics(
            pending, sent, delivered, failed, timeout,
        ))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use r2d2_sqlite::SqliteConnectionManager;

    #[tokio::test]
    async fn test_delivery_statistics_queries_creation() {
        let manager = SqliteConnectionManager::memory();
        let pool = Pool::new(manager).unwrap();
        let queries = DeliveryStatisticsQueries::new(Arc::new(pool));
        // Queries created successfully
    }
}
