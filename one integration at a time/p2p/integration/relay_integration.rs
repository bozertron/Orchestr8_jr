#[path = "relay_integration_helpers.rs"]
mod relay_integration_helpers;

use crate::p2p::{
    config::NetworkConfig,
    events::{EventBus, P2PEventType},
};
use anyhow::{Context, Result};
use relay_integration_helpers::{handle_relay_connection, handle_relay_event_type};
use std::sync::Arc;
use tokio::sync::RwLock;
use tracing::{debug, info};

/// Relay connection state
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RelayState {
    Disconnected,
    Connecting,
    Connected,
    Failed,
}

/// Relay connection manager
pub struct RelayConnection {
    config: NetworkConfig,
    state: Arc<RwLock<RelayState>>,
}

impl RelayConnection {
    /// Create new relay connection
    pub fn new(config: NetworkConfig) -> Self {
        Self {
            config,
            state: Arc::new(RwLock::new(RelayState::Disconnected)),
        }
    }

    /// Connect to relay server
    pub async fn connect(&self) -> Result<()> {
        if let Some(relay_url) = &self.config.relay_url {
            info!("Connecting to relay: {}", relay_url);

            *self.state.write().await = RelayState::Connecting;

            // TODO: Implement actual relay connection
            // For now, just simulate connection

            *self.state.write().await = RelayState::Connected;

            info!("Connected to relay: {}", relay_url);
        } else {
            debug!("No relay URL configured");
        }

        Ok(())
    }

    /// Disconnect from relay server
    pub async fn disconnect(&self) -> Result<()> {
        info!("Disconnecting from relay");

        *self.state.write().await = RelayState::Disconnected;

        info!("Disconnected from relay");
        Ok(())
    }

    /// Get relay state
    pub async fn state(&self) -> RelayState {
        self.state.read().await.clone()
    }
}

/// Wire relay fallback to event bus
pub async fn wire_relay_fallback(
    config: NetworkConfig,
    event_bus: Arc<EventBus>,
) -> Result<Arc<RelayConnection>> {
    info!("Wiring relay fallback to event bus");

    let relay = Arc::new(RelayConnection::new(config.clone()));

    if config.use_relay_fallback {
        let relay_clone = Arc::clone(&relay);
        let event_bus_clone = event_bus.clone();

        tokio::spawn(async move {
            handle_relay_connection(relay_clone, event_bus_clone).await;
        });
    }

    info!("Relay fallback wired to event bus");
    Ok(relay)
}

/// Handle relay connected event
pub async fn handle_relay_connected(event_bus: &EventBus) -> Result<()> {
    debug!("Relay connected");

    event_bus
        .publish(P2PEventType::RelayConnected)
        .await
        .context("Failed to publish relay connected event")?;

    Ok(())
}

/// Handle relay disconnected event
pub async fn handle_relay_disconnected(event_bus: &EventBus) -> Result<()> {
    debug!("Relay disconnected");

    event_bus
        .publish(P2PEventType::RelayDisconnected)
        .await
        .context("Failed to publish relay disconnected event")?;

    Ok(())
}

/// Configure relay event handlers
pub async fn configure_relay_events(
    relay: Arc<RelayConnection>,
    event_bus: Arc<EventBus>,
) -> Result<()> {
    debug!("Configuring relay event handlers");

    let mut receiver = event_bus.subscribe().await;

    tokio::spawn(async move {
        while let Ok(event) = receiver.recv().await {
            handle_relay_event_type(&event, &relay).await;
        }
    });

    debug!("Relay event handlers configured");
    Ok(())
}
