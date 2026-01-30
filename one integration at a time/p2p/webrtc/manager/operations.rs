use super::super::config::WebRtcConfig;
use super::super::connection::WebRtcConnection;
use super::stats::ManagerStats;
use libp2p::PeerId;
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::{mpsc, RwLock};

/// Create connection to peer (as offerer)
pub async fn create_connection(
    peer_id: PeerId,
    connections: &Arc<RwLock<HashMap<PeerId, WebRtcConnection>>>,
    config: &WebRtcConfig,
    event_sender: &mpsc::UnboundedSender<super::super::WebRtcEvent>,
    stats: &Arc<RwLock<ManagerStats>>,
) -> Result<(), String> {
    check_connection_exists(peer_id, connections).await?;
    let connection = create_and_setup_connection(peer_id, config, event_sender).await?;
    store_connection_and_update_stats(peer_id, connection, connections, stats).await;
    Ok(())
}

/// Check if connection already exists
async fn check_connection_exists(
    peer_id: PeerId,
    connections: &Arc<RwLock<HashMap<PeerId, WebRtcConnection>>>,
) -> Result<(), String> {
    if connections.read().await.contains_key(&peer_id) {
        return Err(format!("Connection to peer {} already exists", peer_id));
    }
    Ok(())
}

/// Create and setup new connection
async fn create_and_setup_connection(
    peer_id: PeerId,
    config: &WebRtcConfig,
    event_sender: &mpsc::UnboundedSender<super::super::WebRtcEvent>,
) -> Result<WebRtcConnection, String> {
    let connection = WebRtcConnection::new(peer_id, config, event_sender.clone()).await?;
    connection
        .create_data_channel("default".to_string())
        .await?;
    let _offer = connection.create_offer().await?;
    Ok(connection)
}

/// Store connection and update statistics
async fn store_connection_and_update_stats(
    peer_id: PeerId,
    connection: WebRtcConnection,
    connections: &Arc<RwLock<HashMap<PeerId, WebRtcConnection>>>,
    stats: &Arc<RwLock<ManagerStats>>,
) {
    connections.write().await.insert(peer_id, connection);
    stats.write().await.total_connections += 1;
}

/// Accept connection from peer (as answerer)
pub async fn accept_connection(
    peer_id: PeerId,
    offer: String,
    connections: &Arc<RwLock<HashMap<PeerId, WebRtcConnection>>>,
    config: &WebRtcConfig,
    event_sender: &mpsc::UnboundedSender<super::super::WebRtcEvent>,
    stats: &Arc<RwLock<ManagerStats>>,
) -> Result<String, String> {
    // Check if connection already exists
    if connections.read().await.contains_key(&peer_id) {
        return Err(format!("Connection to peer {} already exists", peer_id));
    }

    // Create new connection
    let connection = WebRtcConnection::new(peer_id, config, event_sender.clone()).await?;

    // Create answer
    let answer = connection.create_answer(offer).await?;

    // Store connection
    connections.write().await.insert(peer_id, connection);

    // Update statistics
    stats.write().await.total_connections += 1;

    Ok(answer)
}

/// Set answer for existing connection
pub async fn set_answer(
    peer_id: PeerId,
    answer: String,
    connections: &Arc<RwLock<HashMap<PeerId, WebRtcConnection>>>,
) -> Result<(), String> {
    let connections_guard = connections.read().await;
    if let Some(connection) = connections_guard.get(&peer_id) {
        connection.set_answer(answer).await
    } else {
        Err(format!("No connection found for peer {}", peer_id))
    }
}

/// Send data through data channel
pub async fn send_data(
    peer_id: PeerId,
    channel_id: String,
    data: Vec<u8>,
    connections: &Arc<RwLock<HashMap<PeerId, WebRtcConnection>>>,
) -> Result<(), String> {
    let connections_guard = connections.read().await;
    if let Some(connection) = connections_guard.get(&peer_id) {
        connection.send_data(channel_id, data).await
    } else {
        Err(format!("No connection found for peer {}", peer_id))
    }
}

/// Create data channel for existing connection
pub async fn create_data_channel(
    peer_id: PeerId,
    channel_id: String,
    connections: &Arc<RwLock<HashMap<PeerId, WebRtcConnection>>>,
) -> Result<(), String> {
    let connections_guard = connections.read().await;
    if let Some(connection) = connections_guard.get(&peer_id) {
        connection.create_data_channel(channel_id).await
    } else {
        Err(format!("No connection found for peer {}", peer_id))
    }
}

/// Remove connection
pub async fn remove_connection(
    peer_id: PeerId,
    connections: &Arc<RwLock<HashMap<PeerId, WebRtcConnection>>>,
) -> Result<(), String> {
    let mut connections_guard = connections.write().await;
    if let Some(connection) = connections_guard.remove(&peer_id) {
        connection.close().await?;
    }
    Ok(())
}
