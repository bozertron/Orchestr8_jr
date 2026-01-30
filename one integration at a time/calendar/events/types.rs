// Calendar Event Types
// Pattern Bible Compliance: File ≤200 lines, Functions ≤30 lines

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use super::recurrence::RecurrencePattern;

pub type EventId = Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum EventType {
    Meeting {
        participants: Vec<String>, // Contact IDs
        location: Option<String>,
        meeting_url: Option<String>,
    },
    Task {
        completed: bool,
        priority: TaskPriority,
        assignee: Option<String>, // Contact ID
    },
    Reminder {
        notification_sent: bool,
    },
    Deadline {
        project: Option<String>,
        severity: DeadlineSeverity,
    },
    Milestone {
        project: Option<String>,
        progress: u8, // 0-100%
    },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum TaskPriority {
    Low,
    Medium,
    High,
    Urgent,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum DeadlineSeverity {
    Normal,
    Important,
    Critical,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Event {
    pub id: EventId,
    pub title: String,
    pub description: Option<String>,
    pub event_type: EventType,
    pub start_time: DateTime<Utc>,
    pub end_time: Option<DateTime<Utc>>,
    pub all_day: bool,
    pub recurrence: Option<RecurrencePattern>,
    pub reminders: Vec<Reminder>,
    pub tags: Vec<String>,
    pub color: Option<String>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
    pub created_by: String, // User ID
    pub attachments: Vec<Attachment>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Reminder {
    pub id: Uuid,
    pub minutes_before: u32,
    pub notification_sent: bool,
    pub snoozed_until: Option<DateTime<Utc>>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Attachment {
    pub id: Uuid,
    pub attachment_type: AttachmentType,
    pub reference_id: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum AttachmentType {
    Document,
    Contact,
    ChatConversation,
    ExternalLink,
}

impl Event {
    pub fn new(
        title: String,
        event_type: EventType,
        start_time: DateTime<Utc>,
        created_by: String,
    ) -> Self {
        let now = Utc::now();
        Self {
            id: Uuid::new_v4(),
            title,
            description: None,
            event_type,
            start_time,
            end_time: None,
            all_day: false,
            recurrence: None,
            reminders: vec![],
            tags: vec![],
            color: None,
            created_at: now,
            updated_at: now,
            created_by,
            attachments: vec![],
        }
    }

    pub fn is_recurring(&self) -> bool {
        self.recurrence.is_some()
    }

    pub fn is_all_day(&self) -> bool {
        self.all_day
    }

    pub fn duration_minutes(&self) -> Option<i64> {
        self.end_time
            .map(|end| (end - self.start_time).num_minutes())
    }

    pub fn add_reminder(&mut self, minutes_before: u32) {
        self.reminders.push(Reminder {
            id: Uuid::new_v4(),
            minutes_before,
            notification_sent: false,
            snoozed_until: None,
        });
        self.updated_at = Utc::now();
    }

    pub fn attach_document(&mut self, document_id: String) {
        self.attachments.push(Attachment {
            id: Uuid::new_v4(),
            attachment_type: AttachmentType::Document,
            reference_id: document_id,
        });
        self.updated_at = Utc::now();
    }

    pub fn attach_contact(&mut self, contact_id: String) {
        self.attachments.push(Attachment {
            id: Uuid::new_v4(),
            attachment_type: AttachmentType::Contact,
            reference_id: contact_id,
        });
        self.updated_at = Utc::now();
    }

    pub fn attach_chat(&mut self, conversation_id: String) {
        self.attachments.push(Attachment {
            id: Uuid::new_v4(),
            attachment_type: AttachmentType::ChatConversation,
            reference_id: conversation_id,
        });
        self.updated_at = Utc::now();
    }
}
