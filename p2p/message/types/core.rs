use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

/// Unique message identifier
pub type MessageId = Uuid;

/// Unique transfer identifier for file transfers
pub type TransferId = Uuid;

/// Unique call identifier for voice/video calls
pub type CallId = Uuid;

/// P2P message protocol
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum P2PMessage {
    /// Chat messages
    Chat {
        id: MessageId,
        text: String,
        timestamp: DateTime<Utc>,
        reply_to: Option<MessageId>,
    },

    /// File transfer messages
    FileOffer {
        id: TransferId,
        name: String,
        size: u64,
        hash: Vec<u8>,
        mime_type: Option<String>,
    },
    FileChunk {
        id: TransferId,
        offset: u64,
        data: Vec<u8>,
    },
    FileComplete {
        id: TransferId,
    },
    FileCancel {
        id: TransferId,
        reason: String,
    },

    /// Voice/Video call signaling
    CallInvite {
        call_id: CallId,
        call_type: CallType,
        sdp_offer: String,
    },
    CallAnswer {
        call_id: CallId,
        accepted: bool,
        sdp_answer: Option<String>,
    },
    CallHangup {
        call_id: CallId,
        reason: HangupReason,
    },
    CallIceCandidate {
        call_id: CallId,
        candidate: String,
    },

    /// State synchronization messages
    StateSync {
        version: u64,
        changes: Vec<StateChange>,
    },
    StateSyncRequest {
        from_version: u64,
    },
    StateSyncResponse {
        from_version: u64,
        to_version: u64,
        changes: Vec<StateChange>,
    },

    /// Control messages
    Ping {
        nonce: u64,
        timestamp: DateTime<Utc>,
    },
    Pong {
        nonce: u64,
        timestamp: DateTime<Utc>,
    },
    DeliveryConfirmation {
        message_id: MessageId,
        timestamp: DateTime<Utc>,
    },
    TypingIndicator {
        typing: bool,
    },
}

impl P2PMessage {
    /// Get message ID if available
    pub fn message_id(&self) -> Option<MessageId> {
        match self {
            P2PMessage::Chat { id, .. } => Some(*id),
            P2PMessage::DeliveryConfirmation { message_id, .. } => Some(*message_id),
            _ => None,
        }
    }

    /// Get timestamp if available
    pub fn timestamp(&self) -> Option<DateTime<Utc>> {
        match self {
            P2PMessage::Chat { timestamp, .. } => Some(*timestamp),
            P2PMessage::Ping { timestamp, .. } => Some(*timestamp),
            P2PMessage::Pong { timestamp, .. } => Some(*timestamp),
            P2PMessage::DeliveryConfirmation { timestamp, .. } => Some(*timestamp),
            _ => None,
        }
    }

    /// Check if message requires delivery confirmation
    pub fn requires_confirmation(&self) -> bool {
        matches!(self, P2PMessage::Chat { .. } | P2PMessage::FileOffer { .. })
    }

    /// Get message type as string
    pub fn message_type(&self) -> &'static str {
        match self {
            P2PMessage::Chat { .. } => "chat",
            P2PMessage::FileOffer { .. } => "file_offer",
            P2PMessage::FileChunk { .. } => "file_chunk",
            P2PMessage::FileComplete { .. } => "file_complete",
            P2PMessage::FileCancel { .. } => "file_cancel",
            P2PMessage::CallInvite { .. } => "call_invite",
            P2PMessage::CallAnswer { .. } => "call_answer",
            P2PMessage::CallHangup { .. } => "call_hangup",
            P2PMessage::CallIceCandidate { .. } => "call_ice_candidate",
            P2PMessage::StateSync { .. } => "state_sync",
            P2PMessage::StateSyncRequest { .. } => "state_sync_request",
            P2PMessage::StateSyncResponse { .. } => "state_sync_response",
            P2PMessage::Ping { .. } => "ping",
            P2PMessage::Pong { .. } => "pong",
            P2PMessage::DeliveryConfirmation { .. } => "delivery_confirmation",
            P2PMessage::TypingIndicator { .. } => "typing_indicator",
        }
    }
}

/// Call types for voice/video communication
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum CallType {
    Audio,
    Video,
    ScreenShare,
}

/// Reasons for call hangup
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum HangupReason {
    UserHangup,
    NetworkError,
    Timeout,
    Busy,
    Declined,
}

/// State change for CRDT synchronization
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StateChange {
    pub id: Uuid,
    pub timestamp: DateTime<Utc>,
    pub operation: StateOperation,
    pub data: Vec<u8>,
}

/// State operations for CRDT
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum StateOperation {
    Insert { position: u64 },
    Delete { position: u64, length: u64 },
    Update { position: u64, length: u64 },
}
