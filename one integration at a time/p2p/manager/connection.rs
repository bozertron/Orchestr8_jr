use libp2p::{Multiaddr, PeerId};
use std::time::{Duration, Instant};

/// Individual peer connection
#[derive(Debug, Clone)]
pub struct PeerConnection {
    pub peer_id: PeerId,
    pub address: Multiaddr,
    pub connected_at: Instant,
    pub last_seen: Instant,
    pub status: ConnectionStatus,
    pub bytes_sent: u64,
    pub bytes_received: u64,
    pub ping_rtt: Option<Duration>,
}

/// Connection status
#[derive(Debug, Clone, PartialEq)]
pub enum ConnectionStatus {
    Connecting,
    Connected,
    Disconnected,
    Failed(String),
}

impl PeerConnection {
    /// Check if connection is alive
    pub fn is_alive(&self) -> bool {
        matches!(self.status, ConnectionStatus::Connected)
            && self.last_seen.elapsed() < Duration::from_secs(60)
    }

    /// Get connection duration
    pub fn duration(&self) -> Duration {
        self.connected_at.elapsed()
    }

    /// Update ping RTT
    pub fn update_ping(&mut self, rtt: Duration) {
        self.ping_rtt = Some(rtt);
        self.last_seen = Instant::now();
    }
}
