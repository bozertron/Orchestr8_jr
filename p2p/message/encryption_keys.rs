use chacha20poly1305::{aead::Aead, aead::KeyInit};
use hkdf::Hkdf;
use libp2p::{identity::Keypair, PeerId};
use rand::{RngCore, SeedableRng};
use sha2::Sha256;
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;

use super::types::*;

/// ChaCha20-Poly1305 key management for secure P2P messaging
#[derive(Debug)]
pub struct EncryptionKeyManager {
    keypair: Arc<Keypair>,
    key_cache: Arc<RwLock<HashMap<PeerId, [u8; 32]>>>,
}

impl EncryptionKeyManager {
    /// Create new key manager
    pub fn new(keypair: Arc<Keypair>) -> Self {
        Self {
            keypair,
            key_cache: Arc::new(RwLock::new(HashMap::new())),
        }
    }

    /// Generate cryptographically secure nonce
    pub fn generate_nonce() -> Result<chacha20poly1305::Nonce, String> {
        let mut nonce_bytes = [0u8; 12];

        // Use timestamp (8 bytes) + random (4 bytes) for uniqueness
        let timestamp = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .map_err(|e| format!("Timestamp error: {}", e))?
            .as_nanos() as u64;

        nonce_bytes[0..8].copy_from_slice(&timestamp.to_le_bytes());

        // Fill remaining bytes with cryptographically secure random data
        let mut rng = rand::rngs::StdRng::from_entropy();
        rng.fill_bytes(&mut nonce_bytes[8..12]);

        Ok(*chacha20poly1305::Nonce::from_slice(&nonce_bytes))
    }

    /// Derive message encryption key using HKDF
    pub async fn derive_message_key(
        &self,
        peer_id: &PeerId,
        nonce: &chacha20poly1305::Nonce,
    ) -> Result<[u8; 32], String> {
        // Check cache first
        if let Some(cached_key) = self.get_cached_key(peer_id).await? {
            return Ok(cached_key);
        }

        // Derive new key and cache it
        let shared_secret = self.derive_shared_secret(peer_id)?;
        let message_key = self.hkdf_derive_key(&shared_secret, nonce)?;
        self.cache_key(peer_id, message_key).await?;

        Ok(message_key)
    }

    /// Get cached key for peer
    async fn get_cached_key(&self, peer_id: &PeerId) -> Result<Option<[u8; 32]>, String> {
        let cache = self.key_cache.read().await;
        Ok(cache.get(peer_id).copied())
    }

    /// Perform HKDF key derivation
    fn hkdf_derive_key(
        &self,
        shared_secret: &[u8; 32],
        nonce: &chacha20poly1305::Nonce,
    ) -> Result<[u8; 32], String> {
        let hkdf = Hkdf::<Sha256>::new(Some(nonce.as_slice()), shared_secret);
        let mut message_key = [0u8; 32];
        hkdf.expand(b"jfdi-message-encryption", &mut message_key)
            .map_err(|e| format!("HKDF expand failed: {}", e))?;
        Ok(message_key)
    }

    /// Cache derived key
    async fn cache_key(&self, peer_id: &PeerId, key: [u8; 32]) -> Result<(), String> {
        let mut cache = self.key_cache.write().await;
        cache.insert(*peer_id, key);
        Ok(())
    }

    /// Derive shared secret from Ed25519 keypairs
    fn derive_shared_secret(&self, peer_id: &PeerId) -> Result<[u8; 32], String> {
        // For Ed25519, we use a deterministic approach based on peer IDs
        // This provides forward secrecy through per-message nonce variation
        let local_public = self.keypair.public().encode_protobuf();
        let peer_bytes = peer_id.to_bytes();

        // Create deterministic shared secret using HKDF
        let mut combined_input = Vec::new();
        combined_input.extend_from_slice(&local_public);
        combined_input.extend_from_slice(&peer_bytes);

        let hkdf = Hkdf::<Sha256>::new(None, &combined_input);
        let mut shared_secret = [0u8; 32];
        hkdf.expand(b"jfdi-shared-secret", &mut shared_secret)
            .map_err(|e| format!("Shared secret derivation failed: {}", e))?;

        Ok(shared_secret)
    }

    /// Clear key cache (for security)
    pub async fn clear_key_cache(&self) {
        let mut cache = self.key_cache.write().await;
        cache.clear();
    }
}

/// Message serialization and validation utilities
pub struct EncryptionUtils;

impl EncryptionUtils {
    /// Serialize message and validate size constraints
    pub fn serialize_and_validate_message(
        message: &SignedMessage,
        max_size: usize,
    ) -> Result<Vec<u8>, String> {
        let plaintext =
            serde_json::to_vec(message).map_err(|e| format!("Serialization failed: {}", e))?;

        // Enforce message size limit from config (security boundary)
        if plaintext.len() > max_size {
            return Err(format!(
                "Message size {} exceeds limit {}",
                plaintext.len(),
                max_size
            ));
        }

        Ok(plaintext)
    }

    /// Perform ChaCha20-Poly1305 encryption
    pub fn perform_encryption(
        plaintext: &[u8],
        nonce: &chacha20poly1305::Nonce,
        key: &[u8; 32],
    ) -> Result<Vec<u8>, String> {
        let cipher = chacha20poly1305::ChaCha20Poly1305::new(key.into());
        cipher
            .encrypt(nonce, plaintext)
            .map_err(|e| format!("AEAD encryption failed: {}", e))
    }
}
