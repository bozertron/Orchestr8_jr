/// Signing-specific errors
#[derive(Debug, thiserror::Error)]
pub enum SigningError {
    #[error("Key extraction failed: {0}")]
    KeyExtraction(String),
    #[error("Signature generation failed: {0}")]
    SignatureGeneration(String),
    #[error("Signature verification failed: {0}")]
    SignatureVerification(String),
    #[error("Message serialization failed: {0}")]
    Serialization(String),
    #[error("Invalid timestamp: {0}")]
    InvalidTimestamp(String),
    #[error("Replay attack detected: {0}")]
    ReplayAttack(String),
}

// Removed From<SigningError> for P2PError - convert to String directly per Pattern Bible
