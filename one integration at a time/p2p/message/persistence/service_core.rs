use super::service_maintenance::ServiceMaintenanceImpl;
use super::service_operations::ServiceOperationsImpl;
use super::{
    ConnectionManager, EventProcessor, PersistenceOperations, PersistenceQueries, SchemaManager,
};
use crate::p2p::{MessageConfig, MessageEvent};
use anyhow::{Context, Result};
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use std::sync::Arc;
use tokio::sync::mpsc;
/// Main message persistence service with SQLite backend
/// Integrates with Task 3.4 routing system and MessageService workflow
#[derive(Clone)]
pub struct PersistenceService {
    config: MessageConfig,
    connection_pool: Arc<Pool<SqliteConnectionManager>>,
    event_sender: mpsc::UnboundedSender<MessageEvent>,
    pub(crate) operations_impl: ServiceOperationsImpl,
    pub(crate) maintenance_impl: ServiceMaintenanceImpl,
}

impl PersistenceService {
    /// Create new persistence service with database initialization
    pub async fn new(
        config: &MessageConfig,
        event_sender: mpsc::UnboundedSender<MessageEvent>,
    ) -> Result<Self> {
        let connection_pool = Self::initialize_database(config)?;
        let (operations_impl, maintenance_impl) =
            Self::create_service_components(&connection_pool, &event_sender);

        Ok(Self {
            config: config.clone(),
            connection_pool,
            event_sender,
            operations_impl,
            maintenance_impl,
        })
    }

    /// Initialize database connection pool and schema
    fn initialize_database(config: &MessageConfig) -> Result<Arc<Pool<SqliteConnectionManager>>> {
        let connection_pool = Arc::new(ConnectionManager::create_pool(&config.database_path)
            .context("Failed to create database connection pool during PersistenceService initialization")?);
        SchemaManager::initialize_schema(&connection_pool).context(
            "Failed to initialize database schema during PersistenceService initialization",
        )?;
        Ok(connection_pool)
    }
    /// Create service implementation components
    fn create_service_components(
        connection_pool: &Arc<Pool<SqliteConnectionManager>>,
        event_sender: &mpsc::UnboundedSender<MessageEvent>,
    ) -> (ServiceOperationsImpl, ServiceMaintenanceImpl) {
        let operations = PersistenceOperations::new(connection_pool.clone());
        let queries = PersistenceQueries::new(connection_pool.clone());
        let event_processor = EventProcessor::new(connection_pool.clone(), event_sender.clone());

        let operations_impl =
            ServiceOperationsImpl::new(operations, queries.clone(), event_processor.clone());
        let maintenance_impl = ServiceMaintenanceImpl::new(connection_pool.clone());

        (operations_impl, maintenance_impl)
    }
    /// Get service configuration
    pub fn config(&self) -> &MessageConfig {
        &self.config
    }
    /// Get connection pool reference
    pub fn connection_pool(&self) -> &Arc<Pool<SqliteConnectionManager>> {
        &self.connection_pool
    }
    /// Get event sender reference
    pub fn event_sender(&self) -> &mpsc::UnboundedSender<MessageEvent> {
        &self.event_sender
    }
}
