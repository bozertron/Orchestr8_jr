use anyhow::{Context, Result};
use libp2p::PeerId;
use r2d2::{Pool, PooledConnection};
use r2d2_sqlite::SqliteConnectionManager;
use rusqlite::{params, Connection};
use std::sync::Arc;

use super::connection::ConnectionUtils;
use crate::p2p::message::routing::{DeliveryStatus, TransportMethod};
use crate::p2p::message::types::*;

pub use super::operations_helpers::*;

/// Core CRUD operations for P2P message persistence
#[derive(Clone)]
pub struct PersistenceOperations {
    pool: Arc<Pool<SqliteConnectionManager>>,
}

impl PersistenceOperations {
    /// Create new operations handler with connection pool
    pub fn new(pool: Arc<Pool<SqliteConnectionManager>>) -> Self {
        Self { pool }
    }

    /// Store sent message with routing metadata
    pub async fn store_sent_message(
        &self,
        message_id: &MessageId,
        to: &PeerId,
        message: &P2PMessage,
        transport_method: &TransportMethod,
    ) -> Result<()> {
        self.store_sent_message_impl(message_id, to, message, transport_method)
            .await
    }

    /// Implementation for storing sent message
    async fn store_sent_message_impl(
        &self,
        message_id: &MessageId,
        to: &PeerId,
        message: &P2PMessage,
        transport_method: &TransportMethod,
    ) -> Result<()> {
        let pool = self.pool.clone();
        let message_id = message_id.clone();
        let to = to.to_string();
        let message = message.clone();
        let transport_method = transport_method.clone();

        tokio::task::spawn_blocking(move || {
            let mut conn = pool.get().context("Failed to get database connection")?;

            Self::execute_sent_message_transaction(
                &mut conn,
                &message_id,
                &to,
                &message,
                &transport_method,
            )
        })
        .await
        .context("Task join error")?
    }

    /// Execute transaction for sent message storage
    fn execute_sent_message_transaction(
        conn: &mut PooledConnection<SqliteConnectionManager>,
        message_id: &MessageId,
        to: &str,
        message: &P2PMessage,
        transport_method: &TransportMethod,
    ) -> Result<()> {
        ConnectionUtils::execute_transaction(conn, |tx| {
            // For sent messages: sender_id is "local" (represents local user), recipient_id is 'to'
            Self::insert_message_record(tx, message_id, message, Some("local"), Some(to))?;
            Self::insert_delivery_status(
                tx,
                message_id,
                to,
                &DeliveryStatus::Pending,
                transport_method,
            )?;
            Ok(())
        })
    }

    /// Store received message with sender information
    pub async fn store_received_message(
        &self,
        message: &P2PMessage,
        from: &PeerId,
        message_id: Option<MessageId>,
    ) -> Result<MessageId> {
        self.store_received_message_impl(message, from, message_id)
            .await
    }

    /// Implementation for storing received message
    async fn store_received_message_impl(
        &self,
        message: &P2PMessage,
        from: &PeerId,
        message_id: Option<MessageId>,
    ) -> Result<MessageId> {
        let pool = self.pool.clone();
        let message = message.clone();
        let from = from.to_string();
        let final_message_id = message_id.unwrap_or_else(|| MessageId::new_v4());

        tokio::task::spawn_blocking(move || {
            let mut conn = pool.get().context("Failed to get database connection")?;

            Self::execute_received_message_transaction(
                &mut conn,
                &final_message_id,
                &message,
                &from,
            )
        })
        .await
        .context("Task join error")?
    }

    /// Execute transaction for received message storage
    fn execute_received_message_transaction(
        conn: &mut PooledConnection<SqliteConnectionManager>,
        message_id: &MessageId,
        message: &P2PMessage,
        from: &str,
    ) -> Result<MessageId> {
        ConnectionUtils::execute_transaction(conn, |tx| {
            // For received messages: sender_id is 'from', recipient_id is "local" (represents local user)
            Self::insert_message_record(tx, message_id, message, Some(from), Some("local"))?;
            let helpers = OperationHelpers::new();
            helpers.insert_routing_history(
                tx,
                message_id,
                from,
                &TransportMethod::LibP2P,
                true,
                None,
            )?;
            Ok(message_id.clone())
        })
    }

    /// Update delivery status for message routing
    pub async fn update_delivery_status(
        &self,
        message_id: &MessageId,
        peer_id: &PeerId,
        status: &DeliveryStatus,
        error_message: Option<&str>,
    ) -> Result<()> {
        let pool = self.pool.clone();
        let message_id = message_id.clone();
        let peer_id = peer_id.to_string();
        let status = status.clone();
        let error_message = error_message.map(|s| s.to_string());

        tokio::task::spawn_blocking(move || {
            let conn = pool.get().context("Failed to get database connection")?;

            let status_str = OperationHelpers::delivery_status_to_string(&status);

            conn.execute(
                "UPDATE p2p_delivery_status 
                 SET status = ?1, error_message = ?2, updated_at = unixepoch()
                 WHERE message_id = ?3 AND peer_id = ?4",
                params![status_str, error_message, message_id.to_string(), peer_id],
            )
            .context("Failed to update delivery status")?;

            Ok(())
        })
        .await
        .context("Task join error")?
    }

    /// Delete message and all related records
    pub async fn delete_message(&self, message_id: &MessageId) -> Result<bool> {
        let pool = self.pool.clone();
        let message_id = message_id.clone();

        let result = tokio::task::spawn_blocking(move || {
            let conn = pool.get().context("Failed to get database connection")?;

            let rows_affected = conn
                .execute(
                    "DELETE FROM p2p_messages WHERE id = ?1",
                    params![message_id.to_string()],
                )
                .context("Failed to delete message")?;

            Ok(rows_affected > 0)
        })
        .await
        .context("Task join error")?;

        result
    }

    /// Insert message record into database
    fn insert_message_record(
        conn: &Connection,
        message_id: &MessageId,
        message: &P2PMessage,
        sender_id: Option<&str>,
        recipient_id: Option<&str>,
    ) -> Result<()> {
        let helpers = OperationHelpers::new();
        helpers.insert_message_record(conn, message_id, message, sender_id, recipient_id)
    }

    /// Insert delivery status record
    pub fn insert_delivery_status(
        conn: &Connection,
        message_id: &MessageId,
        peer_id: &str,
        status: &DeliveryStatus,
        transport_method: &TransportMethod,
    ) -> Result<()> {
        let helpers = OperationHelpers::new();
        helpers.insert_delivery_status(conn, message_id, peer_id, status, transport_method)
    }
}
