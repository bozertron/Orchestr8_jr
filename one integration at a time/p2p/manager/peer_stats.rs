//! Peer Statistics Operations
//! Handles peer-specific statistics tracking and reporting

// use super::{connection::PeerConnection, stats::PeerManagerStats};
use super::stats::PeerManagerStats;

use libp2p::PeerId;
use std::collections::HashMap;

/// Peer-specific statistics operations
///
/// # Send Safety
/// This trait uses `async fn` for ergonomics. All current implementations
/// are used via concrete types (not trait objects) and do not cross thread
/// boundaries. If trait objects are needed in the future, consider desugaring
/// to `impl Future + Send` or using the `async-trait` crate.
///
/// See: docs/async-trait-analysis-2025-10-01.md for detailed analysis
#[allow(async_fn_in_trait)]
pub trait PeerStatsOps {
    async fn update_peer_stats_on_send(
        &mut self,
        peer_id: &PeerId,
        bytes: usize,
    ) -> Result<(), String>;
    async fn update_peer_stats_on_recv(
        &mut self,
        peer_id: &PeerId,
        bytes: usize,
    ) -> Result<(), String>;
    async fn get_peer_stats(&self, peer_id: &PeerId) -> Option<(u64, u64)>;
    async fn get_all_peer_stats(&self) -> HashMap<PeerId, (u64, u64)>;
    async fn reset_peer_stats(&mut self, peer_id: &PeerId) -> Result<(), String>;
}

impl PeerStatsOps for super::peer_manager::PeerManager {
    /// Update peer statistics when sending data
    async fn update_peer_stats_on_send(
        &mut self,
        peer_id: &PeerId,
        bytes: usize,
    ) -> Result<(), String> {
        if let Some(connection) = self.peers().write().await.get_mut(peer_id) {
            connection.bytes_sent += bytes as u64;
        }
        Ok(())
    }

    /// Update peer statistics when receiving data
    async fn update_peer_stats_on_recv(
        &mut self,
        peer_id: &PeerId,
        bytes: usize,
    ) -> Result<(), String> {
        if let Some(connection) = self.peers().write().await.get_mut(peer_id) {
            connection.bytes_received += bytes as u64;
        }
        Ok(())
    }

    /// Get statistics for a specific peer (bytes sent, bytes received)
    async fn get_peer_stats(&self, peer_id: &PeerId) -> Option<(u64, u64)> {
        self.peers()
            .read()
            .await
            .get(peer_id)
            .map(|conn| (conn.bytes_sent, conn.bytes_received))
    }

    /// Get statistics for all peers
    async fn get_all_peer_stats(&self) -> HashMap<PeerId, (u64, u64)> {
        self.peers()
            .read()
            .await
            .iter()
            .map(|(id, conn)| (*id, (conn.bytes_sent, conn.bytes_received)))
            .collect()
    }

    /// Reset statistics for a specific peer
    async fn reset_peer_stats(&mut self, peer_id: &PeerId) -> Result<(), String> {
        if let Some(connection) = self.peers().write().await.get_mut(peer_id) {
            connection.bytes_sent = 0;
            connection.bytes_received = 0;
        }
        Ok(())
    }
}

/// Global manager statistics operations
///
/// # Send Safety
/// This trait uses `async fn` for ergonomics. All current implementations
/// are used via concrete types (not trait objects) and do not cross thread
/// boundaries. If trait objects are needed in the future, consider desugaring
/// to `impl Future + Send` or using the `async-trait` crate.
///
/// See: docs/async-trait-analysis-2025-10-01.md for detailed analysis
#[allow(async_fn_in_trait)]
pub trait ManagerStatsOps {
    async fn increment_manager_bytes_sent(&mut self, bytes: usize);
    async fn increment_manager_bytes_received(&mut self, bytes: usize);
    async fn get_manager_stats(&self) -> PeerManagerStats;
    async fn reset_manager_stats(&mut self);
}

impl ManagerStatsOps for super::peer_manager::PeerManager {
    /// Increment global bytes sent counter
    async fn increment_manager_bytes_sent(&mut self, bytes: usize) {
        self.stats().write().await.bytes_sent += bytes as u64;
    }

    /// Increment global bytes received counter
    async fn increment_manager_bytes_received(&mut self, bytes: usize) {
        self.stats().write().await.bytes_received += bytes as u64;
    }

    /// Get global manager statistics
    async fn get_manager_stats(&self) -> PeerManagerStats {
        self.stats().read().await.clone()
    }

    /// Reset all manager statistics
    async fn reset_manager_stats(&mut self) {
        *self.stats().write().await = PeerManagerStats::default();
    }
}
