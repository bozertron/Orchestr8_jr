use anyhow::{Context, Result};
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use rusqlite::{params, Connection};
use std::sync::Arc;

use super::statistics_types::{EventStatistics, ProcessingMetrics};
/// Core statistics implementation for database queries
#[derive(Clone)]
pub struct StatisticsImplCore {
    pool: Arc<Pool<SqliteConnectionManager>>,
}

impl StatisticsImplCore {
    /// Create new statistics implementation core
    pub fn new(pool: Arc<Pool<SqliteConnectionManager>>) -> Self {
        Self { pool }
    }

    /// Get event statistics for monitoring
    pub async fn get_event_statistics(&self) -> Result<EventStatistics> {
        let pool = self.pool.clone();

        let result = tokio::task::spawn_blocking(move || Self::calculate_event_statistics(pool))
            .await
            .context("Task join error")?;

        result
    }

    /// Calculate event statistics from database
    fn calculate_event_statistics(
        pool: Arc<Pool<SqliteConnectionManager>>,
    ) -> Result<EventStatistics> {
        let conn = pool.get().context("Failed to get database connection")?;

        let total_events = Self::get_total_event_count(&conn)?;
        let unprocessed_events = Self::get_unprocessed_event_count(&conn)?;
        let events_last_hour = Self::get_recent_event_count(&conn)?;

        Ok(EventStatistics::new(
            total_events,
            unprocessed_events,
            events_last_hour,
        ))
    }

    /// Get total event count
    fn get_total_event_count(conn: &Connection) -> Result<u64> {
        conn.query_row("SELECT COUNT(*) FROM p2p_message_events", [], |row| {
            row.get(0)
        })
        .context("Failed to get total event count")
    }

    /// Get unprocessed event count
    fn get_unprocessed_event_count(conn: &Connection) -> Result<u64> {
        conn.query_row(
            "SELECT COUNT(*) FROM p2p_message_events WHERE processed = FALSE",
            [],
            |row| row.get(0),
        )
        .context("Failed to get unprocessed event count")
    }

    /// Get recent event count (last hour)
    fn get_recent_event_count(conn: &Connection) -> Result<u64> {
        conn.query_row(
            "SELECT COUNT(*) FROM p2p_message_events WHERE timestamp > ?1",
            params![chrono::Utc::now().timestamp() - 3600],
            |row| row.get(0),
        )
        .context("Failed to get recent event count")
    }

    /// Get detailed event statistics by type
    pub async fn get_event_statistics_by_type(&self) -> Result<Vec<(String, u64)>> {
        let pool = self.pool.clone();

        let result =
            tokio::task::spawn_blocking(move || Self::query_event_statistics_by_type(pool))
                .await
                .context("Task join error")?;

        result
    }

    /// Query event statistics by type from database
    fn query_event_statistics_by_type(
        pool: Arc<Pool<SqliteConnectionManager>>,
    ) -> Result<Vec<(String, u64)>> {
        let conn = pool.get().context("Failed to get database connection")?;

        let mut stmt = conn
            .prepare(
                "SELECT event_type, COUNT(*) as count
             FROM p2p_message_events
             GROUP BY event_type
             ORDER BY count DESC",
            )
            .context("Failed to prepare event type statistics query")?;

        let type_iter = stmt
            .query_map([], |row| Self::map_type_statistics_row(row))
            .context("Failed to execute event type statistics query")?;

        Self::collect_type_statistics(type_iter)
    }

    /// Map type statistics row
    fn map_type_statistics_row(row: &rusqlite::Row) -> rusqlite::Result<(String, u64)> {
        let event_type: String = row.get(0)?;
        let count: u64 = row.get(1)?;
        Ok((event_type, count))
    }

    /// Collect type statistics results
    fn collect_type_statistics<F>(type_iter: rusqlite::MappedRows<F>) -> Result<Vec<(String, u64)>>
    where
        F: FnMut(&rusqlite::Row) -> rusqlite::Result<(String, u64)>,
    {
        let mut statistics = Vec::new();
        for stat_result in type_iter {
            statistics.push(stat_result?);
        }
        Ok(statistics)
    }

    /// Get event statistics for a specific time period
    pub async fn get_event_statistics_for_period(
        &self,
        start_timestamp: i64,
        end_timestamp: i64,
    ) -> Result<EventStatistics> {
        let pool = self.pool.clone();

        let result = tokio::task::spawn_blocking(move || {
            Self::calculate_period_statistics(pool, start_timestamp, end_timestamp)
        })
        .await
        .context("Task join error")?;

        result
    }

    /// Calculate event statistics for a specific period
    fn calculate_period_statistics(
        pool: Arc<Pool<SqliteConnectionManager>>,
        start_timestamp: i64,
        end_timestamp: i64,
    ) -> Result<EventStatistics> {
        let conn = pool.get().context("Failed to get database connection")?;

        let total_events = Self::get_period_total_events(&conn, start_timestamp, end_timestamp)?;
        let unprocessed_events =
            Self::get_period_unprocessed_events(&conn, start_timestamp, end_timestamp)?;
        let events_in_period = total_events; // For period queries, this represents events in the period

        Ok(EventStatistics::new(
            total_events,
            unprocessed_events,
            events_in_period,
        ))
    }

    /// Get total events for period
    fn get_period_total_events(conn: &Connection, start: i64, end: i64) -> Result<u64> {
        conn.query_row(
            "SELECT COUNT(*) FROM p2p_message_events WHERE timestamp BETWEEN ?1 AND ?2",
            params![start, end],
            |row| row.get(0),
        )
        .context("Failed to get total event count for period")
    }

    /// Get unprocessed events for period
    fn get_period_unprocessed_events(conn: &Connection, start: i64, end: i64) -> Result<u64> {
        conn.query_row(
            "SELECT COUNT(*) FROM p2p_message_events WHERE processed = FALSE AND timestamp BETWEEN ?1 AND ?2",
            params![start, end],
            |row| row.get(0),
        ).context("Failed to get unprocessed event count for period")
    }

    /// Get processing performance metrics
    pub async fn get_processing_metrics(&self) -> Result<ProcessingMetrics> {
        let pool = self.pool.clone();

        let result = tokio::task::spawn_blocking(move || {
            let conn = pool.get().context("Failed to get database connection")?;

            let avg_processing_time: Option<f64> = conn
                .query_row(
                    "SELECT AVG(updated_at - timestamp) FROM p2p_message_events 
                 WHERE processed = TRUE AND updated_at IS NOT NULL",
                    [],
                    |row| row.get(0),
                )
                .context("Failed to get average processing time")?;

            let oldest_unprocessed: Option<i64> = conn
                .query_row(
                    "SELECT MIN(timestamp) FROM p2p_message_events 
                 WHERE processed = FALSE",
                    [],
                    |row| row.get(0),
                )
                .context("Failed to get oldest unprocessed event")?;

            Ok(ProcessingMetrics::new(
                avg_processing_time.unwrap_or(0.0),
                oldest_unprocessed,
            ))
        })
        .await
        .context("Task join error")?;

        result
    }
}
