use super::DataChannelState;
use libp2p::PeerId;
use std::sync::Arc;
use tokio::sync::{mpsc, RwLock};
use webrtc::data_channel::data_channel_message::DataChannelMessage;
use webrtc::data_channel::RTCDataChannel;

/// Setup data channel event handlers
pub async fn setup_data_channel_handlers(
    channel: &Arc<RTCDataChannel>,
    label: String,
    peer_id: PeerId,
    state: Arc<RwLock<DataChannelState>>,
    event_sender: mpsc::UnboundedSender<super::super::WebRtcEvent>,
    bytes_received: Arc<RwLock<u64>>,
) -> Result<(), String> {
    setup_open_handler(
        channel,
        label.clone(),
        peer_id,
        state.clone(),
        event_sender.clone(),
    )
    .await;
    setup_close_handler(
        channel,
        label.clone(),
        peer_id,
        state.clone(),
        event_sender.clone(),
    )
    .await;
    setup_message_handler(channel, label, peer_id, event_sender, bytes_received).await;
    Ok(())
}

/// Setup open handler
async fn setup_open_handler(
    channel: &Arc<RTCDataChannel>,
    label: String,
    peer_id: PeerId,
    state: Arc<RwLock<DataChannelState>>,
    event_sender: mpsc::UnboundedSender<super::super::WebRtcEvent>,
) {
    channel.on_open(Box::new(move || {
        let label = label.clone();
        let state = state.clone();
        let event_sender = event_sender.clone();

        Box::pin(async move {
            *state.write().await = DataChannelState::Open;
            let _ = event_sender.send(super::super::WebRtcEvent::DataChannelOpened {
                peer_id,
                channel_id: label,
            });
        })
    }));
}

/// Setup close handler
async fn setup_close_handler(
    channel: &Arc<RTCDataChannel>,
    label: String,
    peer_id: PeerId,
    state: Arc<RwLock<DataChannelState>>,
    event_sender: mpsc::UnboundedSender<super::super::WebRtcEvent>,
) {
    channel.on_close(Box::new(move || {
        let label = label.clone();
        let state = state.clone();
        let event_sender = event_sender.clone();

        Box::pin(async move {
            *state.write().await = DataChannelState::Closed;
            let _ = event_sender.send(super::super::WebRtcEvent::DataChannelClosed {
                peer_id,
                channel_id: label,
            });
        })
    }));
}

/// Setup message handler
async fn setup_message_handler(
    channel: &Arc<RTCDataChannel>,
    label: String,
    peer_id: PeerId,
    event_sender: mpsc::UnboundedSender<super::super::WebRtcEvent>,
    bytes_received: Arc<RwLock<u64>>,
) {
    channel.on_message(Box::new(move |msg: DataChannelMessage| {
        let label = label.clone();
        let event_sender = event_sender.clone();
        let bytes_received = bytes_received.clone();

        Box::pin(async move {
            let data = msg.data.to_vec();
            *bytes_received.write().await += data.len() as u64;

            let _ = event_sender.send(super::super::WebRtcEvent::MessageReceived {
                peer_id,
                channel_id: label,
                data,
            });
        })
    }));
}
