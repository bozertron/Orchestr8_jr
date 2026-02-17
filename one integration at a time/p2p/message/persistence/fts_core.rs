use anyhow::{Context, Result};
use rusqlite::Connection;

/// FTS5 configuration information
#[derive(Debug, Clone)]
pub struct FTSConfig {
    pub table_definition: String,
    pub trigger_count: u32,
    pub is_fts5: bool,
}

/// Core FTS5 implementation for table and trigger creation
pub struct FTSCoreImpl;

impl FTSCoreImpl {
    /// Create new FTS core implementation
    pub fn new() -> Self {
        Self
    }

    /// Create FTS5 virtual table for message content search
    pub fn create_fts_table(&self, conn: &Connection) -> Result<()> {
        conn.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS p2p_messages_fts USING fts5(
                message_id UNINDEXED,
                content,
                metadata,
                content='p2p_messages',
                content_rowid='rowid'
            )",
            [],
        )
        .context("Failed to create FTS5 table for messages")?;
        Ok(())
    }

    /// Create FTS5 synchronization triggers
    pub fn create_fts_triggers(&self, conn: &Connection) -> Result<()> {
        self.create_fts_insert_trigger(conn)?;
        self.create_fts_delete_trigger(conn)?;
        self.create_fts_update_trigger(conn)?;
        Ok(())
    }

    /// Create complete FTS5 setup (table + triggers)
    pub fn create_fts_complete(&self, conn: &Connection) -> Result<()> {
        self.create_fts_table(conn)?;
        self.create_fts_triggers(conn)?;
        Ok(())
    }

    /// Create FTS5 insert trigger
    fn create_fts_insert_trigger(&self, conn: &Connection) -> Result<()> {
        conn.execute(
            "CREATE TRIGGER IF NOT EXISTS p2p_messages_fts_insert AFTER INSERT ON p2p_messages
            BEGIN
                INSERT INTO p2p_messages_fts(rowid, message_id, content, metadata)
                VALUES (new.rowid, new.id, new.content, new.metadata);
            END",
            [],
        )
        .context("Failed to create FTS5 insert trigger")?;
        Ok(())
    }

    /// Create FTS5 delete trigger
    fn create_fts_delete_trigger(&self, conn: &Connection) -> Result<()> {
        conn.execute(
            "CREATE TRIGGER IF NOT EXISTS p2p_messages_fts_delete AFTER DELETE ON p2p_messages
            BEGIN
                INSERT INTO p2p_messages_fts(p2p_messages_fts, rowid, message_id, content, metadata)
                VALUES ('delete', old.rowid, old.id, old.content, old.metadata);
            END",
            [],
        )
        .context("Failed to create FTS5 delete trigger")?;
        Ok(())
    }

    /// Create FTS5 update trigger
    fn create_fts_update_trigger(&self, conn: &Connection) -> Result<()> {
        conn.execute(
            "CREATE TRIGGER IF NOT EXISTS p2p_messages_fts_update AFTER UPDATE ON p2p_messages
            BEGIN
                INSERT INTO p2p_messages_fts(p2p_messages_fts, rowid, message_id, content, metadata)
                VALUES ('delete', old.rowid, old.id, old.content, old.metadata);
                INSERT INTO p2p_messages_fts(rowid, message_id, content, metadata)
                VALUES (new.rowid, new.id, new.content, new.metadata);
            END",
            [],
        )
        .context("Failed to create FTS5 update trigger")?;
        Ok(())
    }

    /// Drop FTS5 table and triggers
    pub fn drop_fts_complete(&self, conn: &Connection) -> Result<()> {
        // Drop triggers first
        conn.execute("DROP TRIGGER IF EXISTS p2p_messages_fts_insert", [])
            .context("Failed to drop FTS5 insert trigger")?;
        conn.execute("DROP TRIGGER IF EXISTS p2p_messages_fts_delete", [])
            .context("Failed to drop FTS5 delete trigger")?;
        conn.execute("DROP TRIGGER IF EXISTS p2p_messages_fts_update", [])
            .context("Failed to drop FTS5 update trigger")?;

        // Drop FTS table
        conn.execute("DROP TABLE IF EXISTS p2p_messages_fts", [])
            .context("Failed to drop FTS5 table")?;

        Ok(())
    }

    /// Check if FTS5 table exists
    pub fn fts_table_exists(&self, conn: &Connection) -> Result<bool> {
        let exists: i32 = conn.query_row(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name = 'p2p_messages_fts'",
            [],
            |row| row.get(0),
        ).context("Failed to check FTS5 table existence")?;

        Ok(exists > 0)
    }

    /// Check if FTS5 triggers exist
    pub fn fts_triggers_exist(&self, conn: &Connection) -> Result<bool> {
        let trigger_count: i32 = conn.query_row(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger' AND name LIKE 'p2p_messages_fts_%'",
            [],
            |row| row.get(0),
        ).context("Failed to check FTS5 triggers existence")?;

        Ok(trigger_count == 3) // Should have exactly 3 triggers
    }

    /// Validate FTS5 setup is complete and functional
    pub fn validate_fts_setup(&self, conn: &Connection) -> Result<bool> {
        let table_exists = self.fts_table_exists(conn)?;
        let triggers_exist = self.fts_triggers_exist(conn)?;
        Ok(table_exists && triggers_exist)
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    use crate::p2p::message::persistence::connection::ConnectionManager;
    use crate::p2p::message::persistence::schema_tables::TableCreator;
    use tempfile::tempdir;

    #[test]
    fn test_fts_core_creation() {
        let _core = FTSCoreImpl::new();
        // Test passes if no panic occurs during creation
    }
    #[test]
    fn test_fts_table_creation() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();
        let conn = pool.get().unwrap();
        let core = FTSCoreImpl::new();

        // Create base tables first
        TableCreator::create_messages_table(&conn).unwrap();

        // Create FTS table
        core.create_fts_table(&conn).unwrap();

        // Verify FTS table exists
        assert!(core.fts_table_exists(&conn).unwrap());
    }
    #[test]
    fn test_fts_triggers_creation() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();
        let conn = pool.get().unwrap();
        let core = FTSCoreImpl::new();

        // Create base tables and FTS table
        TableCreator::create_messages_table(&conn).unwrap();
        core.create_fts_table(&conn).unwrap();
        core.create_fts_triggers(&conn).unwrap();

        // Verify triggers exist
        assert!(core.fts_triggers_exist(&conn).unwrap());
    }
    #[test]
    fn test_fts_complete_setup() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();
        let conn = pool.get().unwrap();
        let core = FTSCoreImpl::new();

        // Create base tables first
        TableCreator::create_messages_table(&conn).unwrap();

        // Create complete FTS setup
        core.create_fts_complete(&conn).unwrap();

        // Validate complete setup
        assert!(core.validate_fts_setup(&conn).unwrap());
    }
}
