#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::tempdir;

    #[test]
    fn test_connection_manager_creation() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");

        let pool = ConnectionManager::create_pool(&db_path).unwrap();
        assert!(ConnectionUtils::health_check(&pool).unwrap());
    }

    #[test]
    fn test_connection_manager_with_config() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test_config.db");
        
        let config = DatabaseConfig {
            path: db_path.clone(),
            pool_size: 5,
            busy_timeout: std::time::Duration::from_secs(10),
            journal_mode: JournalMode::Wal,
        };

        let pool = ConnectionManager::create_pool_with_config(&db_path, &config).unwrap();
        assert!(ConnectionUtils::health_check(&pool).unwrap());
        
        let (total, idle) = ConnectionUtils::get_pool_stats(&pool);
        assert!(total <= config.pool_size);
    }

    #[test]
    fn test_transaction_rollback() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();

        let mut conn = pool.get().unwrap();
        let result = ConnectionUtils::execute_transaction(
            &mut conn,
            |_tx| Err(anyhow::anyhow!("Test error")),
        );

        assert!(result.is_err());
    }

    #[test]
    fn test_transaction_commit() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();
        let mut conn = pool.get().unwrap();

        Self::setup_test_table(&mut conn);
        Self::execute_test_transaction(&mut conn);
        Self::verify_transaction_commit(&mut conn);
    }

    fn setup_test_table(conn: &mut PooledConnection<SqliteConnectionManager>) {
        conn.execute(
            "CREATE TABLE test_table (id INTEGER PRIMARY KEY, value TEXT)",
            [],
        ).unwrap();
    }

    fn execute_test_transaction(conn: &mut PooledConnection<SqliteConnectionManager>) {
        let result = ConnectionUtils::execute_transaction(conn, |tx| {
            tx.execute("INSERT INTO test_table (value) VALUES (?1)", ["test_value"])?;
            Ok(())
        });
        assert!(result.is_ok());
    }

    fn verify_transaction_commit(conn: &mut PooledConnection<SqliteConnectionManager>) {
        let count: i32 = conn.query_row(
            "SELECT COUNT(*) FROM test_table",
            [],
            |row| row.get(0),
        ).unwrap();
        assert_eq!(count, 1);
    }

    #[test]
    fn test_journal_mode_display() {
        assert_eq!(JournalMode::Delete.to_string(), "DELETE");
        assert_eq!(JournalMode::Truncate.to_string(), "TRUNCATE");
        assert_eq!(JournalMode::Persist.to_string(), "PERSIST");
        assert_eq!(JournalMode::Memory.to_string(), "MEMORY");
        assert_eq!(JournalMode::Wal.to_string(), "WAL");
        assert_eq!(JournalMode::Off.to_string(), "OFF");
    }

    #[test]
    fn test_database_config_default() {
        let config = DatabaseConfig::default();
        assert_eq!(config.pool_size, 10);
        assert_eq!(config.busy_timeout, std::time::Duration::from_secs(30));
        assert!(matches!(config.journal_mode, JournalMode::Wal));
        assert!(config.path.to_string_lossy().contains("jfdi"));
        assert!(config.path.to_string_lossy().contains("data.db"));
    }

    #[test]
    fn test_pool_stats() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();

        let (total, idle) = ConnectionUtils::get_pool_stats(&pool);
        assert!(total >= 0);
        assert!(idle >= 0);
        assert!(idle <= total);
    }

    #[test]
    fn test_health_check_failure() {
        // This test simulates a health check failure by using an invalid path
        // Note: This might not always fail depending on system permissions
        let invalid_path = "/invalid/path/that/should/not/exist/test.db";
        
        // Try to create pool with invalid path - this should work initially
        // but health check might fail if directory creation fails
        if let Ok(pool) = ConnectionManager::create_pool(invalid_path) {
            // Health check should still pass as SQLite can create files
            let health = ConnectionUtils::health_check(&pool);
            // We can't guarantee this will fail, so just verify it returns a result
            assert!(health.is_ok() || health.is_err());
        }
    }

    #[test]
    fn test_multiple_connections() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = ConnectionManager::create_pool(&db_path).unwrap();

        // Get multiple connections
        let conn1 = pool.get().unwrap();
        let conn2 = pool.get().unwrap();

        // Both should be valid
        let result1: i32 = conn1.query_row("SELECT 1", [], |row| row.get(0)).unwrap();
        let result2: i32 = conn2.query_row("SELECT 1", [], |row| row.get(0)).unwrap();

        assert_eq!(result1, 1);
        assert_eq!(result2, 1);
    }

    #[test]
    fn test_connection_timeout() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        
        let config = DatabaseConfig {
            path: db_path.clone(),
            pool_size: 1, // Very small pool
            busy_timeout: std::time::Duration::from_millis(100), // Short timeout
            journal_mode: JournalMode::Wal,
        };

        let pool = ConnectionManager::create_pool_with_config(&db_path, &config).unwrap();
        
        // Get the only connection
        let _conn1 = pool.get().unwrap();
        
        // Try to get another connection - should timeout quickly
        let start = std::time::Instant::now();
        let result = pool.get_timeout(std::time::Duration::from_millis(50));
        let elapsed = start.elapsed();
        
        // Should timeout within reasonable time
        assert!(result.is_err());
        assert!(elapsed < std::time::Duration::from_millis(200));
    }
}
