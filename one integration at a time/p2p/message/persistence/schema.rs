use anyhow::{Context, Result};
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use rusqlite::Connection;

pub use super::schema_fts::*;
pub use super::schema_indexes::*;
pub use super::schema_tables::*;

/// Database schema version for migration tracking
pub const CURRENT_SCHEMA_VERSION: i32 = 1;

/// Schema manager for P2P message persistence
pub struct SchemaManager;

impl SchemaManager {
    /// Initialize database schema with all required tables
    pub fn initialize_schema(pool: &Pool<SqliteConnectionManager>) -> Result<()> {
        let conn = pool
            .get()
            .context("Failed to get connection for schema initialization")?;

        // Check current schema version
        let current_version = Self::get_schema_version(&conn)?;

        if current_version < CURRENT_SCHEMA_VERSION {
            Self::create_tables(&conn)?;
            Self::create_indexes(&conn)?;
            Self::create_fts_tables(&conn)?;
            Self::set_schema_version(&conn, CURRENT_SCHEMA_VERSION)?;
        }

        Ok(())
    }

    /// Get current database schema version
    fn get_schema_version(conn: &Connection) -> Result<i32> {
        // Create schema_version table if it doesn't exist
        conn.execute(
            "CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY
            )",
            [],
        )
        .context("Failed to create schema_version table")?;

        // Get current version or default to 0
        let version = conn
            .query_row("SELECT version FROM schema_version LIMIT 1", [], |row| {
                row.get::<_, i32>(0)
            })
            .unwrap_or(0);

        Ok(version)
    }

    /// Set schema version in database
    fn set_schema_version(conn: &Connection, version: i32) -> Result<()> {
        conn.execute(
            "INSERT OR REPLACE INTO schema_version (version) VALUES (?1)",
            [version],
        )
        .context("Failed to set schema version")?;

        Ok(())
    }

    /// Create all required tables for P2P message persistence
    fn create_tables(conn: &Connection) -> Result<()> {
        TableCreator::create_all_tables(conn)
    }

    /// Create database indexes for optimal query performance
    fn create_indexes(conn: &Connection) -> Result<()> {
        IndexCreator::create_all_indexes(conn)
    }

    /// Create FTS5 tables for full-text search capabilities
    fn create_fts_tables(conn: &Connection) -> Result<()> {
        let fts_creator = FTSCreator::new();
        fts_creator.create_fts_complete(conn)
    }

    /// Drop all tables (for testing/reset purposes)
    #[cfg(test)]
    pub fn drop_all_tables(conn: &Connection) -> Result<()> {
        let tables = [
            "DROP TABLE IF EXISTS p2p_message_events",
            "DROP TABLE IF EXISTS p2p_routing_history",
            "DROP TABLE IF EXISTS p2p_delivery_status",
            "DROP TABLE IF EXISTS p2p_messages_fts",
            "DROP TABLE IF EXISTS p2p_messages",
            "DROP TABLE IF EXISTS schema_version",
        ];

        for table_sql in &tables {
            conn.execute(table_sql, [])
                .with_context(|| format!("Failed to drop table: {}", table_sql))?;
        }

        Ok(())
    }
}
