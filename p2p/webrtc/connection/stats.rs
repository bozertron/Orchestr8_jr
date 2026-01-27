use super::state::ConnectionState;
use libp2p::PeerId;
use std::time::Instant;

/// Connection statistics
#[derive(Debug, Clone)]
pub struct ConnectionStats {
    pub peer_id: PeerId,
    pub state: ConnectionState,
    pub data_channels: usize,
    pub created_at: Instant,
    pub bytes_sent: u64,
    pub bytes_received: u64,
}
