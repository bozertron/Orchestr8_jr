// Calendar Event Notifications
// Pattern Bible Compliance: File ≤200 lines, Functions ≤30 lines

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum NotificationType {
    Reminder,
    EventStarting,
    EventChanged,
    EventCancelled,
    InvitationReceived,
    InvitationAccepted,
    InvitationDeclined,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Notification {
    pub id: Uuid,
    pub notification_type: NotificationType,
    pub event_id: Uuid,
    pub title: String,
    pub message: String,
    pub timestamp: DateTime<Utc>,
    pub read: bool,
}

pub struct NotificationManager {
    notifications: Vec<Notification>,
}

impl NotificationManager {
    pub fn new() -> Self {
        Self {
            notifications: Vec::new(),
        }
    }

    pub fn send_notification(
        &mut self,
        notification_type: NotificationType,
        event_id: Uuid,
        title: String,
        message: String,
    ) -> Uuid {
        let notification = Notification {
            id: Uuid::new_v4(),
            notification_type,
            event_id,
            title,
            message,
            timestamp: Utc::now(),
            read: false,
        };

        let id = notification.id;
        self.notifications.push(notification);
        id
    }

    pub fn mark_as_read(&mut self, notification_id: Uuid) {
        if let Some(notification) = self
            .notifications
            .iter_mut()
            .find(|n| n.id == notification_id)
        {
            notification.read = true;
        }
    }

    pub fn mark_all_as_read(&mut self) {
        for notification in &mut self.notifications {
            notification.read = true;
        }
    }

    /// Get notification settings as JSON
    pub fn get_settings(&self) -> serde_json::Value {
        serde_json::json!({
            "enabled": true,
            "default_reminder_minutes": 15,
            "notification_count": self.notifications.len(),
            "unread_count": self.notifications.iter().filter(|n| !n.read).count()
        })
    }

    pub fn get_unread(&self) -> Vec<&Notification> {
        self.notifications.iter().filter(|n| !n.read).collect()
    }

    pub fn get_all(&self) -> &[Notification] {
        &self.notifications
    }

    pub fn get_by_event(&self, event_id: Uuid) -> Vec<&Notification> {
        self.notifications
            .iter()
            .filter(|n| n.event_id == event_id)
            .collect()
    }

    pub fn clear_old_notifications(&mut self, days: i64) {
        let cutoff = Utc::now() - chrono::Duration::days(days);
        self.notifications.retain(|n| n.timestamp > cutoff);
    }

    pub fn delete_notification(&mut self, notification_id: Uuid) {
        self.notifications.retain(|n| n.id != notification_id);
    }

    pub fn get_unread_count(&self) -> usize {
        self.notifications.iter().filter(|n| !n.read).count()
    }
}

impl Default for NotificationManager {
    fn default() -> Self {
        Self::new()
    }
}
