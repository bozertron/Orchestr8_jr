use anyhow::Result;
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use std::sync::Arc;

/// Event processing functionality for maintenance operations
#[derive(Clone)]
pub struct MaintenanceEventProcessing;

impl MaintenanceEventProcessing {
    /// Mark events as processed
    pub async fn mark_events_processed(
        connection_pool: Arc<Pool<SqliteConnectionManager>>,
        message_ids: &[crate::p2p::message::types::MessageId],
    ) -> Result<()> {
        if message_ids.is_empty() {
            return Ok(());
        }
        let pool = connection_pool.clone();
        let message_id_strings = message_ids
            .iter()
            .map(|id| id.to_string())
            .collect::<Vec<_>>();
        let result = tokio::task::spawn_blocking(move || {
            Self::execute_mark_processed_query(pool, message_id_strings)
        })
        .await
        .map_err(|e| anyhow::anyhow!("Task join error: {}", e))??;
        Ok(result)
    }

    /// Execute mark processed query
    fn execute_mark_processed_query(
        pool: Arc<Pool<SqliteConnectionManager>>,
        message_id_strings: Vec<String>,
    ) -> Result<()> {
        use chrono;
        let conn = pool
            .get()
            .map_err(|e| anyhow::anyhow!("Failed to get database connection: {}", e))?;
        let placeholders = message_id_strings
            .iter()
            .map(|_| "?")
            .collect::<Vec<_>>()
            .join(",");
        let query = format!("UPDATE p2p_message_events SET processed = TRUE, updated_at = ?1 WHERE message_id IN ({})", placeholders);
        let mut params = vec![chrono::Utc::now().timestamp().to_string()];
        params.extend(message_id_strings);
        conn.execute(&query, rusqlite::params_from_iter(params))
            .map_err(|e| anyhow::anyhow!("Failed to mark events as processed: {}", e))?;
        Ok(())
    }
}
