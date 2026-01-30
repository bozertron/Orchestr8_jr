use anyhow::{Context, Result};
use libp2p::PeerId;
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use rusqlite::params;
use std::str::FromStr;

use super::DeliveryInfo;
use crate::p2p::message::routing::{DeliveryStatus, TransportMethod};
use crate::p2p::message::types::MessageId;

/// Helper functions for delivery queries
pub struct DeliveryQueryHelpers;

impl DeliveryQueryHelpers {
    /// Query delivery status from database
    pub fn query_delivery_status(
        pool: &Pool<SqliteConnectionManager>,
        message_id: &str,
    ) -> Result<Vec<DeliveryInfo>> {
        let conn = pool.get().context("Failed to get database connection")?;

        let mut stmt = conn.prepare(
            "SELECT message_id, peer_id, status, transport_method,
                    attempt_count, last_attempt_at, next_retry_at,
                    error_message, created_at, updated_at
             FROM p2p_delivery_status
             WHERE message_id = ?1
             ORDER BY updated_at DESC",
        )?;

        let results = stmt
            .query_map(params![message_id], |row| Self::row_to_delivery_info(row))?
            .collect::<rusqlite::Result<Vec<_>>>()?;

        Ok(results)
    }

    /// Convert database row to DeliveryInfo
    pub fn row_to_delivery_info(row: &rusqlite::Row) -> rusqlite::Result<DeliveryInfo> {
        let message_id_str: String = row.get("message_id")?;
        let message_id = MessageId::from_str(&message_id_str).map_err(|_| {
            rusqlite::Error::InvalidColumnType(
                0,
                "message_id".to_string(),
                rusqlite::types::Type::Text,
            )
        })?;

        let peer_id_str: String = row.get("peer_id")?;
        let peer_id = peer_id_str.parse::<PeerId>().map_err(|_| {
            rusqlite::Error::InvalidColumnType(
                1,
                "peer_id".to_string(),
                rusqlite::types::Type::Text,
            )
        })?;

        let status_str: String = row.get("status")?;
        let status = Self::parse_delivery_status(&status_str);

        let transport_str: String = row.get("transport_method")?;
        let transport_method = Self::parse_transport_method(&transport_str);

        Ok(DeliveryInfo {
            message_id,
            peer_id,
            status,
            transport_method,
            attempt_count: row.get("attempt_count")?,
            last_attempt_at: row.get("last_attempt_at")?,
            next_retry_at: row.get("next_retry_at")?,
            error_message: row.get("error_message")?,
            created_at: row.get("created_at")?,
            updated_at: row.get("updated_at")?,
        })
    }

    /// Parse delivery status from string
    pub fn parse_delivery_status(status_str: &str) -> DeliveryStatus {
        match status_str {
            "pending" => DeliveryStatus::Pending,
            "sent" => DeliveryStatus::Sent,
            "delivered" => DeliveryStatus::Delivered,
            s if s.starts_with("failed:") => {
                DeliveryStatus::Failed(s.strip_prefix("failed:").unwrap_or("").to_string())
            }
            "timeout" => DeliveryStatus::Timeout,
            _ => DeliveryStatus::Pending,
        }
    }

    /// Parse transport method from string
    pub fn parse_transport_method(transport_str: &str) -> TransportMethod {
        if transport_str.starts_with("webrtc:") {
            TransportMethod::WebRTC(
                transport_str
                    .strip_prefix("webrtc:")
                    .unwrap_or("")
                    .to_string(),
            )
        } else if transport_str == "libp2p" {
            TransportMethod::LibP2P
        } else if transport_str.starts_with("relay:") {
            TransportMethod::Relay(
                transport_str
                    .strip_prefix("relay:")
                    .unwrap_or("")
                    .to_string(),
            )
        } else {
            TransportMethod::LibP2P
        }
    }

    /// Query pending deliveries
    pub fn query_pending_deliveries(
        pool: &Pool<SqliteConnectionManager>,
        limit: u32,
    ) -> Result<Vec<DeliveryInfo>> {
        let conn = pool.get().context("Failed to get database connection")?;

        let mut stmt = conn.prepare(
            "SELECT message_id, peer_id, status, transport_method,
                    attempt_count, last_attempt_at, next_retry_at,
                    error_message, created_at, updated_at
             FROM p2p_delivery_status
             WHERE status = 'pending'
             AND (next_retry_at IS NULL OR next_retry_at <= unixepoch())
             ORDER BY created_at ASC
             LIMIT ?1",
        )?;

        let results = stmt
            .query_map(params![limit], |row| Self::row_to_delivery_info(row))?
            .collect::<rusqlite::Result<Vec<_>>>()?;

        Ok(results)
    }

    /// Query failed deliveries
    pub fn query_failed_deliveries(
        pool: &Pool<SqliteConnectionManager>,
        limit: u32,
    ) -> Result<Vec<DeliveryInfo>> {
        let conn = pool.get().context("Failed to get database connection")?;

        let mut stmt = conn.prepare(
            "SELECT message_id, peer_id, status, transport_method,
                    attempt_count, last_attempt_at, next_retry_at,
                    error_message, created_at, updated_at
             FROM p2p_delivery_status
             WHERE status = 'failed'
             ORDER BY updated_at DESC
             LIMIT ?1",
        )?;

        let results = stmt
            .query_map(params![limit], |row| Self::row_to_delivery_info(row))?
            .collect::<rusqlite::Result<Vec<_>>>()?;

        Ok(results)
    }
}
