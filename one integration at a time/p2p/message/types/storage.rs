use super::core::{MessageId, P2PMessage};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

/// Stored message for persistence
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StoredMessage {
    pub id: MessageId,
    pub peer_id: String,
    pub message: P2PMessage,
    pub direction: MessageDirection,
    pub status: MessageStatus,
    pub created_at: DateTime<Utc>,
    pub delivered_at: Option<DateTime<Utc>>,
}

/// Message direction
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum MessageDirection {
    Sent,
    Received,
}

/// Message delivery status
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum MessageStatus {
    Pending,
    Sent,
    Delivered,
    Failed(String),
}
