use anyhow::Result;
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use std::sync::Arc;

// Import modular statistics components
use super::statistics_impl::StatisticsImplCore;
pub use super::statistics_types::{EventStatistics, ProcessingMetrics};

/// Event statistics implementation for performance monitoring and health checking
#[derive(Clone)]
pub struct EventStatisticsImpl {
    core: StatisticsImplCore,
}

impl EventStatisticsImpl {
    /// Create new event statistics implementation
    pub fn new(pool: Arc<Pool<SqliteConnectionManager>>) -> Self {
        Self {
            core: StatisticsImplCore::new(pool),
        }
    }

    /// Get event statistics for monitoring
    pub async fn get_event_statistics(&self) -> Result<EventStatistics> {
        self.core.get_event_statistics().await
    }

    /// Get detailed event statistics by type
    pub async fn get_event_statistics_by_type(&self) -> Result<Vec<(String, u64)>> {
        self.core.get_event_statistics_by_type().await
    }

    /// Get event statistics for a specific time period
    pub async fn get_event_statistics_for_period(
        &self,
        start_timestamp: i64,
        end_timestamp: i64,
    ) -> Result<EventStatistics> {
        self.core
            .get_event_statistics_for_period(start_timestamp, end_timestamp)
            .await
    }

    /// Get processing performance metrics
    pub async fn get_processing_metrics(&self) -> Result<ProcessingMetrics> {
        self.core.get_processing_metrics().await
    }
}
