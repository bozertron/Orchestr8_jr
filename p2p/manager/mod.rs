// Hyper-modular peer manager following Pattern Bible architecture constraints
// Split into focused modules: ≤100 lines each, single responsibility pattern

pub mod connection;
pub mod maintenance;
pub mod peer_manager;
pub mod peer_ops;
pub mod peer_stats;
pub mod stats;

// Re-exports following hyper-modular pattern
pub use connection::{ConnectionStatus, PeerConnection};
pub use peer_manager::PeerManager;
pub use peer_ops::PeerOperations;
pub use peer_stats::{ManagerStatsOps, PeerStatsOps};
pub use stats::PeerManagerStats;
