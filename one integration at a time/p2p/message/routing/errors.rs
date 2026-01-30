/// Routing-specific errors
#[derive(Debug, thiserror::Error)]
pub enum RoutingError {
    #[error("No transport available for peer {0}")]
    NoTransportAvailable(String),
    #[error("Message delivery timeout after {0:?}")]
    DeliveryTimeout(std::time::Duration),
    #[error("Transport error: {0}")]
    TransportError(String),
    #[error("Peer not connected: {0}")]
    PeerNotConnected(String),
    #[error("Message too large: {0} bytes exceeds limit")]
    MessageTooLarge(usize),
    #[error("Retry limit exceeded: {0} attempts")]
    RetryLimitExceeded(u32),
    #[error("Invalid message format: {0}")]
    InvalidMessage(String),
}

// Removed From<RoutingError> for P2PError - convert to String directly per Pattern Bible
