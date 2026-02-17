use super::super::connection::{ConnectionState, WebRtcConnection};
use libp2p::PeerId;
use std::collections::HashMap;
use std::sync::Arc;
use std::time::Duration;
use tokio::sync::{mpsc, RwLock};

/// Start maintenance task for WebRTC connections
pub async fn start_maintenance_task(
    connections: Arc<RwLock<HashMap<PeerId, WebRtcConnection>>>,
    event_sender: mpsc::UnboundedSender<super::super::WebRtcEvent>,
    keep_alive_interval: Duration,
) {
    tokio::spawn(async move {
        let mut interval = tokio::time::interval(keep_alive_interval);

        loop {
            interval.tick().await;
            cleanup_failed_connections(&connections, &event_sender).await;
        }
    });
}

/// Clean up failed and closed connections
async fn cleanup_failed_connections(
    connections: &Arc<RwLock<HashMap<PeerId, WebRtcConnection>>>,
    event_sender: &mpsc::UnboundedSender<super::super::WebRtcEvent>,
) {
    let to_remove = find_failed_connections(connections).await;
    remove_failed_connections(connections, event_sender, to_remove).await;
}

/// Find connections that need to be removed
async fn find_failed_connections(
    connections: &Arc<RwLock<HashMap<PeerId, WebRtcConnection>>>,
) -> Vec<PeerId> {
    let mut to_remove = Vec::new();
    let connections_guard = connections.read().await;

    for (peer_id, connection) in connections_guard.iter() {
        let state = connection.state().await;
        if state == ConnectionState::Failed || state == ConnectionState::Closed {
            to_remove.push(*peer_id);
        }
    }

    to_remove
}

/// Remove failed connections and send events
async fn remove_failed_connections(
    connections: &Arc<RwLock<HashMap<PeerId, WebRtcConnection>>>,
    event_sender: &mpsc::UnboundedSender<super::super::WebRtcEvent>,
    to_remove: Vec<PeerId>,
) {
    if !to_remove.is_empty() {
        let mut connections_guard = connections.write().await;
        for peer_id in to_remove {
            connections_guard.remove(&peer_id);
            let _ = event_sender.send(super::super::WebRtcEvent::ConnectionClosed { peer_id });
        }
    }
}
