use libp2p::PeerId;
use rusqlite::Row;
use serde_json;
use std::str::FromStr;

use crate::p2p::message::types::*;

/// Query filters for message retrieval
#[derive(Debug, Clone)]
pub struct MessageFilter {
    pub sender_id: Option<PeerId>,
    pub recipient_id: Option<PeerId>,
    pub message_type: Option<String>,
    pub start_timestamp: Option<i64>,
    pub end_timestamp: Option<i64>,
    pub limit: Option<u32>,
    pub offset: Option<u32>,
}

impl Default for MessageFilter {
    fn default() -> Self {
        Self {
            sender_id: None,
            recipient_id: None,
            message_type: None,
            start_timestamp: None,
            end_timestamp: None,
            limit: Some(100),
            offset: Some(0),
        }
    }
}

impl MessageFilter {
    pub fn matches(&self, msg: &StoredMessage) -> bool {
        if let Some(sender_id) = &self.sender_id {
            if sender_id.to_string() != msg.peer_id {
                return false;
            }
        }
        // Add other filter conditions here
        true
    }
}

/// Convert database row to StoredMessage
pub fn row_to_message(row: &Row) -> rusqlite::Result<StoredMessage> {
    let content = parse_message_content(row)?;
    let metadata = parse_message_metadata(row)?;
    let sender = parse_sender_id(row)?;

    let id_str: String = row.get("id")?;
    let id = MessageId::from_str(&id_str).map_err(|_| {
        rusqlite::Error::InvalidColumnType(0, "id".to_string(), rusqlite::types::Type::Text)
    })?;

    let timestamp: i64 = row.get("timestamp")?;
    let created_at =
        chrono::DateTime::from_timestamp(timestamp, 0).unwrap_or_else(|| chrono::Utc::now());

    Ok(StoredMessage {
        id,
        peer_id: sender,
        message: content,
        direction: metadata,
        status: MessageStatus::Delivered,
        created_at,
        delivered_at: None,
    })
}

/// Parse message content from row
fn parse_message_content(row: &Row) -> rusqlite::Result<P2PMessage> {
    let content_json: String = row.get("content")?;
    serde_json::from_str(&content_json).map_err(|_| {
        rusqlite::Error::InvalidColumnType(2, "content".to_string(), rusqlite::types::Type::Text)
    })
}

/// Parse message metadata from row
fn parse_message_metadata(row: &Row) -> rusqlite::Result<MessageDirection> {
    let metadata_json: Option<String> = row.get("metadata")?;
    match metadata_json {
        Some(json) => {
            // Try to parse as MessageDirection first
            if let Ok(direction) = serde_json::from_str::<MessageDirection>(&json) {
                return Ok(direction);
            }
            // If that fails, it might be a metadata object - default to Received
            Ok(MessageDirection::Received)
        }
        None => Ok(MessageDirection::Received), // Default to Received if no metadata
    }
}

/// Parse sender ID from row
fn parse_sender_id(row: &Row) -> rusqlite::Result<String> {
    row.get("sender_id")
}
