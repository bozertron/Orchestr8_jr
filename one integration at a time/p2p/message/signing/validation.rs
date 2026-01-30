use super::errors::SigningError;
use crate::p2p::message::types::P2PMessage;
use crate::p2p::MessageConfig;
use chrono::{DateTime, Utc};
use libp2p::PeerId;

/// Validation utilities for message signing
pub struct SigningValidator;

impl SigningValidator {
    /// Validate message size constraints
    pub fn validate_message_size(
        message: &P2PMessage,
        config: &MessageConfig,
    ) -> Result<(), SigningError> {
        let serialized_size = serde_json::to_vec(message)
            .map_err(|e| SigningError::Serialization(format!("Size validation failed: {}", e)))?
            .len();

        if serialized_size > config.max_message_size {
            return Err(SigningError::SignatureGeneration(format!(
                "Message size {} exceeds maximum {}",
                serialized_size, config.max_message_size
            )));
        }

        Ok(())
    }

    /// Validate timestamp to prevent replay attacks
    pub fn validate_timestamp(timestamp: &DateTime<Utc>) -> Result<(), String> {
        let now = Utc::now();
        let age = now.signed_duration_since(*timestamp);

        // Reject messages older than 5 minutes
        if age.num_seconds() > 300 {
            return Err(format!(
                "Message timestamp too old: {} seconds",
                age.num_seconds()
            ));
        }

        // Reject messages from the future (allow 30 second clock skew)
        if age.num_seconds() < -30 {
            return Err(format!(
                "Message timestamp from future: {} seconds",
                -age.num_seconds()
            ));
        }

        Ok(())
    }

    /// Verify peer identity matches public key
    pub fn verify_peer_identity(public_key: &[u8], peer_id: &PeerId) -> Result<(), String> {
        // Create libp2p public key from Ed25519 bytes
        let ed25519_public = libp2p::identity::ed25519::PublicKey::try_from_bytes(public_key)
            .map_err(|e| format!("Invalid Ed25519 public key: {}", e))?;

        let libp2p_public = libp2p::identity::PublicKey::from(ed25519_public);
        let expected_peer_id = PeerId::from(libp2p_public);

        if expected_peer_id != *peer_id {
            return Err(format!(
                "Peer ID mismatch: expected {}, got {}",
                expected_peer_id, peer_id
            ));
        }

        Ok(())
    }

    /// Validate signature and public key lengths
    pub fn validate_signature_format(
        signature: &[u8],
        public_key: &[u8],
    ) -> Result<(), SigningError> {
        // Validate signature length
        if signature.len() != 64 {
            return Err(SigningError::SignatureVerification(
                "Invalid signature length, expected 64 bytes".to_string(),
            ));
        }

        // Validate public key length
        if public_key.len() != 32 {
            return Err(SigningError::SignatureVerification(
                "Invalid public key length, expected 32 bytes".to_string(),
            ));
        }

        Ok(())
    }
}
