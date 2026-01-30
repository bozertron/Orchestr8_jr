use super::super::types::*;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

/// Pending confirmation tracking
#[derive(Debug, Clone)]
pub struct PendingConfirmation {
    pub message_id: MessageId,
    pub sent_at: DateTime<Utc>,
    pub retry_count: u32,
}

/// File transfer state
#[derive(Debug, Clone)]
pub struct FileTransferState {
    pub transfer_id: TransferId,
    pub filename: String,
    pub total_size: u64,
    pub received_bytes: u64,
    pub status: TransferStatus,
}

/// File transfer status
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum TransferStatus {
    Offered,
    Accepted,
    InProgress,
    Complete,
    Cancelled,
    Failed(String),
}

/// Call state
#[derive(Debug, Clone)]
pub struct CallState {
    pub call_id: CallId,
    pub call_type: CallType,
    pub status: CallStatus,
}

/// Call status
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum CallStatus {
    Incoming,
    Outgoing,
    Active,
    Declined,
    Ended,
}
