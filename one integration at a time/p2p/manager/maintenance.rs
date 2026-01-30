use super::{ConnectionStatus, PeerConnection};
use crate::p2p::{NetworkConfig, P2PEvent};
use libp2p::PeerId;
use std::collections::HashMap;
use std::sync::Arc;
use std::time::Instant;
use tokio::sync::{mpsc, RwLock};

/// Start maintenance task for peer connections
pub async fn start_maintenance_task(
    peers: Arc<RwLock<HashMap<PeerId, PeerConnection>>>,
    config: NetworkConfig,
    event_sender: mpsc::UnboundedSender<P2PEvent>,
) {
    tokio::spawn(async move {
        let mut interval = tokio::time::interval(config.ping_interval);

        loop {
            interval.tick().await;
            perform_maintenance_cycle(&peers, &config, &event_sender).await;
        }
    });
}

/// Perform a single maintenance cycle
async fn perform_maintenance_cycle(
    peers: &Arc<RwLock<HashMap<PeerId, PeerConnection>>>,
    config: &NetworkConfig,
    event_sender: &mpsc::UnboundedSender<P2PEvent>,
) {
    let mut peers_to_remove = Vec::new();
    let mut peers_guard = peers.write().await;

    check_peer_connections(&mut peers_guard, config, &mut peers_to_remove);
    remove_stale_peers(&mut peers_guard, peers_to_remove, event_sender);
}

/// Check peer connections and identify stale ones
fn check_peer_connections(
    peers_guard: &mut HashMap<PeerId, PeerConnection>,
    config: &NetworkConfig,
    peers_to_remove: &mut Vec<PeerId>,
) {
    for (peer_id, connection) in peers_guard.iter_mut() {
        if connection.last_seen.elapsed() > config.connection_timeout {
            connection.status = ConnectionStatus::Disconnected;
            peers_to_remove.push(*peer_id);
        } else if connection.status == ConnectionStatus::Connected {
            connection.last_seen = Instant::now();
        }
    }
}

/// Remove stale peers and send disconnect events
fn remove_stale_peers(
    peers_guard: &mut HashMap<PeerId, PeerConnection>,
    peers_to_remove: Vec<PeerId>,
    event_sender: &mpsc::UnboundedSender<P2PEvent>,
) {
    for peer_id in peers_to_remove {
        peers_guard.remove(&peer_id);
        let _ = event_sender.send(P2PEvent::PeerDisconnected { peer_id });
    }
}
