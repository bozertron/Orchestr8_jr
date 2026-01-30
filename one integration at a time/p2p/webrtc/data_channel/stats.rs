use super::DataChannelState;
use libp2p::PeerId;

/// Data channel statistics
#[derive(Debug, Clone)]
pub struct DataChannelStats {
    pub label: String,
    pub peer_id: PeerId,
    pub state: DataChannelState,
    pub bytes_sent: u64,
    pub bytes_received: u64,
    pub buffer_size: usize,
    pub ordered: bool,
}
