use anyhow::{Context, Result};
use rusqlite::{params, Connection};
use serde_json;

use crate::p2p::message::types::*;

/// Message-related helper functions
pub struct MessageHelpers;

impl MessageHelpers {
    /// Create new message helpers
    pub fn new() -> Self {
        Self
    }

    /// Insert message record into database
    pub fn insert_message_record(
        &self,
        conn: &Connection,
        message_id: &MessageId,
        message: &P2PMessage,
        sender_id: Option<&str>,
        recipient_id: Option<&str>,
    ) -> Result<()> {
        let (message_type, content_json, metadata_json) = self.prepare_message_data(message)?;
        self.execute_message_insert(
            conn,
            message_id,
            message,
            sender_id,
            recipient_id,
            &message_type,
            &content_json,
            &metadata_json,
        )
    }

    /// Prepare message data for insertion
    fn prepare_message_data(&self, message: &P2PMessage) -> Result<(&'static str, String, String)> {
        let message_type = message.message_type();
        let content_json = Self::serialize_message_content(message)?;
        let metadata_json = Self::serialize_message_metadata(message)?;
        Ok((message_type, content_json, metadata_json))
    }

    /// Execute message insertion query
    fn execute_message_insert(
        &self,
        conn: &Connection,
        message_id: &MessageId,
        message: &P2PMessage,
        sender_id: Option<&str>,
        recipient_id: Option<&str>,
        message_type: &str,
        content_json: &str,
        metadata_json: &str,
    ) -> Result<()> {
        conn.execute(
            "INSERT INTO p2p_messages (
                id, message_type, content, sender_id, recipient_id,
                timestamp, signature, encryption_key_id, content_hash, metadata
            ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10)",
            params![
                message_id.to_string(),
                message_type,
                content_json,
                sender_id,
                recipient_id,
                message.timestamp().map(|t| t.timestamp()).unwrap_or(0),
                None::<Vec<u8>>,
                None::<String>,
                message_id.to_string(),
                metadata_json,
            ],
        )
        .context("Failed to insert message record")?;
        Ok(())
    }

    /// Get message type string from content
    pub fn get_message_type_string(content: &P2PMessage) -> &'static str {
        content.message_type()
    }

    /// Serialize message content to JSON
    pub fn serialize_message_content(content: &P2PMessage) -> Result<String> {
        serde_json::to_string(content).context("Failed to serialize message content")
    }

    /// Serialize message metadata to JSON
    pub fn serialize_message_metadata(message: &P2PMessage) -> Result<String> {
        // Create basic metadata from the message
        let metadata = serde_json::json!({
            "message_type": message.message_type(),
            "requires_confirmation": message.requires_confirmation(),
            "has_timestamp": message.timestamp().is_some()
        });
        serde_json::to_string(&metadata).context("Failed to serialize message metadata")
    }

    /// Deserialize message content from JSON
    pub fn deserialize_message_content(json: &str) -> Result<P2PMessage> {
        serde_json::from_str(json).context("Failed to deserialize message content")
    }

    /// Deserialize message metadata from JSON
    pub fn deserialize_message_metadata(json: &str) -> Result<StoredMessage> {
        serde_json::from_str(json).context("Failed to deserialize message metadata")
    }

    /// Validate message content structure
    pub fn validate_message_content(content: &P2PMessage) -> Result<()> {
        match content {
            P2PMessage::Chat { text, .. } => {
                if text.is_empty() {
                    return Err(anyhow::anyhow!("Chat message text cannot be empty"));
                }
                Ok(())
            }
            P2PMessage::FileOffer { name, size, .. } => {
                if name.is_empty() {
                    return Err(anyhow::anyhow!("File name cannot be empty"));
                }
                if *size == 0 {
                    return Err(anyhow::anyhow!("File size must be greater than 0"));
                }
                Ok(())
            }
            _ => Ok(()), // Other message types are valid by construction
        }
    }

    /// Get content size in bytes
    pub fn get_content_size(content: &P2PMessage) -> usize {
        match content {
            P2PMessage::Chat { text, .. } => text.len(),
            P2PMessage::FileOffer { name, .. } => name.len(),
            P2PMessage::FileChunk { data, .. } => data.len(),
            P2PMessage::CallInvite { sdp_offer, .. } => sdp_offer.len(),
            P2PMessage::StateSync { changes, .. } => changes.iter().map(|c| c.data.len()).sum(),
            _ => 0,
        }
    }

    /// Check if message content is large (over 1MB)
    pub fn is_large_content(content: &P2PMessage) -> bool {
        Self::get_content_size(content) > 1024 * 1024
    }

    /// Get content summary for logging
    pub fn get_content_summary(content: &P2PMessage) -> String {
        match content {
            P2PMessage::Chat { text, .. } => {
                format!(
                    "Chat: {}",
                    if text.len() > 50 {
                        format!("{}...", &text[..50])
                    } else {
                        text.clone()
                    }
                )
            }
            P2PMessage::FileOffer { name, size, .. } => {
                format!("File: {} ({} bytes)", name, size)
            }
            P2PMessage::FileChunk {
                id, offset, data, ..
            } => {
                format!("FileChunk: {} at {} ({} bytes)", id, offset, data.len())
            }
            P2PMessage::CallInvite {
                call_id, call_type, ..
            } => {
                format!("Call: {:?} ({})", call_type, call_id)
            }
            P2PMessage::StateSync {
                version, changes, ..
            } => {
                format!("StateSync: v{} ({} changes)", version, changes.len())
            }
            _ => format!("{:?}", content),
        }
    }
}
