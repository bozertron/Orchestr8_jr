// Calendar Events Module
// Pattern Bible Compliance: File ≤200 lines, Functions ≤30 lines

pub mod notifications;
pub mod recurrence;
pub mod reminders;
pub mod types;

// Re-export core types
pub use notifications::{Notification, NotificationManager, NotificationType};
pub use recurrence::{RecurrencePattern, RecurrenceRule};
pub use reminders::ReminderManager;
pub use types::{
    Attachment, AttachmentType, DeadlineSeverity, Event, EventId, EventType, Reminder, TaskPriority,
};
