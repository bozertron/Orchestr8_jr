use super::types::*;
use crate::p2p::MessageConfig;
use chacha20poly1305::Nonce;
use libp2p::{identity::Keypair, PeerId};
use std::sync::Arc;

/// ChaCha20-Poly1305 encryption service for secure P2P messaging
pub struct EncryptionService {
    config: MessageConfig,
    key_manager: super::encryption_keys::EncryptionKeyManager,
}

/// Encryption-specific errors
#[derive(Debug, thiserror::Error)]
pub enum EncryptionError {
    #[error("Key derivation failed: {0}")]
    KeyDerivation(String),
    #[error("Encryption failed: {0}")]
    Encryption(String),
    #[error("Decryption failed: {0}")]
    Decryption(String),
    #[error("Invalid nonce: {0}")]
    InvalidNonce(String),
}

// Removed From<EncryptionError> for P2PError - convert to String directly per Pattern Bible

impl EncryptionService {
    /// Create new encryption service with keypair
    pub async fn new(config: &MessageConfig, keypair: Arc<Keypair>) -> Result<Self, String> {
        let key_manager = super::encryption_keys::EncryptionKeyManager::new(keypair);

        Ok(Self {
            config: config.clone(),
            key_manager,
        })
    }

    /// Encrypt signed message for specific peer
    pub async fn encrypt_message(
        &self,
        message: SignedMessage,
        to: &PeerId,
    ) -> Result<EncryptedMessage, String> {
        let plaintext = super::encryption_keys::EncryptionUtils::serialize_and_validate_message(
            &message,
            self.config.max_message_size,
        )?;

        let nonce = super::encryption_keys::EncryptionKeyManager::generate_nonce()?;
        let encryption_key = self.key_manager.derive_message_key(to, &nonce).await?;
        let ciphertext = super::encryption_keys::EncryptionUtils::perform_encryption(
            &plaintext,
            &nonce,
            &encryption_key,
        )?;

        Ok(EncryptedMessage {
            nonce: nonce.to_vec(),
            ciphertext,
            sender_public_key: vec![], // Will be set by caller if needed
        })
    }

    /// Decrypt message from specific peer
    pub async fn decrypt_message(
        &self,
        encrypted_message: EncryptedMessage,
        from: &PeerId,
    ) -> Result<SignedMessage, String> {
        // Validate nonce length
        if encrypted_message.nonce.len() != 12 {
            return Err(
                EncryptionError::InvalidNonce("Nonce must be 12 bytes".to_string()).to_string(),
            );
        }

        // Convert nonce
        let nonce = Nonce::from_slice(&encrypted_message.nonce);

        // Derive decryption key for this peer using key manager
        let decryption_key = self.key_manager.derive_message_key(from, &nonce).await?;

        // Decrypt with ChaCha20-Poly1305 AEAD using utility function
        let plaintext =
            self.perform_decryption(&encrypted_message.ciphertext, &nonce, &decryption_key)?;

        // Deserialize the signed message
        let signed_message: SignedMessage = match serde_json::from_slice(&plaintext) {
            Ok(msg) => msg,
            Err(e) => {
                return Err(format!(
                    "{}",
                    EncryptionError::Decryption(format!("Deserialization failed: {}", e))
                ))
            }
        };

        Ok(signed_message)
    }

    /// Perform ChaCha20-Poly1305 decryption
    fn perform_decryption(
        &self,
        ciphertext: &[u8],
        nonce: &Nonce,
        key: &[u8; 32],
    ) -> Result<Vec<u8>, String> {
        use chacha20poly1305::{aead::Aead, aead::KeyInit, ChaCha20Poly1305};

        let cipher = ChaCha20Poly1305::new(key.into());
        cipher.decrypt(nonce, ciphertext).map_err(|e| {
            format!(
                "{}",
                EncryptionError::Decryption(format!("AEAD decryption failed: {}", e))
            )
        })
    }

    /// Clear key cache (for security)
    pub async fn clear_key_cache(&self) {
        self.key_manager.clear_key_cache().await;
    }
}
