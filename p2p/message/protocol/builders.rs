use super::super::types::*;
use chrono::Utc;
use uuid::Uuid;

/// Message builders for creating protocol messages
pub struct MessageBuilders;

impl MessageBuilders {
    /// Create a new chat message
    pub fn create_chat_message(text: String, reply_to: Option<MessageId>) -> P2PMessage {
        P2PMessage::Chat {
            id: Uuid::new_v4(),
            text,
            timestamp: Utc::now(),
            reply_to,
        }
    }

    /// Create a new file offer
    pub fn create_file_offer(
        name: String,
        size: u64,
        hash: Vec<u8>,
        mime_type: Option<String>,
    ) -> P2PMessage {
        P2PMessage::FileOffer {
            id: Uuid::new_v4(),
            name,
            size,
            hash,
            mime_type,
        }
    }

    /// Create a call invite
    pub fn create_call_invite(call_type: CallType, sdp_offer: String) -> P2PMessage {
        P2PMessage::CallInvite {
            call_id: Uuid::new_v4(),
            call_type,
            sdp_offer,
        }
    }

    /// Create a ping message
    pub fn create_ping() -> P2PMessage {
        P2PMessage::Ping {
            nonce: rand::random(),
            timestamp: Utc::now(),
        }
    }

    /// Create a pong response
    pub fn create_pong(nonce: u64) -> P2PMessage {
        P2PMessage::Pong {
            nonce,
            timestamp: Utc::now(),
        }
    }

    /// Create delivery confirmation
    pub fn create_delivery_confirmation(message_id: MessageId) -> P2PMessage {
        P2PMessage::DeliveryConfirmation {
            message_id,
            timestamp: Utc::now(),
        }
    }
}
