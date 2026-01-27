// Calendar Reminder System
// Pattern Bible Compliance: File ≤200 lines, Functions ≤30 lines

use chrono::{DateTime, Duration, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ReminderManager {
    pending_reminders: Vec<PendingReminder>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PendingReminder {
    id: Uuid,
    event_id: Uuid,
    trigger_time: DateTime<Utc>,
    message: String,
    sent: bool,
}

impl ReminderManager {
    pub fn new() -> Self {
        Self {
            pending_reminders: Vec::new(),
        }
    }

    pub fn schedule_reminder(
        &mut self,
        event_id: Uuid,
        event_start: DateTime<Utc>,
        minutes_before: u32,
        message: String,
    ) -> Uuid {
        let trigger_time = event_start - Duration::minutes(minutes_before as i64);
        let reminder = PendingReminder {
            id: Uuid::new_v4(),
            event_id,
            trigger_time,
            message,
            sent: false,
        };

        let id = reminder.id;
        self.pending_reminders.push(reminder);
        id
    }

    pub fn get_due_reminders(&mut self) -> Vec<(Uuid, String)> {
        let now = Utc::now();
        let mut due = Vec::new();

        for reminder in &mut self.pending_reminders {
            if !reminder.sent && reminder.trigger_time <= now {
                due.push((reminder.event_id, reminder.message.clone()));
                reminder.sent = true;
            }
        }

        due
    }

    pub fn snooze_reminder(&mut self, reminder_id: Uuid, minutes: u32) {
        if let Some(reminder) = self
            .pending_reminders
            .iter_mut()
            .find(|r| r.id == reminder_id)
        {
            reminder.trigger_time = Utc::now() + Duration::minutes(minutes as i64);
            reminder.sent = false;
        }
    }

    pub fn cancel_reminder(&mut self, reminder_id: Uuid) {
        self.pending_reminders.retain(|r| r.id != reminder_id);
    }

    pub fn cancel_event_reminders(&mut self, event_id: Uuid) {
        self.pending_reminders.retain(|r| r.event_id != event_id);
    }

    pub fn cleanup_sent_reminders(&mut self) {
        let cutoff = Utc::now() - Duration::hours(24);
        self.pending_reminders
            .retain(|r| !r.sent || r.trigger_time > cutoff);
    }

    pub fn get_pending_count(&self) -> usize {
        self.pending_reminders.iter().filter(|r| !r.sent).count()
    }

    pub fn get_event_reminders(&self, event_id: Uuid) -> Vec<&PendingReminder> {
        self.pending_reminders
            .iter()
            .filter(|r| r.event_id == event_id)
            .collect()
    }
}

impl Default for ReminderManager {
    fn default() -> Self {
        Self::new()
    }
}
