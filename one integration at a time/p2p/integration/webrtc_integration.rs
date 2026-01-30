#[path = "webrtc_integration_helpers.rs"]
mod webrtc_integration_helpers;

use crate::p2p::{
    events::{EventBus, P2PEventType},
    webrtc::{WebRtcEvent, WebRtcService},
};
use anyhow::{Context, Result};
use std::sync::Arc;
use tokio::sync::{mpsc, RwLock};
use tracing::{debug, info};
use webrtc_integration_helpers::handle_data_channel_event;

/// Wire WebRTC manager to event bus
pub async fn wire_webrtc_manager(
    webrtc: Arc<RwLock<Option<WebRtcService>>>,
    event_bus: Arc<EventBus>,
    mut webrtc_event_receiver: mpsc::UnboundedReceiver<WebRtcEvent>,
) -> Result<()> {
    info!("Wiring WebRTC manager to event bus");

    // Spawn task to forward WebRTC events to event bus
    tokio::spawn(async move {
        while let Some(event) = webrtc_event_receiver.recv().await {
            if let Err(e) = handle_webrtc_event(event, &event_bus, &webrtc).await {
                debug!("Error handling WebRTC event: {}", e);
            }
        }
    });

    info!("WebRTC manager wired to event bus");
    Ok(())
}

/// Handle WebRTC event
async fn handle_webrtc_event(
    event: WebRtcEvent,
    event_bus: &EventBus,
    webrtc: &Arc<RwLock<Option<WebRtcService>>>,
) -> Result<()> {
    match event {
        WebRtcEvent::ConnectionEstablished { peer_id } => {
            handle_webrtc_connection_established(peer_id, event_bus, webrtc).await?;
        }
        WebRtcEvent::ConnectionClosed { peer_id } => {
            handle_webrtc_connection_closed(peer_id, event_bus, webrtc).await?;
        }
        WebRtcEvent::DataChannelOpened {
            peer_id,
            channel_id,
        } => {
            handle_data_channel_open(peer_id, channel_id, event_bus, webrtc).await?;
        }
        WebRtcEvent::DataChannelClosed {
            peer_id,
            channel_id,
        } => {
            handle_data_channel_closed(peer_id, channel_id, event_bus, webrtc).await?;
        }
        WebRtcEvent::ConnectionFailed { peer_id, error } => {
            handle_webrtc_connection_failed(peer_id, error, event_bus, webrtc).await?;
        }
        _ => {
            debug!("Ignoring other WebRTC event");
        }
    }

    Ok(())
}

/// Handle WebRTC connection established
async fn handle_webrtc_connection_established(
    peer_id: libp2p::PeerId,
    event_bus: &EventBus,
    webrtc: &Arc<RwLock<Option<WebRtcService>>>,
) -> Result<()> {
    debug!("WebRTC connection established: {}", peer_id);

    // Update WebRTC service with new connection
    if let Some(_service) = webrtc.read().await.as_ref() {
        debug!("WebRTC service processing new connection for {}", peer_id);
        // TODO: Implement connection state update
        // In a full implementation, this would update connection state
    }

    event_bus
        .publish(P2PEventType::ConnectionEstablished { peer_id })
        .await
        .context("Failed to publish WebRTC connection established event")?;

    Ok(())
}

/// Handle WebRTC connection closed
async fn handle_webrtc_connection_closed(
    peer_id: libp2p::PeerId,
    event_bus: &EventBus,
    _webrtc: &Arc<RwLock<Option<WebRtcService>>>,
) -> Result<()> {
    debug!("WebRTC connection closed: {}", peer_id);

    event_bus
        .publish(P2PEventType::ConnectionLost { peer_id })
        .await
        .context("Failed to publish WebRTC connection closed event")?;

    Ok(())
}

/// Handle data channel open event
async fn handle_data_channel_open(
    peer_id: libp2p::PeerId,
    channel_id: String,
    event_bus: &EventBus,
    _webrtc: &Arc<RwLock<Option<WebRtcService>>>,
) -> Result<()> {
    debug!("Data channel opened: {} - {}", peer_id, channel_id);

    event_bus
        .publish(P2PEventType::DataChannelOpen {
            peer_id,
            channel_id,
        })
        .await
        .context("Failed to publish data channel open event")?;

    Ok(())
}

/// Handle data channel closed event
async fn handle_data_channel_closed(
    peer_id: libp2p::PeerId,
    channel_id: String,
    event_bus: &EventBus,
    _webrtc: &Arc<RwLock<Option<WebRtcService>>>,
) -> Result<()> {
    debug!("Data channel closed: {} - {}", peer_id, channel_id);

    event_bus
        .publish(P2PEventType::DataChannelClosed {
            peer_id,
            channel_id,
        })
        .await
        .context("Failed to publish data channel closed event")?;

    Ok(())
}

/// Handle WebRTC connection failed
async fn handle_webrtc_connection_failed(
    peer_id: libp2p::PeerId,
    error: String,
    event_bus: &EventBus,
    _webrtc: &Arc<RwLock<Option<WebRtcService>>>,
) -> Result<()> {
    debug!("WebRTC connection failed: {} - {}", peer_id, error);

    event_bus
        .publish(P2PEventType::ComponentFailed {
            component: format!("webrtc:{}", peer_id),
        })
        .await
        .context("Failed to publish WebRTC connection failed event")?;

    Ok(())
}

/// Configure WebRTC event handlers
pub async fn configure_webrtc_events(
    webrtc: Arc<RwLock<Option<WebRtcService>>>,
    event_bus: Arc<EventBus>,
) -> Result<()> {
    debug!("Configuring WebRTC event handlers");

    let mut receiver = event_bus.subscribe().await;

    tokio::spawn(async move {
        while let Ok(event) = receiver.recv().await {
            handle_data_channel_event(&event, &webrtc).await;
        }
    });

    debug!("WebRTC event handlers configured");
    Ok(())
}
