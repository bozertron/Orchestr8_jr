#[path = "message_integration_helpers.rs"]
mod message_integration_helpers;

use crate::p2p::{
    events::{EventBus, P2PEventType},
    message::{MessageEvent, MessageService},
};
use anyhow::{Context, Result};
use message_integration_helpers::{
    extract_message_id, handle_message_event_type, process_through_service,
};
use std::sync::Arc;
use tokio::sync::{mpsc, RwLock};
use tracing::{debug, info};

/// Wire message service to event bus
pub async fn wire_message_service(
    message_service: Arc<RwLock<Option<MessageService>>>,
    event_bus: Arc<EventBus>,
    mut message_event_receiver: mpsc::UnboundedReceiver<MessageEvent>,
) -> Result<()> {
    info!("Wiring message service to event bus");

    // Spawn task to forward message events to event bus
    tokio::spawn(async move {
        while let Some(event) = message_event_receiver.recv().await {
            if let Err(e) = handle_message_event(event, &event_bus, &message_service).await {
                debug!("Error handling message event: {}", e);
            }
        }
    });

    info!("Message service wired to event bus");
    Ok(())
}

/// Handle message event
async fn handle_message_event(
    event: MessageEvent,
    event_bus: &EventBus,
    message_service: &Arc<RwLock<Option<MessageService>>>,
) -> Result<()> {
    match event {
        MessageEvent::MessageReceived { from, message } => {
            handle_message_received(from, message, event_bus, message_service).await?;
        }
        MessageEvent::MessageSent { to, message_id } => {
            handle_message_sent(to, message_id, event_bus, message_service).await?;
        }
        MessageEvent::MessageDelivered { message_id } => {
            handle_message_delivered(message_id, event_bus, message_service).await?;
        }
        MessageEvent::MessageFailed { message_id, error } => {
            handle_message_failed(message_id, error, event_bus, message_service).await?;
        }
    }

    Ok(())
}

/// Handle message received event
async fn handle_message_received(
    from: libp2p::PeerId,
    message: crate::p2p::message::P2PMessage,
    event_bus: &EventBus,
    message_service: &Arc<RwLock<Option<MessageService>>>,
) -> Result<()> {
    debug!("Message received from: {}", from);

    let message_id = extract_message_id(&message);
    process_through_service(message_service, &from, &message).await;

    event_bus
        .publish(P2PEventType::MessageReceived { message_id })
        .await
        .context("Failed to publish message received event")?;

    Ok(())
}

/// Handle message sent event
async fn handle_message_sent(
    to: libp2p::PeerId,
    message_id: crate::p2p::message::MessageId,
    event_bus: &EventBus,
    _message_service: &Arc<RwLock<Option<MessageService>>>,
) -> Result<()> {
    debug!("Message sent to: {} - ID: {}", to, message_id);

    event_bus
        .publish(P2PEventType::MessageSent {
            message_id: message_id.to_string(),
        })
        .await
        .context("Failed to publish message sent event")?;

    Ok(())
}

/// Handle message delivered event
async fn handle_message_delivered(
    message_id: crate::p2p::message::MessageId,
    event_bus: &EventBus,
    _message_service: &Arc<RwLock<Option<MessageService>>>,
) -> Result<()> {
    debug!("Message delivered: {}", message_id);

    event_bus
        .publish(P2PEventType::MessageDelivered {
            message_id: message_id.to_string(),
        })
        .await
        .context("Failed to publish message delivered event")?;

    Ok(())
}

/// Handle message failed event
async fn handle_message_failed(
    message_id: crate::p2p::message::MessageId,
    error: String,
    event_bus: &EventBus,
    _message_service: &Arc<RwLock<Option<MessageService>>>,
) -> Result<()> {
    debug!("Message failed: {} - {}", message_id, error);

    event_bus
        .publish(P2PEventType::MessageFailed {
            message_id: message_id.to_string(),
            error,
        })
        .await
        .context("Failed to publish message failed event")?;

    Ok(())
}

/// Configure message event handlers
pub async fn configure_message_events(
    message_service: Arc<RwLock<Option<MessageService>>>,
    event_bus: Arc<EventBus>,
) -> Result<()> {
    debug!("Configuring message event handlers");

    let mut receiver = event_bus.subscribe().await;

    tokio::spawn(async move {
        while let Ok(event) = receiver.recv().await {
            handle_message_event_type(&event, &message_service).await;
        }
    });

    debug!("Message event handlers configured");
    Ok(())
}
