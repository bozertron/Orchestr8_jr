use anyhow::Result;
use rusqlite::Connection;

// Import modular FTS components
use super::fts_core::FTSCoreImpl;
use super::fts_maintenance::FTSMaintenanceImpl;

// Re-export public types for API compatibility
pub use super::fts_maintenance::FTSStats;

/// FTS5 (Full-Text Search) utilities for P2P message persistence schema
pub struct FTSCreator {
    core: FTSCoreImpl,
    maintenance: FTSMaintenanceImpl,
}

impl Default for FTSCreator {
    fn default() -> Self {
        Self::new()
    }
}

impl FTSCreator {
    /// Create new FTS creator
    pub fn new() -> Self {
        Self {
            core: FTSCoreImpl::new(),
            maintenance: FTSMaintenanceImpl::new(),
        }
    }

    /// Create FTS5 virtual table for message content search
    pub fn create_fts_table(&self, conn: &Connection) -> Result<()> {
        self.core.create_fts_table(conn)
    }

    /// Create FTS5 synchronization triggers
    pub fn create_fts_triggers(&self, conn: &Connection) -> Result<()> {
        self.core.create_fts_triggers(conn)
    }

    /// Create complete FTS5 setup (table + triggers)
    pub fn create_fts_complete(&self, conn: &Connection) -> Result<()> {
        self.core.create_fts_complete(conn)
    }

    /// Rebuild FTS5 index (maintenance operation)
    pub fn rebuild_fts_index(&self, conn: &Connection) -> Result<()> {
        self.maintenance.rebuild_fts_index(conn)
    }

    /// Optimize FTS5 index (maintenance operation)
    pub fn optimize_fts_index(&self, conn: &Connection) -> Result<()> {
        self.maintenance.optimize_fts_index(conn)
    }

    /// Get FTS5 index statistics
    pub fn get_fts_stats(&self, conn: &Connection) -> Result<FTSStats> {
        self.maintenance.get_fts_stats(conn)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::p2p::message::persistence::connection::ConnectionManager;
    use crate::p2p::message::persistence::schema_tables::TableCreator;
    use tempfile::tempdir;

    #[test]
    fn test_fts_creator_creation() {
        let creator = FTSCreator::new();
        let default_creator = FTSCreator::default();

        // Test passes if no panic occurs during creation
        drop(creator);
        drop(default_creator);
    }

    #[test]
    fn test_fts_complete_setup() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();
        let conn = pool.get().unwrap();
        let creator = FTSCreator::new();

        // Create base tables first
        TableCreator::create_messages_table(&conn).unwrap();

        // Create complete FTS setup
        creator.create_fts_complete(&conn).unwrap();

        // Verify both table and triggers exist
        let fts_exists: i32 = conn.query_row(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name = 'p2p_messages_fts'",
            [],
            |row| row.get(0),
        ).unwrap();

        let trigger_count: i32 = conn.query_row(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger' AND name LIKE 'p2p_messages_fts_%'",
            [],
            |row| row.get(0),
        ).unwrap();

        assert_eq!(fts_exists, 1);
        assert_eq!(trigger_count, 3);
    }
}
