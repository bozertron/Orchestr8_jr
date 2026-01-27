use anyhow::{Context, Result};
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use std::sync::Arc;

use super::{ConnectionUtils, EventProcessor};

#[derive(Debug, Clone)]
pub struct MaintenanceResult {
    pub events_cleaned: u32,
    pub database_optimized: bool,
}

impl MaintenanceResult {
    pub fn new(events_cleaned: u32, database_optimized: bool) -> Self {
        Self {
            events_cleaned,
            database_optimized,
        }
    }

    pub fn is_successful(&self) -> bool {
        self.database_optimized
    }

    pub fn total_processed(&self) -> u32 {
        self.events_cleaned
    }
}

#[derive(Debug, Clone)]
pub struct PersistenceHealth {
    pub database_healthy: bool,
    pub total_connections: u32,
    pub idle_connections: u32,
    pub unprocessed_events: u64,
}

impl PersistenceHealth {
    pub fn new(
        database_healthy: bool,
        total_connections: u32,
        idle_connections: u32,
        unprocessed_events: u64,
    ) -> Self {
        Self {
            database_healthy,
            total_connections,
            idle_connections,
            unprocessed_events,
        }
    }

    pub fn is_healthy(&self) -> bool {
        self.database_healthy && self.unprocessed_events < 1000
    }

    pub fn connection_utilization(&self) -> f64 {
        if self.total_connections == 0 {
            0.0
        } else {
            ((self.total_connections - self.idle_connections) as f64
                / self.total_connections as f64)
                * 100.0
        }
    }

    pub fn is_connection_stressed(&self) -> bool {
        self.connection_utilization() > 80.0
    }
}

#[derive(Debug, Clone)]
pub struct MaintenanceStatistics {
    pub database_size_bytes: u64,
    pub total_messages: u64,
    pub total_events: u64,
    pub last_vacuum: Option<i64>,
}

impl MaintenanceStatistics {
    pub fn database_size_mb(&self) -> f64 {
        self.database_size_bytes as f64 / (1024.0 * 1024.0)
    }

    pub fn needs_maintenance(&self) -> bool {
        self.database_size_mb() > 100.0 || self.total_events > 10000
    }
}

#[derive(Clone)]
pub struct MaintenanceCoreImpl {
    connection_pool: Arc<Pool<SqliteConnectionManager>>,
    event_processor: Option<EventProcessor>,
}

impl MaintenanceCoreImpl {
    /// Create new maintenance core implementation
    pub fn new(connection_pool: Arc<Pool<SqliteConnectionManager>>) -> Self {
        Self {
            connection_pool,
            event_processor: None,
        }
    }

    /// Optional injection of event processor for richer health metrics
    pub fn with_event_processor(mut self, event_processor: EventProcessor) -> Self {
        self.event_processor = Some(event_processor);
        self
    }

    /// Cleanup old events and optimize database
    pub async fn maintenance_cleanup(&self, older_than_days: u32) -> Result<MaintenanceResult> {
        let events_cleaned = if let Some(ref ep) = self.event_processor {
            ep.cleanup_old_events(older_than_days)
                .await
                .with_context(|| {
                    "persistence.maintenance_core: ep.cleanup_old_events".to_string()
                })?
        } else {
            cleanup_old_database_records(self.connection_pool.clone(), older_than_days).await?
        };
        let database_optimized = optimize_database(self.connection_pool.clone()).await?;

        Ok(MaintenanceResult::new(events_cleaned, database_optimized))
    }

    /// Health check for persistence service
    pub async fn health_check(&self) -> Result<PersistenceHealth> {
        let pool_healthy = ConnectionUtils::health_check(&self.connection_pool)
            .with_context(|| "persistence.maintenance_core: pool health_check".to_string())?;
        let (total_connections, idle_connections) = self.pool_stats();
        let unprocessed_events = self.unprocessed_events_count().await?;
        Ok(PersistenceHealth::new(
            pool_healthy,
            total_connections,
            idle_connections,
            unprocessed_events,
        ))
    }

    fn pool_stats(&self) -> (u32, u32) {
        ConnectionUtils::get_pool_stats(&self.connection_pool)
    }

    async fn unprocessed_events_count(&self) -> Result<u64> {
        if let Some(ref ep) = self.event_processor {
            unprocessed_events_count(ep).await
        } else {
            Ok(0)
        }
    }
}

// --- Local, private helpers to keep functions ≤30 lines and preserve behavior
async fn unprocessed_events_count(ep: &EventProcessor) -> Result<u64> {
    let events = ep
        .get_unprocessed_events(Some(100))
        .await
        .with_context(|| "persistence.maintenance_core: get_unprocessed_events".to_string())?;
    Ok(events.len() as u64)
}

async fn optimize_database(pool: Arc<Pool<SqliteConnectionManager>>) -> Result<bool> {
    let result = tokio::task::spawn_blocking(move || {
        let conn = pool
            .get()
            .map_err(|e| anyhow::anyhow!("Failed to get database connection: {}", e))?;
        conn.execute("VACUUM", [])
            .map_err(|e| anyhow::anyhow!("Failed to vacuum database: {}", e))?;
        conn.execute("ANALYZE", [])
            .map_err(|e| anyhow::anyhow!("Failed to analyze database: {}", e))?;
        Ok::<bool, anyhow::Error>(true)
    })
    .await
    .map_err(|e| anyhow::anyhow!("Task join error: {}", e))??;
    Ok(result)
}

async fn cleanup_old_database_records(
    pool: Arc<Pool<SqliteConnectionManager>>,
    older_than_days: u32,
) -> Result<u32> {
    let cutoff_timestamp = chrono::Utc::now().timestamp() - (older_than_days as i64 * 24 * 60 * 60);
    let result = tokio::task::spawn_blocking(move || {
        let conn = pool
            .get()
            .map_err(|e| anyhow::anyhow!("Failed to get database connection: {}", e))?;
        let rows_deleted = conn
            .execute(
                "DELETE FROM p2p_message_events WHERE processed = TRUE AND timestamp < ?1",
                rusqlite::params![cutoff_timestamp],
            )
            .with_context(|| "persistence.maintenance_core: delete old events".to_string())?
            as u32;
        Ok::<u32, anyhow::Error>(rows_deleted)
    })
    .await
    .map_err(|e| anyhow::anyhow!("Task join error: {}", e))??;
    Ok(result)
}
