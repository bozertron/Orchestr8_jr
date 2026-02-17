#[cfg(test)]
mod tests {
    use super::super::*;
    use tempfile::tempdir;
    use crate::p2p::message::persistence::connection::ConnectionManager;

    #[test]
    fn test_schema_initialization() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();

        SchemaManager::initialize_schema(&pool).unwrap();

        // Verify tables exist
        let conn = pool.get().unwrap();
        let table_count: i32 = conn.query_row(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name LIKE 'p2p_%'",
            [],
            |row| row.get(0),
        ).unwrap();

        assert_eq!(table_count, 4); // 4 main tables + FTS table
    }

    #[test]
    fn test_schema_version_tracking() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();

        SchemaManager::initialize_schema(&pool).unwrap();

        let conn = pool.get().unwrap();
        let version: i32 = conn.query_row(
            "SELECT version FROM schema_version LIMIT 1",
            [],
            |row| row.get(0),
        ).unwrap();

        assert_eq!(version, CURRENT_SCHEMA_VERSION);
    }

    #[test]
    fn test_table_creation() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();

        SchemaManager::initialize_schema(&pool).unwrap();

        let conn = pool.get().unwrap();

        // Check specific tables exist
        let tables = [
            "p2p_messages",
            "p2p_delivery_status", 
            "p2p_routing_history",
            "p2p_message_events",
            "p2p_messages_fts",
        ];

        for table in &tables {
            let exists: i32 = conn.query_row(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name = ?1",
                [table],
                |row| row.get(0),
            ).unwrap();
            
            assert_eq!(exists, 1, "Table {} should exist", table);
        }
    }

    #[test]
    fn test_index_creation() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();

        SchemaManager::initialize_schema(&pool).unwrap();

        let conn = pool.get().unwrap();

        // Check that indexes were created
        let index_count: i32 = conn.query_row(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'",
            [],
            |row| row.get(0),
        ).unwrap();

        assert!(index_count > 0, "Should have created performance indexes");
    }

    #[test]
    fn test_foreign_key_constraints() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();

        SchemaManager::initialize_schema(&pool).unwrap();

        let conn = pool.get().unwrap();

        // Check foreign key constraints are enabled
        let fk_enabled: i32 = conn.query_row(
            "PRAGMA foreign_keys",
            [],
            |row| row.get(0),
        ).unwrap();

        assert_eq!(fk_enabled, 1, "Foreign keys should be enabled");
    }

    #[test]
    fn test_schema_idempotency() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();

        // Initialize schema twice
        SchemaManager::initialize_schema(&pool).unwrap();
        SchemaManager::initialize_schema(&pool).unwrap();

        let conn = pool.get().unwrap();

        // Should still have correct number of tables
        let table_count: i32 = conn.query_row(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name LIKE 'p2p_%'",
            [],
            |row| row.get(0),
        ).unwrap();

        assert_eq!(table_count, 4); // Should not duplicate tables

        // Version should still be correct
        let version: i32 = conn.query_row(
            "SELECT version FROM schema_version LIMIT 1",
            [],
            |row| row.get(0),
        ).unwrap();

        assert_eq!(version, CURRENT_SCHEMA_VERSION);
    }
}
