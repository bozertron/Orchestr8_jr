#[cfg(test)]
mod tests {
    use super::super::*;
    use tempfile::tempdir;
    use crate::p2p::message::persistence::connection::ConnectionManager;

    #[test]
    fn test_fts_table_creation() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();

        SchemaManager::initialize_schema(&pool).unwrap();

        let conn = pool.get().unwrap();

        // Check FTS5 table exists
        let fts_exists: i32 = conn.query_row(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name = 'p2p_messages_fts'",
            [],
            |row| row.get(0),
        ).unwrap();

        assert_eq!(fts_exists, 1, "FTS5 table should exist");

        // Check FTS5 triggers exist
        let trigger_count: i32 = conn.query_row(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger' AND name LIKE 'p2p_messages_fts_%'",
            [],
            |row| row.get(0),
        ).unwrap();

        assert_eq!(trigger_count, 3, "Should have 3 FTS5 triggers (insert, update, delete)");
    }

    #[test]
    fn test_table_structure() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();
        SchemaManager::initialize_schema(&pool).unwrap();
        let conn = pool.get().unwrap();

        Self::verify_messages_table_structure(&conn);
    }

    fn verify_messages_table_structure(conn: &PooledConnection<SqliteConnectionManager>) {
        let column_names = Self::get_table_columns(conn, "p2p_messages");
        let expected_columns = [
            "id", "message_type", "content", "sender_id", "recipient_id",
            "timestamp", "signature", "encryption_key_id", "content_hash",
            "metadata", "created_at", "updated_at"
        ];

        for expected_col in &expected_columns {
            assert!(
                column_names.contains(&expected_col.to_string()),
                "Column {} should exist in p2p_messages table",
                expected_col
            );
        }
    }

    fn get_table_columns(conn: &PooledConnection<SqliteConnectionManager>, table_name: &str) -> Vec<String> {
        let mut stmt = conn.prepare(&format!("PRAGMA table_info({})", table_name)).unwrap();
        stmt.query_map([], |row| {
            Ok(row.get::<_, String>(1)?) // Column name is at index 1
        }).unwrap().collect::<Result<Vec<_>, _>>().unwrap()
    }

    #[test]
    fn test_delivery_status_table_structure() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();
        SchemaManager::initialize_schema(&pool).unwrap();
        let conn = pool.get().unwrap();

        Self::verify_delivery_status_table_structure(&conn);
    }

    fn verify_delivery_status_table_structure(conn: &PooledConnection<SqliteConnectionManager>) {
        let column_names = Self::get_table_columns(conn, "p2p_delivery_status");
        let expected_columns = [
            "id", "message_id", "peer_id", "status", "transport_method",
            "error_message", "retry_count", "last_attempt", "created_at", "updated_at"
        ];

        for expected_col in &expected_columns {
            assert!(
                column_names.contains(&expected_col.to_string()),
                "Column {} should exist in p2p_delivery_status table",
                expected_col
            );
        }
    }

    #[test]
    fn test_routing_history_table_structure() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();
        SchemaManager::initialize_schema(&pool).unwrap();
        let conn = pool.get().unwrap();

        Self::verify_routing_history_table_structure(&conn);
    }

    fn verify_routing_history_table_structure(conn: &PooledConnection<SqliteConnectionManager>) {
        let column_names = Self::get_table_columns(conn, "p2p_routing_history");
        let expected_columns = [
            "id", "message_id", "hop_peer_id", "hop_timestamp", "transport_method",
            "latency_ms", "success", "error_details", "created_at"
        ];

        for expected_col in &expected_columns {
            assert!(
                column_names.contains(&expected_col.to_string()),
                "Column {} should exist in p2p_routing_history table",
                expected_col
            );
        }
    }

    #[test]
    fn test_message_events_table_structure() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();
        SchemaManager::initialize_schema(&pool).unwrap();
        let conn = pool.get().unwrap();

        Self::verify_message_events_table_structure(&conn);
    }

    fn verify_message_events_table_structure(conn: &PooledConnection<SqliteConnectionManager>) {
        let column_names = Self::get_table_columns(conn, "p2p_message_events");
        let expected_columns = [
            "id", "message_id", "event_type", "event_data", "peer_id",
            "timestamp", "processed", "created_at", "updated_at"
        ];

        for expected_col in &expected_columns {
            assert!(
                column_names.contains(&expected_col.to_string()),
                "Column {} should exist in p2p_message_events table",
                expected_col
            );
        }
    }

    #[test]
    fn test_primary_key_constraints() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();

        SchemaManager::initialize_schema(&pool).unwrap();

        let conn = pool.get().unwrap();

        // Check that each table has a primary key
        let tables = ["p2p_messages", "p2p_delivery_status", "p2p_routing_history", "p2p_message_events"];

        for table in &tables {
            let pk_count: i32 = conn.query_row(
                "SELECT COUNT(*) FROM pragma_table_info(?1) WHERE pk > 0",
                [table],
                |row| row.get(0),
            ).unwrap();

            assert!(pk_count > 0, "Table {} should have a primary key", table);
        }
    }
}
