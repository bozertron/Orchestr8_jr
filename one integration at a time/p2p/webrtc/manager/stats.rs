/// Manager statistics
#[derive(Debug, Clone, Default)]
pub struct ManagerStats {
    pub total_connections: u64,
    pub failed_connections: u64,
    pub bytes_sent: u64,
    pub bytes_received: u64,
    pub ice_candidates_gathered: u64,
}
