/// Statistics functionality for maintenance operations
#[derive(Clone)]
pub struct MaintenanceStatisticsHandler {
    connection_pool: std::sync::Arc<r2d2::Pool<r2d2_sqlite::SqliteConnectionManager>>,
    event_sender: Option<tokio::sync::mpsc::UnboundedSender<crate::p2p::P2PEvent>>,
}

impl MaintenanceStatisticsHandler {
    /// Create new maintenance statistics handler
    pub fn new(
        connection_pool: std::sync::Arc<r2d2::Pool<r2d2_sqlite::SqliteConnectionManager>>,
    ) -> Self {
        Self {
            connection_pool,
            event_sender: None,
        }
    }

    /// Set event sender for emit operations
    pub fn with_event_sender(
        mut self,
        sender: tokio::sync::mpsc::UnboundedSender<crate::p2p::P2PEvent>,
    ) -> Self {
        self.event_sender = Some(sender);
        self
    }

    /// Get detailed maintenance statistics with event emission
    pub async fn get_maintenance_statistics(
        &self,
    ) -> anyhow::Result<super::maintenance_core::MaintenanceStatistics> {
        let pool = self.connection_pool.clone();
        let result =
            tokio::task::spawn_blocking(move || Self::calculate_maintenance_statistics(pool))
                .await
                .map_err(|e| anyhow::anyhow!("Task join error: {}", e))??;

        // Emit maintenance summary event
        self.emit_maintenance_summary(&result).await;
        Ok(result)
    }

    /// Get event processing statistics
    pub async fn get_event_processing_stats(
        &self,
    ) -> anyhow::Result<super::statistics_types::EventProcessingStats> {
        use super::statistics_types::EventProcessingStats;
        let pool = self.connection_pool.clone();
        tokio::task::spawn_blocking(move || {
            let conn = pool.get().map_err(|e| anyhow::anyhow!("Failed to get database connection: {}", e))?;
            let total: u64 = conn.query_row("SELECT COUNT(*) FROM p2p_message_events", [], |row| row.get(0)).unwrap_or(0);
            let processed: u64 = conn.query_row("SELECT COUNT(*) FROM p2p_message_events WHERE processed = TRUE", [], |row| row.get(0)).unwrap_or(0);
            let avg_time: Option<f64> = conn.query_row("SELECT AVG(updated_at - timestamp) FROM p2p_message_events WHERE processed = TRUE AND updated_at IS NOT NULL", [], |row| row.get(0)).unwrap_or(None);
            Ok(EventProcessingStats { total_events: total, processed_events: processed, unprocessed_events: total - processed, average_processing_time: avg_time.unwrap_or(0.0) })
        }).await.map_err(|e| anyhow::anyhow!("Task join error: {}", e))?
    }

    /// Calculate maintenance statistics from database
    fn calculate_maintenance_statistics(
        pool: std::sync::Arc<r2d2::Pool<r2d2_sqlite::SqliteConnectionManager>>,
    ) -> anyhow::Result<super::maintenance_core::MaintenanceStatistics> {
        let conn = pool
            .get()
            .map_err(|e| anyhow::anyhow!("Failed to get database connection: {}", e))?;
        let db_size = Self::get_database_size(&conn)?;
        let message_count = Self::get_message_count(&conn);
        let event_count = Self::get_event_count(&conn);
        Ok(super::maintenance_core::MaintenanceStatistics {
            database_size_bytes: db_size as u64,
            total_messages: message_count,
            total_events: event_count,
            last_vacuum: None,
        })
    }

    /// Get database size in bytes
    fn get_database_size(conn: &rusqlite::Connection) -> anyhow::Result<i64> {
        conn.query_row(
            "SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()",
            [],
            |row| row.get(0),
        )
        .map_err(|e| anyhow::anyhow!("Failed to get database size: {}", e))
    }

    /// Get total message count
    fn get_message_count(conn: &rusqlite::Connection) -> u64 {
        conn.query_row("SELECT COUNT(*) FROM p2p_messages", [], |row| row.get(0))
            .unwrap_or(0)
    }

    /// Get total event count
    fn get_event_count(conn: &rusqlite::Connection) -> u64 {
        conn.query_row("SELECT COUNT(*) FROM p2p_message_events", [], |row| {
            row.get(0)
        })
        .unwrap_or(0)
    }

    /// Emit maintenance summary event
    async fn emit_maintenance_summary(
        &self,
        stats: &super::maintenance_core::MaintenanceStatistics,
    ) {
        if let Some(sender) = &self.event_sender {
            let message = format!(
                "Database: {}MB, Messages: {}, Events: {}",
                stats.database_size_bytes / 1_000_000,
                stats.total_messages,
                stats.total_events
            );
            let event = crate::p2p::P2PEvent::MaintenanceSummary(message);
            let _ = sender.send(event);
        }
    }
}
