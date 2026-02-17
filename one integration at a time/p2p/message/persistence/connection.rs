use anyhow::{Context, Result};
use r2d2::{Pool, PooledConnection};
use r2d2_sqlite::SqliteConnectionManager;
use rusqlite::{Connection, OpenFlags};
use std::path::Path;
use std::time::Duration;

/// Database connection configuration following JFDI Pattern Bible
#[derive(Debug, Clone)]
pub struct DatabaseConfig {
    pub path: std::path::PathBuf,
    pub pool_size: u32,
    pub busy_timeout: Duration,
    pub journal_mode: JournalMode,
}

#[derive(Debug, Clone)]
pub enum JournalMode {
    Delete,
    Truncate,
    Persist,
    Memory,
    Wal,
    Off,
}

impl Default for DatabaseConfig {
    fn default() -> Self {
        Self {
            path: dirs::data_dir()
                .unwrap_or_else(|| std::path::PathBuf::from("."))
                .join("jfdi")
                .join("data.db"),
            pool_size: 10,
            busy_timeout: Duration::from_secs(30),
            journal_mode: JournalMode::Wal,
        }
    }
}

impl std::fmt::Display for JournalMode {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            JournalMode::Delete => write!(f, "DELETE"),
            JournalMode::Truncate => write!(f, "TRUNCATE"),
            JournalMode::Persist => write!(f, "PERSIST"),
            JournalMode::Memory => write!(f, "MEMORY"),
            JournalMode::Wal => write!(f, "WAL"),
            JournalMode::Off => write!(f, "OFF"),
        }
    }
}

/// Connection manager for SQLite database pools
pub struct ConnectionManager;

impl ConnectionManager {
    /// Create optimized SQLite connection pool following Pattern Bible
    pub fn create_pool<P: AsRef<Path>>(database_path: P) -> Result<Pool<SqliteConnectionManager>> {
        let config = DatabaseConfig::default();
        Self::create_pool_with_config(database_path, &config)
    }

    /// Create connection pool with custom configuration
    pub fn create_pool_with_config<P: AsRef<Path>>(
        database_path: P,
        config: &DatabaseConfig,
    ) -> Result<Pool<SqliteConnectionManager>> {
        // Ensure parent directory exists
        if let Some(parent) = database_path.as_ref().parent() {
            std::fs::create_dir_all(parent).context("Failed to create database directory")?;
        }

        // Create connection manager with optimized flags
        let manager = SqliteConnectionManager::file(database_path).with_flags(
            OpenFlags::SQLITE_OPEN_READ_WRITE
                | OpenFlags::SQLITE_OPEN_CREATE
                | OpenFlags::SQLITE_OPEN_NO_MUTEX,
        );

        // Build connection pool
        let pool = r2d2::Pool::builder()
            .max_size(config.pool_size)
            .connection_timeout(config.busy_timeout)
            .build(manager)
            .context("Failed to create connection pool")?;

        // Configure initial connection for performance
        Self::configure_connection(&pool, config)?;

        Ok(pool)
    }

    /// Configure SQLite connection for optimal performance
    fn configure_connection(
        pool: &Pool<SqliteConnectionManager>,
        config: &DatabaseConfig,
    ) -> Result<()> {
        let conn = pool.get().context("Failed to get connection from pool")?;

        // Apply performance optimizations from Pattern Bible
        conn.execute_batch(&format!(
            "
            PRAGMA journal_mode = {};
            PRAGMA synchronous = NORMAL;
            PRAGMA cache_size = -64000;
            PRAGMA mmap_size = 268435456;
            PRAGMA foreign_keys = ON;
            PRAGMA busy_timeout = {};
            PRAGMA temp_store = MEMORY;
            PRAGMA page_size = 4096;
            ",
            config.journal_mode,
            config.busy_timeout.as_millis()
        ))
        .context("Failed to configure SQLite connection")?;

        Ok(())
    }
}

/// Type alias for pooled SQLite connection
pub type PooledSqliteConnection = PooledConnection<SqliteConnectionManager>;

/// Connection utilities for database operations
pub struct ConnectionUtils;

impl ConnectionUtils {
    /// Execute transaction with automatic rollback on error
    pub fn execute_transaction<F, R>(conn: &mut PooledSqliteConnection, operation: F) -> Result<R>
    where
        F: FnOnce(&Connection) -> Result<R>,
    {
        let tx = conn.transaction().context("Failed to begin transaction")?;

        match operation(&tx) {
            Ok(result) => {
                tx.commit().context("Failed to commit transaction")?;
                Ok(result)
            }
            Err(e) => {
                let _ = tx.rollback();
                Err(e)
            }
        }
    }

    /// Check database health and connectivity
    pub fn health_check(pool: &Pool<SqliteConnectionManager>) -> Result<bool> {
        let conn = pool
            .get()
            .context("Failed to get connection for health check")?;

        let result: i32 = conn
            .query_row("SELECT 1", [], |row| row.get(0))
            .context("Health check query failed")?;

        Ok(result == 1)
    }

    /// Get connection pool statistics
    pub fn get_pool_stats(pool: &Pool<SqliteConnectionManager>) -> (u32, u32) {
        let state = pool.state();
        (state.connections, state.idle_connections)
    }
}
