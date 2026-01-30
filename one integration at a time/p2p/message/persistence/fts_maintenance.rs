use anyhow::{Context, Result};
use rusqlite::Connection;

use super::fts_core::FTSConfig;

/// FTS5 index statistics
#[derive(Debug, Clone)]
pub struct FTSStats {
    pub total_documents: u64,
    pub index_size_bytes: u64,
}

/// FTS5 performance metrics
#[derive(Debug, Clone)]
pub struct PerformanceMetrics {
    pub total_documents: u64,
    pub index_size_bytes: u64,
    pub avg_query_time_ms: u64,
}

impl FTSStats {
    /// Create new FTS statistics
    pub fn new(total_documents: u64, index_size_bytes: u64) -> Self {
        Self {
            total_documents,
            index_size_bytes,
        }
    }

    /// Get index size in MB
    pub fn index_size_mb(&self) -> f64 {
        self.index_size_bytes as f64 / (1024.0 * 1024.0)
    }

    /// Check if index needs optimization
    pub fn needs_optimization(&self) -> bool {
        self.index_size_mb() > 10.0 || self.total_documents > 10000
    }
}

/// FTS5 maintenance implementation for optimization and statistics
pub struct FTSMaintenanceImpl;

impl FTSMaintenanceImpl {
    /// Create new FTS maintenance implementation
    pub fn new() -> Self {
        Self
    }

    /// Rebuild FTS5 index (maintenance operation)
    pub fn rebuild_fts_index(&self, conn: &Connection) -> Result<()> {
        conn.execute(
            "INSERT INTO p2p_messages_fts(p2p_messages_fts) VALUES('rebuild')",
            [],
        )
        .context("Failed to rebuild FTS5 index")?;
        Ok(())
    }

    /// Optimize FTS5 index (maintenance operation)
    pub fn optimize_fts_index(&self, conn: &Connection) -> Result<()> {
        conn.execute(
            "INSERT INTO p2p_messages_fts(p2p_messages_fts) VALUES('optimize')",
            [],
        )
        .context("Failed to optimize FTS5 index")?;
        Ok(())
    }

    /// Get FTS5 index statistics
    pub fn get_fts_stats(&self, conn: &Connection) -> Result<FTSStats> {
        let total_docs: i64 = conn
            .query_row("SELECT COUNT(*) FROM p2p_messages_fts", [], |row| {
                row.get(0)
            })
            .context("Failed to get FTS document count")?;

        let index_size: i64 = conn
            .query_row(
                "SELECT page_count * page_size FROM pragma_page_count(), pragma_page_size()",
                [],
                |row| row.get(0),
            )
            .unwrap_or(0);

        Ok(FTSStats::new(total_docs as u64, index_size as u64))
    }

    /// Perform complete FTS5 maintenance
    pub fn perform_maintenance(&self, conn: &Connection) -> Result<MaintenanceResult> {
        let stats_before = self.get_fts_stats(conn)?;

        // Optimize the index
        self.optimize_fts_index(conn)?;

        let stats_after = self.get_fts_stats(conn)?;

        Ok(MaintenanceResult {
            documents_processed: stats_before.total_documents,
            size_before_bytes: stats_before.index_size_bytes,
            size_after_bytes: stats_after.index_size_bytes,
            optimization_performed: true,
        })
    }

    /// Check FTS5 index integrity
    pub fn check_fts_integrity(&self, conn: &Connection) -> Result<bool> {
        // Run FTS5 integrity check
        let result: String = conn
            .query_row(
                "INSERT INTO p2p_messages_fts(p2p_messages_fts) VALUES('integrity-check')",
                [],
                |_row| Ok("ok".to_string()),
            )
            .unwrap_or_else(|_| "error".to_string());

        Ok(result == "ok")
    }

    /// Get detailed FTS5 configuration
    pub fn get_fts_config(&self, conn: &Connection) -> Result<FTSConfig> {
        // Get FTS5 table configuration
        let table_sql: String = conn
            .query_row(
                "SELECT sql FROM sqlite_master WHERE type='table' AND name = 'p2p_messages_fts'",
                [],
                |row| row.get(0),
            )
            .context("Failed to get FTS5 table configuration")?;

        // Count triggers
        let trigger_count: i32 = conn.query_row(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger' AND name LIKE 'p2p_messages_fts_%'",
            [],
            |row| row.get(0),
        ).context("Failed to count FTS5 triggers")?;

        Ok(FTSConfig {
            table_definition: table_sql.clone(),
            trigger_count: trigger_count as u32,
            is_fts5: table_sql.contains("fts5"),
        })
    }

    /// Vacuum FTS5 index to reclaim space
    pub fn vacuum_fts_index(&self, conn: &Connection) -> Result<()> {
        // FTS5 doesn't have a direct vacuum command, but we can rebuild
        self.rebuild_fts_index(conn)
    }

    /// Get FTS5 performance metrics
    pub fn get_performance_metrics(&self, conn: &Connection) -> Result<PerformanceMetrics> {
        let stats = self.get_fts_stats(conn)?;

        // Measure simple query performance
        let start_time = std::time::Instant::now();
        let _: i32 = conn
            .query_row(
                "SELECT COUNT(*) FROM p2p_messages_fts WHERE p2p_messages_fts MATCH 'test'",
                [],
                |row| row.get(0),
            )
            .unwrap_or(0);
        let query_duration = start_time.elapsed();

        Ok(PerformanceMetrics {
            total_documents: stats.total_documents,
            index_size_bytes: stats.index_size_bytes,
            avg_query_time_ms: query_duration.as_millis() as u64,
        })
    }
}

/// FTS5 maintenance operation result
#[derive(Debug, Clone)]
pub struct MaintenanceResult {
    pub documents_processed: u64,
    pub size_before_bytes: u64,
    pub size_after_bytes: u64,
    pub optimization_performed: bool,
}

impl MaintenanceResult {
    /// Get space saved in bytes
    pub fn space_saved_bytes(&self) -> i64 {
        self.size_before_bytes as i64 - self.size_after_bytes as i64
    }

    /// Get space saved in MB
    pub fn space_saved_mb(&self) -> f64 {
        self.space_saved_bytes() as f64 / (1024.0 * 1024.0)
    }

    /// Check if maintenance was beneficial
    pub fn was_beneficial(&self) -> bool {
        self.space_saved_bytes() > 0 || self.optimization_performed
    }
}
