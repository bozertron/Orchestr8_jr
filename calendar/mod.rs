// Calendar System Module
// Pattern Bible Compliance: File ≤200 lines, Functions ≤30 lines

pub mod events;
pub mod integration;
pub mod manager;
pub mod scheduling;
pub mod storage;

// Re-export core types for convenience
pub use events::{
    Attachment, AttachmentType, DeadlineSeverity, Event, EventId, EventType, RecurrencePattern,
    Reminder, TaskPriority,
};
pub use integration::{ChatIntegration, ContactIntegration, DocumentIntegration};
pub use manager::CalendarManager;
pub use scheduling::{AvailabilityChecker, ConflictDetector, MeetingSuggester};
pub use storage::{CalendarStorage, CalendarSync};

/// Calendar system version
pub const CALENDAR_VERSION: &str = "1.0.0";

/// Maximum events per calendar
pub const MAX_EVENTS_PER_CALENDAR: usize = 10_000;

/// Default reminder time (minutes before event)
pub const DEFAULT_REMINDER_MINUTES: u32 = 15;

/// Maximum reminders per event
pub const MAX_REMINDERS_PER_EVENT: usize = 10;

/// Maximum attachments per event
pub const MAX_ATTACHMENTS_PER_EVENT: usize = 50;

/// Default event duration (minutes)
pub const DEFAULT_EVENT_DURATION_MINUTES: u32 = 60;
