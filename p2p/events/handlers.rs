use super::P2PEventType;
use anyhow::Result;
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;
use tracing::{debug, info};

/// Event handler function type
pub type EventHandler = Arc<dyn Fn(P2PEventType) -> Result<()> + Send + Sync>;

/// Event handler registry for managing event handlers
pub struct EventHandlerRegistry {
    handlers: Arc<RwLock<HashMap<String, Vec<EventHandler>>>>,
}

impl EventHandlerRegistry {
    /// Create new event handler registry
    pub fn new() -> Self {
        Self {
            handlers: Arc::new(RwLock::new(HashMap::new())),
        }
    }

    /// Register event handler for specific event type
    pub async fn register_handler(&self, event_type: &str, handler: EventHandler) -> Result<()> {
        info!("Registering handler for event type: {}", event_type);

        let mut handlers = self.handlers.write().await;
        handlers
            .entry(event_type.to_string())
            .or_insert_with(Vec::new)
            .push(handler);

        debug!("Handler registered for: {}", event_type);
        Ok(())
    }

    /// Dispatch event to registered handlers
    pub async fn dispatch_event(&self, event: P2PEventType) -> Result<()> {
        let event_type = self.get_event_type_name(&event);
        debug!("Dispatching event: {}", event_type);

        let handlers = self.handlers.read().await;

        if let Some(handler_list) = handlers.get(&event_type) {
            for handler in handler_list {
                if let Err(e) = handler(event.clone()) {
                    debug!("Handler error for {}: {}", event_type, e);
                }
            }
        }

        Ok(())
    }

    /// Handle peer-related events
    pub async fn handle_peer_event(&self, event: P2PEventType) -> Result<()> {
        match &event {
            P2PEventType::PeerDiscovered { peer_id } => {
                info!("Handling peer discovered: {}", peer_id);
                self.dispatch_event(event).await?;
            }
            P2PEventType::PeerLost { peer_id } => {
                info!("Handling peer lost: {}", peer_id);
                self.dispatch_event(event).await?;
            }
            P2PEventType::ConnectionEstablished { peer_id } => {
                info!("Handling connection established: {}", peer_id);
                self.dispatch_event(event).await?;
            }
            P2PEventType::ConnectionLost { peer_id } => {
                info!("Handling connection lost: {}", peer_id);
                self.dispatch_event(event).await?;
            }
            _ => {
                debug!("Not a peer event, skipping");
            }
        }

        Ok(())
    }

    /// Handle message-related events
    pub async fn handle_message_event(&self, event: P2PEventType) -> Result<()> {
        match &event {
            P2PEventType::MessageReceived { message_id } => {
                info!("Handling message received: {}", message_id);
                self.dispatch_event(event).await?;
            }
            P2PEventType::MessageSent { message_id } => {
                info!("Handling message sent: {}", message_id);
                self.dispatch_event(event).await?;
            }
            P2PEventType::MessageDelivered { message_id } => {
                info!("Handling message delivered: {}", message_id);
                self.dispatch_event(event).await?;
            }
            P2PEventType::MessageFailed { message_id, error } => {
                info!("Handling message failed: {} - {}", message_id, error);
                self.dispatch_event(event).await?;
            }
            _ => {
                debug!("Not a message event, skipping");
            }
        }

        Ok(())
    }

    /// Get event type name for routing
    fn get_event_type_name(&self, event: &P2PEventType) -> String {
        match event {
            P2PEventType::PeerDiscovered { .. } => "peer_discovered".to_string(),
            P2PEventType::PeerLost { .. } => "peer_lost".to_string(),
            P2PEventType::ConnectionEstablished { .. } => "connection_established".to_string(),
            P2PEventType::ConnectionLost { .. } => "connection_lost".to_string(),
            P2PEventType::DataChannelOpen { .. } => "data_channel_open".to_string(),
            P2PEventType::DataChannelClosed { .. } => "data_channel_closed".to_string(),
            P2PEventType::MessageReceived { .. } => "message_received".to_string(),
            P2PEventType::MessageSent { .. } => "message_sent".to_string(),
            P2PEventType::MessageDelivered { .. } => "message_delivered".to_string(),
            P2PEventType::MessageFailed { .. } => "message_failed".to_string(),
            P2PEventType::RelayConnected => "relay_connected".to_string(),
            P2PEventType::RelayDisconnected => "relay_disconnected".to_string(),
            P2PEventType::ServiceStarted => "service_started".to_string(),
            P2PEventType::ServiceStopped => "service_stopped".to_string(),
            P2PEventType::ServiceDegraded { .. } => "service_degraded".to_string(),
            P2PEventType::ComponentFailed { .. } => "component_failed".to_string(),
        }
    }

    /// Get handler count for event type
    pub async fn handler_count(&self, event_type: &str) -> usize {
        let handlers = self.handlers.read().await;
        handlers.get(event_type).map(|h| h.len()).unwrap_or(0)
    }

    /// Clear all handlers
    pub async fn clear_handlers(&self) -> Result<()> {
        info!("Clearing all event handlers");
        self.handlers.write().await.clear();
        Ok(())
    }
}

impl Default for EventHandlerRegistry {
    fn default() -> Self {
        Self::new()
    }
}
