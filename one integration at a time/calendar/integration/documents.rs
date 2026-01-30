// Calendar Document Integration
// Pattern Bible Compliance: File ≤200 lines, Functions ≤30 lines

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::calendar::EventId;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum AccessLevel {
    View,
    Edit,
    Owner,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DocumentAttachment {
    pub id: Uuid,
    pub event_id: EventId,
    pub document_id: String,
    pub document_name: String,
    pub attached_at: DateTime<Utc>,
    pub attached_by: String, // User ID
    pub access_level: AccessLevel,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DocumentAccess {
    pub document_id: String,
    pub user_id: String,
    pub access_level: AccessLevel,
    pub granted_at: DateTime<Utc>,
}

pub struct DocumentIntegration {
    attachments: Vec<DocumentAttachment>,
    access_controls: Vec<DocumentAccess>,
}

impl DocumentIntegration {
    pub fn new() -> Self {
        Self {
            attachments: Vec::new(),
            access_controls: Vec::new(),
        }
    }

    pub fn attach_document(
        &mut self,
        event_id: EventId,
        document_id: String,
        document_name: String,
        attached_by: String,
        access_level: AccessLevel,
    ) -> Uuid {
        let attachment = DocumentAttachment {
            id: Uuid::new_v4(),
            event_id,
            document_id,
            document_name,
            attached_at: Utc::now(),
            attached_by,
            access_level,
        };

        let id = attachment.id;
        self.attachments.push(attachment);
        id
    }

    pub fn remove_attachment(&mut self, attachment_id: Uuid) -> Result<(), String> {
        let initial_len = self.attachments.len();
        self.attachments.retain(|a| a.id != attachment_id);

        if self.attachments.len() == initial_len {
            return Err("Attachment not found".to_string());
        }

        Ok(())
    }

    pub fn get_event_documents(&self, event_id: EventId) -> Vec<&DocumentAttachment> {
        self.attachments
            .iter()
            .filter(|a| a.event_id == event_id)
            .collect()
    }

    pub fn get_attachment(&self, attachment_id: Uuid) -> Option<&DocumentAttachment> {
        self.attachments.iter().find(|a| a.id == attachment_id)
    }

    pub fn grant_access(
        &mut self,
        document_id: String,
        user_id: String,
        access_level: AccessLevel,
    ) {
        // Remove existing access if present
        self.access_controls
            .retain(|a| !(a.document_id == document_id && a.user_id == user_id));

        // Add new access
        self.access_controls.push(DocumentAccess {
            document_id,
            user_id,
            access_level,
            granted_at: Utc::now(),
        });
    }

    pub fn revoke_access(&mut self, document_id: &str, user_id: &str) {
        self.access_controls
            .retain(|a| !(a.document_id == document_id && a.user_id == user_id));
    }

    pub fn check_access(&self, document_id: &str, user_id: &str) -> Option<AccessLevel> {
        self.access_controls
            .iter()
            .find(|a| a.document_id == document_id && a.user_id == user_id)
            .map(|a| a.access_level)
    }

    pub fn get_document_access(&self, document_id: &str) -> Vec<&DocumentAccess> {
        self.access_controls
            .iter()
            .filter(|a| a.document_id == document_id)
            .collect()
    }
}

impl Default for DocumentIntegration {
    fn default() -> Self {
        Self::new()
    }
}
