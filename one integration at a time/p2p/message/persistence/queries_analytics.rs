use anyhow::{Context, Result};
use libp2p::PeerId;
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use rusqlite::{params, Connection, Row};
use std::sync::Arc;

use crate::p2p::message::routing::{DeliveryStatus, TransportMethod};
use crate::p2p::message::types::*;

/// Message statistics for analytics
#[derive(Debug, Clone)]
pub struct MessageStats {
    pub total_messages: u64,
    pub sent_messages: u64,
    pub received_messages: u64,
    pub failed_deliveries: u64,
    pub pending_deliveries: u64,
    pub average_delivery_time_ms: Option<f64>,
}

/// Analytics and monitoring queries
#[derive(Clone)]
pub struct AnalyticsQueries {
    pool: Arc<Pool<SqliteConnectionManager>>,
}

impl AnalyticsQueries {
    /// Create new analytics queries handler with connection pool
    pub fn new(pool: Arc<Pool<SqliteConnectionManager>>) -> Self {
        Self { pool }
    }

    /// Get delivery status for a message
    pub async fn get_delivery_status(
        &self,
        message_id: &MessageId,
    ) -> Result<Vec<(PeerId, DeliveryStatus, TransportMethod)>> {
        self.get_delivery_status_impl(message_id).await
    }

    /// Implementation for delivery status retrieval
    async fn get_delivery_status_impl(
        &self,
        message_id: &MessageId,
    ) -> Result<Vec<(PeerId, DeliveryStatus, TransportMethod)>> {
        let pool = self.pool.clone();
        let message_id = message_id.clone();

        tokio::task::spawn_blocking(move || {
            let conn = pool.get().context("Failed to get database connection")?;
            Self::execute_delivery_status_query(&conn, &message_id)
        })
        .await
        .context("Task join error")?
    }

    /// Execute delivery status query
    fn execute_delivery_status_query(
        conn: &Connection,
        message_id: &MessageId,
    ) -> Result<Vec<(PeerId, DeliveryStatus, TransportMethod)>> {
        let mut stmt = conn
            .prepare(
                "SELECT peer_id, status, transport_method
             FROM p2p_delivery_status
             WHERE message_id = ?1",
            )
            .context("Failed to prepare delivery status query")?;

        let status_iter = stmt
            .query_map(params![message_id.to_string()], |row| {
                Self::parse_delivery_status_row(row)
            })
            .context("Failed to execute delivery status query")?;

        let mut statuses = Vec::new();
        for status_result in status_iter {
            statuses.push(status_result?);
        }
        Ok(statuses)
    }

    /// Parse delivery status row
    fn parse_delivery_status_row(
        row: &Row,
    ) -> rusqlite::Result<(PeerId, DeliveryStatus, TransportMethod)> {
        let peer_id_str: String = row.get(0)?;
        let status_str: String = row.get(1)?;
        let transport_str: String = row.get(2)?;

        let peer_id = peer_id_str.parse::<PeerId>().map_err(|_| {
            rusqlite::Error::InvalidColumnType(
                0,
                "peer_id".to_string(),
                rusqlite::types::Type::Text,
            )
        })?;

        let status = Self::parse_delivery_status(&status_str);
        let transport = Self::parse_transport_method(&transport_str);

        Ok((peer_id, status, transport))
    }

    /// Parse delivery status string
    fn parse_delivery_status(status_str: &str) -> DeliveryStatus {
        match status_str {
            "pending" => DeliveryStatus::Pending,
            "sent" => DeliveryStatus::Sent,
            "delivered" => DeliveryStatus::Delivered,
            "failed" => DeliveryStatus::Failed("Unknown error".to_string()),
            "timeout" => DeliveryStatus::Timeout,
            _ => DeliveryStatus::Failed("Unknown error".to_string()),
        }
    }

    /// Parse transport method string
    fn parse_transport_method(transport_str: &str) -> TransportMethod {
        match transport_str {
            "libp2p" => TransportMethod::LibP2P,
            "relay" => TransportMethod::Relay("unknown".to_string()),
            "webrtc" => TransportMethod::WebRTC("unknown".to_string()),
            _ => TransportMethod::LibP2P,
        }
    }

    /// Get message statistics for analytics
    pub async fn get_message_statistics(&self) -> Result<MessageStats> {
        self.get_message_statistics_impl().await
    }

    /// Implementation for message statistics retrieval
    async fn get_message_statistics_impl(&self) -> Result<MessageStats> {
        let pool = self.pool.clone();

        tokio::task::spawn_blocking(move || {
            let conn = pool.get().context("Failed to get database connection")?;
            Self::collect_message_statistics(&conn)
        })
        .await
        .context("Task join error")?
    }

    /// Collect message statistics from database
    fn collect_message_statistics(conn: &Connection) -> Result<MessageStats> {
        let total_messages = Self::get_total_message_count(conn)?;
        let sent_messages = Self::get_sent_message_count(conn)?;
        let received_messages = total_messages - sent_messages;
        let (failed_deliveries, pending_deliveries) = Self::get_delivery_statistics(conn)?;
        let average_delivery_time_ms = None; // TODO: Implement based on routing history

        Ok(MessageStats {
            total_messages,
            sent_messages,
            received_messages,
            failed_deliveries,
            pending_deliveries,
            average_delivery_time_ms,
        })
    }

    /// Get total message count
    fn get_total_message_count(conn: &Connection) -> Result<u64> {
        conn.query_row("SELECT COUNT(*) FROM p2p_messages", [], |row| row.get(0))
            .context("Failed to get total message count")
    }

    /// Get sent message count
    fn get_sent_message_count(conn: &Connection) -> Result<u64> {
        conn.query_row(
            "SELECT COUNT(*) FROM p2p_messages WHERE recipient_id IS NOT NULL",
            [],
            |row| row.get(0),
        )
        .context("Failed to get sent message count")
    }

    /// Get delivery statistics
    fn get_delivery_statistics(conn: &Connection) -> Result<(u64, u64)> {
        let failed_deliveries: u64 = conn
            .query_row(
                "SELECT COUNT(*) FROM p2p_delivery_status WHERE status = 'failed'",
                [],
                |row| row.get(0),
            )
            .context("Failed to get failed delivery count")?;

        let pending_deliveries: u64 = conn
            .query_row(
                "SELECT COUNT(*) FROM p2p_delivery_status WHERE status = 'pending'",
                [],
                |row| row.get(0),
            )
            .context("Failed to get pending delivery count")?;

        Ok((failed_deliveries, pending_deliveries))
    }
}
