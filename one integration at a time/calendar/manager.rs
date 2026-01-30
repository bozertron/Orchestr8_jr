// Calendar Manager - Central Coordinator
// Pattern Bible Compliance: File ≤200 lines, Functions ≤30 lines

use chrono::{DateTime, Utc};
use std::sync::Arc;
use tokio::sync::RwLock;

use crate::calendar::{
    events::{NotificationManager, ReminderManager},
    integration::{ChatIntegration, ContactIntegration, DocumentIntegration},
    scheduling::{
        AvailabilityChecker, Conflict, ConflictDetector, MeetingSuggester, MeetingSuggestion,
        TimeSlot, WorkingHours,
    },
    storage::{CalendarStorage, CalendarSync},
    Event, EventId,
};

pub struct CalendarManager {
    storage: Arc<RwLock<CalendarStorage>>,
    sync: Arc<RwLock<CalendarSync>>,
    reminder_manager: Arc<RwLock<ReminderManager>>,
    notification_manager: Arc<RwLock<NotificationManager>>,
    availability_checker: Arc<RwLock<AvailabilityChecker>>,
    conflict_detector: Arc<RwLock<ConflictDetector>>,
    meeting_suggester: Arc<RwLock<MeetingSuggester>>,
    contact_integration: Arc<RwLock<ContactIntegration>>,
    document_integration: Arc<RwLock<DocumentIntegration>>,
    chat_integration: Arc<RwLock<ChatIntegration>>,
}

impl CalendarManager {
    pub fn new(db_path: &str, working_hours: WorkingHours) -> Result<Self, String> {
        let storage = CalendarStorage::new(db_path)
            .map_err(|e| format!("Failed to initialize storage: {}", e))?;

        Ok(Self {
            storage: Arc::new(RwLock::new(storage)),
            sync: Arc::new(RwLock::new(CalendarSync::new())),
            reminder_manager: Arc::new(RwLock::new(ReminderManager::new())),
            notification_manager: Arc::new(RwLock::new(NotificationManager::new())),
            availability_checker: Arc::new(RwLock::new(AvailabilityChecker::new(
                working_hours.clone(),
            ))),
            conflict_detector: Arc::new(RwLock::new(ConflictDetector::new())),
            meeting_suggester: Arc::new(RwLock::new(MeetingSuggester::new(working_hours))),
            contact_integration: Arc::new(RwLock::new(ContactIntegration::new())),
            document_integration: Arc::new(RwLock::new(DocumentIntegration::new())),
            chat_integration: Arc::new(RwLock::new(ChatIntegration::new())),
        })
    }

    // Event Operations
    pub async fn create_event(&self, event: Event) -> Result<EventId, String> {
        let storage = self.storage.read().await;
        storage
            .create_event(&event)
            .map_err(|e| format!("Failed to create event: {}", e))?;
        Ok(event.id)
    }

    pub async fn get_event(&self, event_id: EventId) -> Result<Option<Event>, String> {
        let storage = self.storage.read().await;
        storage
            .get_event(event_id)
            .map_err(|e| format!("Failed to get event: {}", e))
    }

    pub async fn get_events_in_range(
        &self,
        start: DateTime<Utc>,
        end: DateTime<Utc>,
    ) -> Result<Vec<Event>, String> {
        let storage = self.storage.read().await;
        storage
            .get_events_in_range(start, end)
            .map_err(|e| format!("Failed to get events: {}", e))
    }

    pub async fn search_events(&self, query: &str) -> Result<Vec<Event>, String> {
        let storage = self.storage.read().await;
        storage
            .search_events(query)
            .map_err(|e| format!("Failed to search events: {}", e))
    }

    pub async fn update_event(&self, event: Event) -> Result<(), String> {
        let storage = self.storage.read().await;
        storage
            .update_event(&event)
            .map_err(|e| format!("Failed to update event: {}", e))
    }

    pub async fn delete_event(&self, event_id: EventId) -> Result<(), String> {
        let storage = self.storage.read().await;
        storage
            .delete_event(event_id)
            .map_err(|e| format!("Failed to delete event: {}", e))
    }

