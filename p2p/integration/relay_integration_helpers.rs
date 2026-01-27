// Helper functions for relay integration
//
// Pattern Bible Compliance:
// - File: Helper module for relay_integration.rs
// - Extracted to maintain ≤30 lines per function
// - Contains relay connection and event handling logic

use crate::p2p::events::{EventBus, P2PEventType};
use std::sync::Arc;
use tracing::debug;

use super::RelayConnection;

/// Handle relay connection for wire_relay_fallback
///
/// Connects to relay and publishes appropriate events
pub(crate) async fn handle_relay_connection(relay: Arc<RelayConnection>, event_bus: Arc<EventBus>) {
    if let Err(e) = relay.connect().await {
        debug!("Failed to connect to relay: {}", e);
        let _ = event_bus
            .publish(P2PEventType::ComponentFailed {
                component: "relay".to_string(),
            })
            .await;
    } else {
        let _ = event_bus.publish(P2PEventType::RelayConnected).await;
    }
}

/// Handle relay event type for configure_relay_events
///
/// Processes relay-specific events and manages reconnection logic
pub(crate) async fn handle_relay_event_type(event: &P2PEventType, relay: &Arc<RelayConnection>) {
    match event {
        P2PEventType::RelayConnected => {
            debug!("Relay handler received relay connected");
            // Additional relay-specific handling can go here
        }
        P2PEventType::RelayDisconnected => {
            debug!("Relay handler received relay disconnected");
            // Attempt to reconnect
            if let Err(e) = relay.connect().await {
                debug!("Failed to reconnect to relay: {}", e);
            }
        }
        P2PEventType::ComponentFailed { component } if component == "relay" => {
            debug!("Relay handler received relay failed");
            // Attempt to reconnect after delay
            tokio::time::sleep(tokio::time::Duration::from_secs(5)).await;
            if let Err(e) = relay.connect().await {
                debug!("Failed to reconnect to relay: {}", e);
            }
        }
        _ => {}
    }
}
