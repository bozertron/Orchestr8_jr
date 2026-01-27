use anyhow::{Context, Result};
use r2d2::Pool;
use r2d2_sqlite::SqliteConnectionManager;
use std::sync::Arc;
use tokio::sync::mpsc;

use super::events_core::{PersistenceEvent, PersistenceEventType};
use crate::p2p::MessageEvent;

/// Core processor implementation for event handling and conversion
#[derive(Clone)]
pub struct ProcessorCoreImpl {
    pool: Arc<Pool<SqliteConnectionManager>>,
    event_sender: mpsc::UnboundedSender<MessageEvent>,
}

impl ProcessorCoreImpl {
    /// Create new processor core
    pub fn new(
        pool: Arc<Pool<SqliteConnectionManager>>,
        event_sender: mpsc::UnboundedSender<MessageEvent>,
    ) -> Self {
        Self { pool, event_sender }
    }

    /// Emit persistence event to message event system
    pub async fn emit_persistence_event(&self, persistence_event: PersistenceEvent) -> Result<()> {
        let message_event = self.convert_persistence_to_message_event(&persistence_event);
        self.send_message_event(message_event).await
    }

    /// Expose pool stats access for health diagnostics
    pub fn pool(&self) -> &Pool<SqliteConnectionManager> {
        &self.pool
    }

    /// Convert persistence event to message event
    pub fn convert_persistence_to_message_event(&self, event: &PersistenceEvent) -> MessageEvent {
        match event.event_type {
            PersistenceEventType::MessageStored => self.handle_message_stored(event),
            PersistenceEventType::MessageRetrieved
            | PersistenceEventType::DeliveryStatusUpdated
            | PersistenceEventType::SearchPerformed => MessageEvent::MessageDelivered {
                message_id: event.message_id,
            },
            PersistenceEventType::MessageDeleted => MessageEvent::MessageFailed {
                message_id: event.message_id,
                error: "Message deleted".to_string(),
            },
        }
    }

    /// Handle message stored event conversion
    fn handle_message_stored(&self, event: &PersistenceEvent) -> MessageEvent {
        if let Some(peer_id) = event.peer_id {
            MessageEvent::MessageSent {
                to: peer_id,
                message_id: event.message_id,
            }
        } else {
            MessageEvent::MessageFailed {
                message_id: event.message_id,
                error: "No peer_id for stored message".to_string(),
            }
        }
    }

    /// Send message event to channel
    async fn send_message_event(&self, message_event: MessageEvent) -> Result<()> {
        self.event_sender
            .send(message_event)
            .context("Failed to send message event")?;
        Ok(())
    }
}
