use std::time::Duration;

/// Peer manager statistics
#[derive(Debug, Clone, Default)]
pub struct PeerManagerStats {
    pub total_connections: u64,
    pub failed_connections: u64,
    pub bytes_sent: u64,
    pub bytes_received: u64,
    pub average_ping: Option<Duration>,
}
