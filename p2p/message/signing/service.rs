use super::errors::SigningError;
use super::validation::SigningValidator;
use crate::p2p::message::types::*;
use crate::p2p::MessageConfig;
use chrono::Utc;
use ed25519_dalek::{Signature, Signer, SigningKey, Verifier, VerifyingKey};
use libp2p::{identity::Keypair, PeerId};
use std::sync::Arc;

/// Ed25519 message signing service for secure P2P messaging
pub struct SigningService {
    config: MessageConfig,
    keypair: Arc<Keypair>,
}

impl SigningService {
    /// Create new signing service with keypair
    pub async fn new(config: &MessageConfig, keypair: Arc<Keypair>) -> Result<Self, String> {
        Ok(Self {
            config: config.clone(),
            keypair,
        })
    }

    /// Sign P2P message with Ed25519 signature
    pub async fn sign_message(&self, message: P2PMessage) -> Result<SignedMessage, String> {
        let signing_key = self.extract_signing_key().map_err(|e| e.to_string())?;
        let timestamp = Utc::now();

        // Validate and prepare message
        SigningValidator::validate_message_size(&message, &self.config)
            .map_err(|e| e.to_string())?;
        let signature_payload = self
            .create_signature_payload(&message, &timestamp)
            .map_err(|e| e.to_string())?;

        // Generate signature
        let signature = signing_key.sign(&signature_payload);
        let public_key = signing_key.verifying_key().to_bytes().to_vec();

        Ok(SignedMessage {
            message,
            signature: signature.to_bytes().to_vec(),
            public_key,
            timestamp,
        })
    }

    /// Create signature payload from message and timestamp
    fn create_signature_payload(
        &self,
        message: &P2PMessage,
        timestamp: &chrono::DateTime<Utc>,
    ) -> Result<Vec<u8>, SigningError> {
        let message_bytes = serde_json::to_vec(message).map_err(|e| {
            SigningError::Serialization(format!("Message serialization failed: {}", e))
        })?;

        let mut signature_payload = Vec::new();
        signature_payload.extend_from_slice(&message_bytes);
        signature_payload.extend_from_slice(&timestamp.timestamp().to_le_bytes());

        Ok(signature_payload)
    }

    /// Verify Ed25519 signature and extract P2P message
    pub async fn verify_message(
        &self,
        signed_message: SignedMessage,
        from: &PeerId,
    ) -> Result<P2PMessage, String> {
        // Validate message format and identity
        self.validate_signed_message(&signed_message, from)
            .map_err(|e| e.to_string())?;

        // Reconstruct and verify signature
        let signature_payload = self
            .create_signature_payload(&signed_message.message, &signed_message.timestamp)
            .map_err(|e| e.to_string())?;
        self.verify_ed25519_signature(&signed_message, &signature_payload)
            .map_err(|e| e.to_string())?;

        Ok(signed_message.message)
    }

    /// Validate signed message format and identity
    fn validate_signed_message(
        &self,
        signed_message: &SignedMessage,
        from: &PeerId,
    ) -> Result<(), SigningError> {
        SigningValidator::validate_timestamp(&signed_message.timestamp)
            .map_err(|e| SigningError::ReplayAttack(e))?;
        SigningValidator::validate_signature_format(
            &signed_message.signature,
            &signed_message.public_key,
        )?;
        SigningValidator::verify_peer_identity(&signed_message.public_key, from)
            .map_err(|e| SigningError::SignatureVerification(e))?;
        Ok(())
    }

    /// Verify Ed25519 signature against payload
    fn verify_ed25519_signature(
        &self,
        signed_message: &SignedMessage,
        signature_payload: &[u8],
    ) -> Result<(), SigningError> {
        // Convert Vec<u8> to [u8; 64] for signature
        let signature_bytes: [u8; 64] =
            signed_message.signature.clone().try_into().map_err(|_| {
                SigningError::SignatureVerification("Invalid signature format".to_string())
            })?;
        let signature = Signature::from_bytes(&signature_bytes);

        // Convert Vec<u8> to [u8; 32] for public key
        let public_key_bytes: [u8; 32] =
            signed_message.public_key.clone().try_into().map_err(|_| {
                SigningError::SignatureVerification("Invalid public key format".to_string())
            })?;
        let verifying_key = VerifyingKey::from_bytes(&public_key_bytes).map_err(|e| {
            SigningError::SignatureVerification(format!("Invalid public key: {}", e))
        })?;

        verifying_key
            .verify(signature_payload, &signature)
            .map_err(|e| {
                SigningError::SignatureVerification(format!("Signature verification failed: {}", e))
            })?;

        Ok(())
    }

    /// Extract Ed25519 signing key from libp2p keypair
    fn extract_signing_key(&self) -> Result<SigningKey, SigningError> {
        // Get the protobuf encoding to extract the raw key bytes
        let protobuf_bytes = self
            .keypair
            .to_protobuf_encoding()
            .map_err(|e| SigningError::KeyExtraction(format!("Failed to encode keypair: {}", e)))?;

        // libp2p Ed25519 protobuf format (verified via debug tests):
        // - Byte 0: 0x08 (field number 1, wire type 0)
        // - Byte 1: 0x01 (key type = Ed25519)
        // - Byte 2: 0x12 (field number 2, wire type 2 = length-delimited)
        // - Byte 3: 0x40 (length = 64 bytes for key data)
        // - Bytes 4-35: 32-byte secret key
        // - Bytes 36-67: 32-byte public key

        if protobuf_bytes.len() < 36 {
            return Err(SigningError::KeyExtraction(format!(
                "Protobuf encoding too short: {} bytes (expected at least 36)",
                protobuf_bytes.len()
            )));
        }

        // Extract the 32-byte secret key (bytes 4-35, offset 4)
        let secret_bytes = &protobuf_bytes[4..36];

        // Create ed25519-dalek SigningKey from the secret bytes
        SigningKey::try_from(secret_bytes).map_err(|e| {
            SigningError::KeyExtraction(format!("Failed to create signing key: {}", e))
        })
    }
}
