use super::state::ConnectionState;
use libp2p::PeerId;
use std::sync::Arc;
use tokio::sync::{mpsc, RwLock};
use webrtc::peer_connection::RTCPeerConnection;

/// Setup connection event handlers
pub async fn setup_connection_handlers(
    peer_connection: &Arc<RTCPeerConnection>,
    peer_id: PeerId,
    state: Arc<RwLock<ConnectionState>>,
    event_sender: mpsc::UnboundedSender<super::super::WebRtcEvent>,
) -> Result<(), String> {
    setup_state_change_handler(peer_connection, peer_id, state, event_sender).await;
    Ok(())
}

/// Setup connection state change handler
async fn setup_state_change_handler(
    peer_connection: &Arc<RTCPeerConnection>,
    peer_id: PeerId,
    state: Arc<RwLock<ConnectionState>>,
    event_sender: mpsc::UnboundedSender<super::super::WebRtcEvent>,
) {
    peer_connection.on_peer_connection_state_change(Box::new(move |s| {
        let peer_id = peer_id;
        let state = state.clone();
        let event_sender = event_sender.clone();

        Box::pin(async move {
            let new_state = ConnectionState::from(s);
            *state.write().await = new_state.clone();
            send_state_event(peer_id, new_state, event_sender).await;
        })
    }));
}

/// Send state change event
async fn send_state_event(
    peer_id: PeerId,
    state: ConnectionState,
    event_sender: mpsc::UnboundedSender<super::super::WebRtcEvent>,
) {
    match state {
        ConnectionState::Connected => {
            let _ = event_sender.send(super::super::WebRtcEvent::ConnectionEstablished { peer_id });
        }
        ConnectionState::Failed => {
            let _ = event_sender.send(super::super::WebRtcEvent::ConnectionFailed {
                peer_id,
                error: "Connection failed".to_string(),
            });
        }
        ConnectionState::Closed => {
            let _ = event_sender.send(super::super::WebRtcEvent::ConnectionClosed { peer_id });
        }
        _ => {}
    }
}
