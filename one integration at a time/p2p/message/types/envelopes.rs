use super::core::P2PMessage;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

/// Signed message envelope
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SignedMessage {
    pub message: P2PMessage,
    pub signature: Vec<u8>,
    pub public_key: Vec<u8>,
    pub timestamp: DateTime<Utc>,
}

/// Encrypted message envelope
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EncryptedMessage {
    pub nonce: Vec<u8>,
    pub ciphertext: Vec<u8>,
    pub sender_public_key: Vec<u8>,
}