    // Reminder Operations
    pub async fn schedule_reminder(
        &self,
        event_id: EventId,
        event_start: DateTime<Utc>,
        minutes_before: u32,
        message: String,
    ) -> Result<uuid::Uuid, String> {
        let mut manager = self.reminder_manager.write().await;
        Ok(manager.schedule_reminder(event_id, event_start, minutes_before, message))
    }

    pub async fn get_due_reminders(&self) -> Result<Vec<(EventId, String)>, String> {
        let mut manager = self.reminder_manager.write().await;
        Ok(manager.get_due_reminders())
    }

    pub async fn snooze_reminder(
        &self,
        reminder_id: uuid::Uuid,
        minutes: u32,
    ) -> Result<(), String> {
        let mut manager = self.reminder_manager.write().await;
        manager.snooze_reminder(reminder_id, minutes);
        Ok(())
    }

    // Scheduling Operations
    pub async fn check_availability(
        &self,
        start: DateTime<Utc>,
        end: DateTime<Utc>,
        events: Vec<Event>,
    ) -> Result<bool, String> {
        let checker = self.availability_checker.read().await;
        let slot = TimeSlot::new(start, end);
        Ok(checker.is_available(&slot, &events))
    }

    pub async fn detect_conflicts(&self, events: Vec<Event>) -> Result<Vec<Conflict>, String> {
        let detector = self.conflict_detector.read().await;
        Ok(detector.detect_conflicts(&events))
    }

    pub async fn suggest_meeting_times(
        &self,
        from: DateTime<Utc>,
        to: DateTime<Utc>,
        duration_minutes: i64,
        participant_calendars: Vec<Vec<Event>>,
    ) -> Result<Vec<MeetingSuggestion>, String> {
        let suggester = self.meeting_suggester.read().await;
        Ok(suggester.suggest_meeting_times(from, to, duration_minutes, &participant_calendars))
    }

    // Integration Operations
    pub fn contact_integration(&self) -> Arc<RwLock<ContactIntegration>> {
        Arc::clone(&self.contact_integration)
    }

    pub fn document_integration(&self) -> Arc<RwLock<DocumentIntegration>> {
        Arc::clone(&self.document_integration)
    }

    pub fn chat_integration(&self) -> Arc<RwLock<ChatIntegration>> {
        Arc::clone(&self.chat_integration)
    }

    pub fn sync(&self) -> Arc<RwLock<CalendarSync>> {
        Arc::clone(&self.sync)
    }

    // Notification Operations
    pub async fn send_notification(
        &self,
        event_id: EventId,
        message: String,
        notification_type: String,
    ) -> Result<(), String> {
        let mut manager = self.notification_manager.write().await;
        // Parse notification_type string to NotificationType enum
        let notif_type = match notification_type.as_str() {
            "reminder" => crate::calendar::events::notifications::NotificationType::Reminder,
            "event_starting" => {
                crate::calendar::events::notifications::NotificationType::EventStarting
            }
            "event_changed" => {
                crate::calendar::events::notifications::NotificationType::EventChanged
            }
            "event_cancelled" => {
                crate::calendar::events::notifications::NotificationType::EventCancelled
            }
            "invitation_received" => {
                crate::calendar::events::notifications::NotificationType::InvitationReceived
            }
            "invitation_accepted" => {
                crate::calendar::events::notifications::NotificationType::InvitationAccepted
            }
            "invitation_declined" => {
                crate::calendar::events::notifications::NotificationType::InvitationDeclined
            }
            _ => crate::calendar::events::notifications::NotificationType::Reminder,
        };
        let title = format!("Event {}", event_id);
        manager.send_notification(notif_type, event_id, title, message);
        Ok(())
    }

    pub async fn get_notification_settings(&self) -> Result<serde_json::Value, String> {
        let manager = self.notification_manager.read().await;
        Ok(manager.get_settings())
    }
}
