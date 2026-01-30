pub mod bus;
pub mod handlers;
pub mod subscriptions;

#[cfg(test)]
mod tests;

pub use bus::EventBus;
pub use handlers::EventHandlerRegistry;
pub use subscriptions::{Subscription, SubscriptionManager};

use crate::p2p::{DiscoveryEvent, MessageEvent, WebRtcEvent};
use libp2p::PeerId;

/// Unified P2P event type for the event bus
#[derive(Debug, Clone)]
pub enum P2PEventType {
    // Discovery events
    PeerDiscovered { peer_id: PeerId },
    PeerLost { peer_id: PeerId },

    // Transport events
    ConnectionEstablished { peer_id: PeerId },
    ConnectionLost { peer_id: PeerId },

    // WebRTC events
    DataChannelOpen { peer_id: PeerId, channel_id: String },
    DataChannelClosed { peer_id: PeerId, channel_id: String },

    // Message events
    MessageReceived { message_id: String },
    MessageSent { message_id: String },
    MessageDelivered { message_id: String },
    MessageFailed { message_id: String, error: String },

    // Relay events
    RelayConnected,
    RelayDisconnected,

    // Lifecycle events
    ServiceStarted,
    ServiceStopped,
    ServiceDegraded { reason: String },
    ComponentFailed { component: String },
}

impl From<DiscoveryEvent> for P2PEventType {
    fn from(event: DiscoveryEvent) -> Self {
        match event {
            DiscoveryEvent::PeerDiscovered { peer_id, .. } => {
                P2PEventType::PeerDiscovered { peer_id }
            }
            DiscoveryEvent::PeerExpired { peer_id } => P2PEventType::PeerLost { peer_id },
            _ => P2PEventType::ServiceStarted, // Placeholder for other events
        }
    }
}

impl From<WebRtcEvent> for P2PEventType {
    fn from(event: WebRtcEvent) -> Self {
        match event {
            WebRtcEvent::ConnectionEstablished { peer_id } => {
                P2PEventType::ConnectionEstablished { peer_id }
            }
            WebRtcEvent::ConnectionClosed { peer_id } => P2PEventType::ConnectionLost { peer_id },
            WebRtcEvent::DataChannelOpened {
                peer_id,
                channel_id,
            } => P2PEventType::DataChannelOpen {
                peer_id,
                channel_id,
            },
            WebRtcEvent::DataChannelClosed {
                peer_id,
                channel_id,
            } => P2PEventType::DataChannelClosed {
                peer_id,
                channel_id,
            },
            _ => P2PEventType::ServiceStarted, // Placeholder for other events
        }
    }
}

impl From<MessageEvent> for P2PEventType {
    fn from(event: MessageEvent) -> Self {
        match event {
            MessageEvent::MessageSent { message_id, .. } => P2PEventType::MessageSent {
                message_id: message_id.to_string(),
            },
            MessageEvent::MessageDelivered { message_id } => P2PEventType::MessageDelivered {
                message_id: message_id.to_string(),
            },
            MessageEvent::MessageFailed { message_id, error } => P2PEventType::MessageFailed {
                message_id: message_id.to_string(),
                error,
            },
            _ => P2PEventType::ServiceStarted, // Placeholder for other events
        }
    }
}
