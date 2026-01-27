// Calendar Chat Integration
// Pattern Bible Compliance: File ≤200 lines, Functions ≤30 lines

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::calendar::{Event, EventId, EventType};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChatLink {
    pub id: Uuid,
    pub event_id: EventId,
    pub conversation_id: String,
    pub linked_at: DateTime<Utc>,
    pub linked_by: String, // User ID
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EventUpdate {
    pub id: Uuid,
    pub event_id: EventId,
    pub conversation_id: String,
    pub update_type: UpdateType,
    pub message: String,
    pub sent_at: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum UpdateType {
    Created,
    Updated,
    Cancelled,
    Reminder,
    RsvpChanged,
}

pub struct ChatIntegration {
    links: Vec<ChatLink>,
    updates: Vec<EventUpdate>,
}

impl ChatIntegration {
    pub fn new() -> Self {
        Self {
            links: Vec::new(),
            updates: Vec::new(),
        }
    }

    pub fn create_event_from_message(
        &self,
        message_content: &str,
        created_by: String,
    ) -> Result<Event, String> {
        // Parse message for event details (simplified)
        let title = self.extract_title(message_content)?;
        let start_time = Utc::now();

        Ok(Event::new(
            title,
            EventType::Meeting {
                participants: vec![created_by.clone()],
                location: None,
                meeting_url: None,
            },
            start_time,
            created_by,
        ))
    }

    pub fn link_to_conversation(
        &mut self,
        event_id: EventId,
        conversation_id: String,
        linked_by: String,
    ) -> Uuid {
        let link = ChatLink {
            id: Uuid::new_v4(),
            event_id,
            conversation_id,
            linked_at: Utc::now(),
            linked_by,
        };

        let id = link.id;
        self.links.push(link);
        id
    }

    pub fn unlink_conversation(&mut self, link_id: Uuid) -> Result<(), String> {
        let initial_len = self.links.len();
        self.links.retain(|l| l.id != link_id);

        if self.links.len() == initial_len {
            return Err("Link not found".to_string());
        }

        Ok(())
    }

    pub fn send_event_update(
        &mut self,
        event_id: EventId,
        conversation_id: String,
        update_type: UpdateType,
        message: String,
    ) -> Uuid {
        let update = EventUpdate {
            id: Uuid::new_v4(),
            event_id,
            conversation_id,
            update_type,
            message,
            sent_at: Utc::now(),
        };

        let id = update.id;
        self.updates.push(update);
        id
    }

    pub fn get_event_links(&self, event_id: EventId) -> Vec<&ChatLink> {
        self.links
            .iter()
            .filter(|l| l.event_id == event_id)
            .collect()
    }

    pub fn get_conversation_events(&self, conversation_id: &str) -> Vec<EventId> {
        self.links
            .iter()
            .filter(|l| l.conversation_id == conversation_id)
            .map(|l| l.event_id)
            .collect()
    }

    pub fn get_updates_for_conversation(&self, conversation_id: &str) -> Vec<&EventUpdate> {
        self.updates
            .iter()
            .filter(|u| u.conversation_id == conversation_id)
            .collect()
    }

    fn extract_title(&self, message: &str) -> Result<String, String> {
        // Simplified title extraction
        let title = message
            .lines()
            .next()
            .unwrap_or("Untitled Event")
            .trim()
            .to_string();

        if title.is_empty() {
            return Err("Could not extract event title".to_string());
        }

        Ok(title)
    }
}

impl Default for ChatIntegration {
    fn default() -> Self {
        Self::new()
    }
}
