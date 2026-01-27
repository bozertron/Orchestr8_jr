/// P2P network errors
#[derive(Debug, thiserror::Error)]
pub enum P2PError {
    #[error("Transport error: {0}")]
    Transport(String),

    #[error("Discovery error: {0}")]
    Discovery(String),

    #[error("Connection error: {0}")]
    Connection(String),

    #[error("Configuration error: {0}")]
    Config(String),

    #[error("Invalid message: {0}")]
    InvalidMessage(String),

    #[error("Serialization error: {0}")]
    Serialization(String),

    #[error("Storage error: {0}")]
    Storage(String),

    #[error("Persistence error: {0}")]
    PersistenceError(String),

    #[error("Not found: {0}")]
    NotFound(String),

    #[error("Not initialized: {0}")]
    NotInitialized(String),

    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Anyhow error: {0}")]
    Anyhow(#[from] anyhow::Error),
}

// Removed recursive type alias - use std::result::Result<T, String> directly per Pattern Bible
