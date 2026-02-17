use anyhow::{Context, Result};
use rusqlite::{params, Connection, OptionalExtension};

use crate::p2p::message::routing::{DeliveryStatus, TransportMethod};
use crate::p2p::message::types::MessageId;

/// Delivery and routing-related helper functions
pub struct DeliveryHelpers;

impl DeliveryHelpers {
    /// Create new delivery helpers
    pub fn new() -> Self {
        Self
    }

    /// Insert delivery status record
    pub fn insert_delivery_status(
        &self,
        conn: &Connection,
        message_id: &MessageId,
        peer_id: &str,
        status: &DeliveryStatus,
        transport_method: &TransportMethod,
    ) -> Result<()> {
        let status_str = Self::delivery_status_to_string(status);
        let transport_str = Self::transport_method_to_string(transport_method);

        conn.execute(
            "INSERT INTO p2p_delivery_status (
                message_id, peer_id, status, transport_method
            ) VALUES (?1, ?2, ?3, ?4)",
            params![message_id.to_string(), peer_id, status_str, transport_str,],
        )
        .context("Failed to insert delivery status")?;

        Ok(())
    }

    /// Insert routing history record
    pub fn insert_routing_history(
        &self,
        conn: &Connection,
        message_id: &MessageId,
        hop_peer_id: &str,
        transport_method: &TransportMethod,
        success: bool,
        error_details: Option<&str>,
    ) -> Result<()> {
        let transport_str = Self::transport_method_to_string(transport_method);

        conn.execute(
            "INSERT INTO p2p_routing_history (
                message_id, hop_peer_id, transport_method, 
                hop_timestamp, success, error_details
            ) VALUES (?1, ?2, ?3, ?4, ?5, ?6)",
            params![
                message_id.to_string(),
                hop_peer_id,
                transport_str,
                chrono::Utc::now().timestamp(),
                success,
                error_details,
            ],
        )
        .context("Failed to insert routing history")?;

        Ok(())
    }

    /// Convert DeliveryStatus to string representation
    pub fn delivery_status_to_string(status: &DeliveryStatus) -> &'static str {
        match status {
            DeliveryStatus::Pending => "pending",
            DeliveryStatus::Sent => "sent",
            DeliveryStatus::Delivered => "delivered",
            DeliveryStatus::Failed(_) => "failed",
            DeliveryStatus::Timeout => "timeout",
        }
    }

    /// Convert TransportMethod to string representation
    pub fn transport_method_to_string(transport: &TransportMethod) -> &'static str {
        match transport {
            TransportMethod::LibP2P => "libp2p",
            TransportMethod::Relay(_) => "relay",
            TransportMethod::WebRTC(_) => "webrtc",
        }
    }

    /// Convert string to DeliveryStatus
    pub fn string_to_delivery_status(status_str: &str) -> DeliveryStatus {
        match status_str {
            "pending" => DeliveryStatus::Pending,
            "sent" => DeliveryStatus::Sent,
            "delivered" => DeliveryStatus::Delivered,
            "failed" => DeliveryStatus::Failed("Unknown error".to_string()),
            "timeout" => DeliveryStatus::Timeout,
            _ => DeliveryStatus::Failed("Unknown error".to_string()),
        }
    }

    /// Convert string to TransportMethod
    pub fn string_to_transport_method(transport_str: &str) -> TransportMethod {
        match transport_str {
            "libp2p" => TransportMethod::LibP2P,
            "relay" => TransportMethod::Relay("unknown".to_string()),
            "webrtc" => TransportMethod::WebRTC("unknown".to_string()),
            _ => TransportMethod::LibP2P,
        }
    }

    /// Check if delivery status indicates completion
    pub fn is_final_status(status: &DeliveryStatus) -> bool {
        matches!(
            status,
            DeliveryStatus::Delivered | DeliveryStatus::Failed(_) | DeliveryStatus::Timeout
        )
    }

    /// Check if delivery status indicates success
    pub fn is_success_status(status: &DeliveryStatus) -> bool {
        matches!(status, DeliveryStatus::Delivered)
    }

    /// Check if delivery status indicates failure
    pub fn is_failure_status(status: &DeliveryStatus) -> bool {
        matches!(status, DeliveryStatus::Failed(_) | DeliveryStatus::Timeout)
    }

    /// Update delivery status with validation
    pub fn update_delivery_status(
        &self,
        conn: &Connection,
        message_id: &MessageId,
        peer_id: &str,
        new_status: &DeliveryStatus,
        error_details: Option<&str>,
    ) -> Result<bool> {
        if !self.can_update_status(conn, message_id, peer_id, new_status)? {
            return Ok(false);
        }
        self.execute_status_update(conn, message_id, peer_id, new_status, error_details)
    }

    /// Check if status can be updated
    fn can_update_status(
        &self,
        conn: &Connection,
        message_id: &MessageId,
        peer_id: &str,
        new_status: &DeliveryStatus,
    ) -> Result<bool> {
        let current_status_str: Option<String> = conn
            .query_row(
                "SELECT status FROM p2p_delivery_status WHERE message_id = ?1 AND peer_id = ?2",
                params![message_id.to_string(), peer_id],
                |row| row.get(0),
            )
            .optional()
            .context("Failed to check current delivery status")?;

        if let Some(current_str) = current_status_str {
            let current_status = Self::string_to_delivery_status(&current_str);
            if Self::is_final_status(&current_status)
                && !matches!(new_status, DeliveryStatus::Pending)
            {
                return Ok(false);
            }
        }
        Ok(true)
    }

    /// Execute status update query
    fn execute_status_update(
        &self,
        conn: &Connection,
        message_id: &MessageId,
        peer_id: &str,
        new_status: &DeliveryStatus,
        error_details: Option<&str>,
    ) -> Result<bool> {
        let rows_affected = conn
            .execute(
                "UPDATE p2p_delivery_status
             SET status = ?1, last_updated = ?2, error_details = ?3
             WHERE message_id = ?4 AND peer_id = ?5",
                params![
                    Self::delivery_status_to_string(new_status),
                    chrono::Utc::now().timestamp(),
                    error_details,
                    message_id.to_string(),
                    peer_id,
                ],
            )
            .context("Failed to update delivery status")?;
        Ok(rows_affected > 0)
    }

    /// Get next logical status in delivery progression
    pub fn get_next_status(current: &DeliveryStatus) -> Option<DeliveryStatus> {
        match current {
            DeliveryStatus::Pending => Some(DeliveryStatus::Sent),
            DeliveryStatus::Sent => Some(DeliveryStatus::Delivered),
            _ => None,
        }
    }
}
