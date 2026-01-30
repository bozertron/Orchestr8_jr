//! Peer Operations - Connection Lifecycle and Messaging
//! Handles peer connection, disconnection, and message operations

use super::{connection::PeerConnection, peer_manager::PeerManager};
use crate::p2p::P2PEvent;
use libp2p::{Multiaddr, PeerId};
use std::collections::HashMap;
use std::time::{Duration, Instant};

/// Peer operations trait for connection lifecycle
///
/// # Send Safety
/// This trait uses `async fn` for ergonomics. All current implementations
/// are used via concrete types (not trait objects) and do not cross thread
/// boundaries. If trait objects are needed in the future, consider desugaring
/// to `impl Future + Send` or using the `async-trait` crate.
///
/// See: docs/async-trait-analysis-2025-10-01.md for detailed analysis
#[allow(async_fn_in_trait)]
pub trait PeerOperations {
    async fn connect_peer(&mut self, peer_id: PeerId, address: Multiaddr) -> Result<(), String>;
    async fn disconnect_peer(&mut self, peer_id: PeerId) -> Result<(), String>;
    async fn send_message(&mut self, peer_id: PeerId, data: Vec<u8>) -> Result<(), String>;
    async fn handle_message(&mut self, peer_id: PeerId, data: Vec<u8>) -> Result<(), String>;
    async fn connected_peers(&self) -> HashMap<PeerId, PeerConnection>;
    async fn peer_count(&self) -> usize;
    async fn bytes_sent(&self) -> u64;
    async fn bytes_received(&self) -> u64;
}

impl PeerOperations for PeerManager {
    /// Connect to a peer
    async fn connect_peer(&mut self, peer_id: PeerId, address: Multiaddr) -> Result<(), String> {
        let connection = self.create_peer_connection(peer_id, address);
        self.peers().write().await.insert(peer_id, connection);
        self.start_connection_process(peer_id).await;
        Ok(())
    }

    /// Disconnect from a peer
    async fn disconnect_peer(&mut self, peer_id: PeerId) -> Result<(), String> {
        if let Some(connection) = self.peers().write().await.get_mut(&peer_id) {
            connection.status = super::connection::ConnectionStatus::Disconnected;
            self.event_sender()
                .send(P2PEvent::PeerDisconnected { peer_id })
                .map_err(|_| format!("Connection: {}", "Failed to send event".to_string()))?;
        }
        Ok(())
    }

    /// Send message to peer
    async fn send_message(&mut self, peer_id: PeerId, data: Vec<u8>) -> Result<(), String> {
        let mut peers = self.peers().write().await;
        if let Some(connection) = peers.get_mut(&peer_id) {
            if connection.status == super::connection::ConnectionStatus::Connected {
                connection.bytes_sent += data.len() as u64;
                connection.last_seen = Instant::now();

                // Update stats
                let mut stats = self.stats().write().await;
                stats.bytes_sent += data.len() as u64;

                // In a real implementation, this would send via libp2p
                return Ok(());
            }
        }

        Err(format!(
            "Connection: {}",
            format!("Peer {} not connected", peer_id)
        ))
    }

    /// Handle received message
    async fn handle_message(&mut self, peer_id: PeerId, data: Vec<u8>) -> Result<(), String> {
        let mut peers = self.peers().write().await;
        if let Some(connection) = peers.get_mut(&peer_id) {
            connection.bytes_received += data.len() as u64;
            connection.last_seen = Instant::now();

            // Update stats
            let mut stats = self.stats().write().await;
            stats.bytes_received += data.len() as u64;

            self.event_sender()
                .send(P2PEvent::MessageReceived {
                    from: peer_id,
                    data,
                })
                .map_err(|_| format!("Connection: {}", "Failed to send event".to_string()))?;
        }

        Ok(())
    }

    /// Get connected peers
    async fn connected_peers(&self) -> HashMap<PeerId, PeerConnection> {
        self.peers()
            .read()
            .await
            .iter()
            .filter(|(_, conn)| conn.status == super::connection::ConnectionStatus::Connected)
            .map(|(id, conn)| (*id, conn.clone()))
            .collect()
    }

    /// Get peer count
    async fn peer_count(&self) -> usize {
        self.peers()
            .read()
            .await
            .values()
            .filter(|conn| conn.status == super::connection::ConnectionStatus::Connected)
            .count()
    }

    /// Get bytes sent
    async fn bytes_sent(&self) -> u64 {
        self.stats().read().await.bytes_sent
    }

    /// Get bytes received
    async fn bytes_received(&self) -> u64 {
        self.stats().read().await.bytes_received
    }
}

/// Private implementation details for PeerManager
impl PeerManager {
    /// Create a new peer connection
    fn create_peer_connection(
        &self,
        peer_id: PeerId,
        address: Multiaddr,
    ) -> super::connection::PeerConnection {
        super::connection::PeerConnection {
            peer_id,
            address,
            connected_at: Instant::now(),
            last_seen: Instant::now(),
            status: super::connection::ConnectionStatus::Connecting,
            bytes_sent: 0,
            bytes_received: 0,
            ping_rtt: None,
        }
    }

    /// Start connection process for a peer
    async fn start_connection_process(&self, peer_id: PeerId) {
        let event_sender = self.event_sender().clone();
        let peers = self.peers().clone();

        tokio::spawn(async move {
            tokio::time::sleep(Duration::from_millis(100)).await;

            if let Some(connection) = peers.write().await.get_mut(&peer_id) {
                connection.status = super::connection::ConnectionStatus::Connected;
                let _ = event_sender.send(P2PEvent::PeerConnected { peer_id });
            }
        });
    }
}
