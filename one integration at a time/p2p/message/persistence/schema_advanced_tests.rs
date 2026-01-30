#[cfg(test)]
mod tests {
    use super::super::*;
    use tempfile::tempdir;
    use crate::p2p::message::persistence::connection::ConnectionManager;

    #[test]
    fn test_drop_all_tables() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();

        SchemaManager::initialize_schema(&pool).unwrap();

        let conn = pool.get().unwrap();

        // Verify tables exist before dropping
        let table_count_before: i32 = conn.query_row(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name LIKE 'p2p_%'",
            [],
            |row| row.get(0),
        ).unwrap();

        assert!(table_count_before > 0);

        // Drop all tables
        SchemaManager::drop_all_tables(&conn).unwrap();

        // Verify tables are gone
        let table_count_after: i32 = conn.query_row(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND (name LIKE 'p2p_%' OR name = 'schema_version')",
            [],
            |row| row.get(0),
        ).unwrap();

        assert_eq!(table_count_after, 0);
    }

    #[test]
    fn test_pragma_settings() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();
        SchemaManager::initialize_schema(&pool).unwrap();
        let conn = pool.get().unwrap();

        Self::verify_journal_mode(&conn);
        Self::verify_synchronous_mode(&conn);
        Self::verify_foreign_keys(&conn);
    }

    fn verify_journal_mode(conn: &PooledConnection<SqliteConnectionManager>) {
        let journal_mode: String = conn.query_row(
            "PRAGMA journal_mode",
            [],
            |row| row.get(0),
        ).unwrap();
        assert_eq!(journal_mode.to_uppercase(), "WAL");
    }

    fn verify_synchronous_mode(conn: &PooledConnection<SqliteConnectionManager>) {
        let synchronous: String = conn.query_row(
            "PRAGMA synchronous",
            [],
            |row| row.get(0),
        ).unwrap();
        assert_eq!(synchronous, "1"); // NORMAL = 1
    }

    fn verify_foreign_keys(conn: &PooledConnection<SqliteConnectionManager>) {
        let foreign_keys: i32 = conn.query_row(
            "PRAGMA foreign_keys",
            [],
            |row| row.get(0),
        ).unwrap();
        assert_eq!(foreign_keys, 1);
    }

    #[test]
    fn test_database_integrity() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();

        SchemaManager::initialize_schema(&pool).unwrap();

        let conn = pool.get().unwrap();

        // Run integrity check
        let integrity_result: String = conn.query_row(
            "PRAGMA integrity_check",
            [],
            |row| row.get(0),
        ).unwrap();

        assert_eq!(integrity_result, "ok", "Database integrity check should pass");
    }

    #[test]
    fn test_schema_migration_compatibility() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();

        // Initialize schema
        SchemaManager::initialize_schema(&pool).unwrap();

        let conn = pool.get().unwrap();

        // Verify schema version is tracked
        let version_exists: i32 = conn.query_row(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name = 'schema_version'",
            [],
            |row| row.get(0),
        ).unwrap();

        assert_eq!(version_exists, 1, "Schema version table should exist");

        // Verify version is correct
        let current_version: i32 = conn.query_row(
            "SELECT version FROM schema_version LIMIT 1",
            [],
            |row| row.get(0),
        ).unwrap();

        assert_eq!(current_version, CURRENT_SCHEMA_VERSION, "Schema version should match current");
    }

    #[test]
    fn test_concurrent_schema_initialization() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        
        // Create multiple connection pools to simulate concurrent access
        let pool1 = ConnectionManager::create_pool(&db_path).unwrap();
        let pool2 = ConnectionManager::create_pool(&db_path).unwrap();

        // Initialize schema from both pools (should be safe)
        SchemaManager::initialize_schema(&pool1).unwrap();
        SchemaManager::initialize_schema(&pool2).unwrap();

        let conn = pool1.get().unwrap();

        // Verify only one set of tables exists
        let table_count: i32 = conn.query_row(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name LIKE 'p2p_%'",
            [],
            |row| row.get(0),
        ).unwrap();

        assert_eq!(table_count, 4, "Should have exactly 4 P2P tables");
    }

    #[test]
    fn test_performance_indexes() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();

        SchemaManager::initialize_schema(&pool).unwrap();

        let conn = pool.get().unwrap();

        // Check for specific performance indexes
        let expected_indexes = [
            "idx_p2p_messages_timestamp",
            "idx_p2p_messages_sender",
            "idx_p2p_delivery_status_message_id",
            "idx_p2p_routing_history_message_id",
            "idx_p2p_message_events_message_id",
        ];

        for index_name in &expected_indexes {
            let index_exists: i32 = conn.query_row(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND name = ?1",
                [index_name],
                |row| row.get(0),
            ).unwrap();

            assert_eq!(index_exists, 1, "Index {} should exist", index_name);
        }
    }




}
