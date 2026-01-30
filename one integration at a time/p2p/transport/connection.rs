use libp2p::PeerId;
use std::time::{Duration, Instant};

/// Transport statistics
#[derive(Debug, Clone)]
pub struct TransportStats {
    pub peer_id: PeerId,
    pub active_connections: usize,
    pub pending_connections: usize,
    pub bytes_sent: u64,
    pub bytes_received: u64,
}

/// Transport connection info
#[derive(Debug, Clone)]
pub struct ConnectionInfo {
    pub peer_id: PeerId,
    pub local_addr: libp2p::Multiaddr,
    pub remote_addr: libp2p::Multiaddr,
    pub established_at: Instant,
    pub protocol: String,
}

impl ConnectionInfo {
    /// Create new connection info
    pub fn new(
        peer_id: PeerId,
        local_addr: libp2p::Multiaddr,
        remote_addr: libp2p::Multiaddr,
        protocol: String,
    ) -> Self {
        Self {
            peer_id,
            local_addr,
            remote_addr,
            established_at: Instant::now(),
            protocol,
        }
    }

    /// Get connection duration
    pub fn duration(&self) -> Duration {
        self.established_at.elapsed()
    }

    /// Check if connection is local
    pub fn is_local(&self) -> bool {
        self.remote_addr.to_string().contains("127.0.0.1")
            || self.remote_addr.to_string().contains("::1")
            || self.remote_addr.to_string().contains("192.168.")
            || self.remote_addr.to_string().contains("10.")
            || self.remote_addr.to_string().contains("172.")
    }
}
