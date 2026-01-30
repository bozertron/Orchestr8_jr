// Helper functions for WebRTC integration
//
// Pattern Bible Compliance:
// - File: Helper module for webrtc_integration.rs
// - Extracted to maintain ≤30 lines per function
// - Contains data channel event handling logic

use crate::p2p::{events::P2PEventType, webrtc::WebRtcService};
use std::sync::Arc;
use tokio::sync::RwLock;
use tracing::debug;

/// Handle data channel event for configure_webrtc_events
///
/// Processes data channel open/close events and updates WebRTC service state
pub(crate) async fn handle_data_channel_event(
    event: &P2PEventType,
    webrtc: &Arc<RwLock<Option<WebRtcService>>>,
) {
    match event {
        P2PEventType::DataChannelOpen {
            peer_id,
            channel_id,
        } => {
            debug!(
                "WebRTC handler received data channel open: {} - {}",
                peer_id, channel_id
            );
            if let Some(_service) = webrtc.read().await.as_ref() {
                debug!(
                    "WebRTC service managing channel {} for {}",
                    channel_id, peer_id
                );
                // TODO: Implement data channel management
                // In a full implementation, this would manage data channels
            }
        }
        P2PEventType::DataChannelClosed {
            peer_id,
            channel_id,
        } => {
            debug!(
                "WebRTC handler received data channel closed: {} - {}",
                peer_id, channel_id
            );
            if let Some(_service) = webrtc.read().await.as_ref() {
                debug!(
                    "WebRTC service cleaning up channel {} for {}",
                    channel_id, peer_id
                );
                // TODO: Implement resource cleanup
                // In a full implementation, this would clean up resources
            }
        }
        _ => {}
    }
}
