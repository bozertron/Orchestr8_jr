// Calendar Database Storage
// Pattern Bible Compliance: File ≤200 lines, Functions ≤30 lines

use chrono::{DateTime, Utc};
use rusqlite::{params, Connection, Result as SqliteResult};
use serde_json;
use std::sync::{Arc, Mutex};

use crate::calendar::{Event, EventId};

#[path = "database_queries.rs"]
mod database_queries;

#[path = "database_helpers.rs"]
mod database_helpers;

use database_helpers::get_calendar_schema_sql;

pub struct CalendarStorage {
    conn: Arc<Mutex<Connection>>,
}

impl CalendarStorage {
    pub fn new(db_path: &str) -> SqliteResult<Self> {
        let conn = Connection::open(db_path)?;
        let storage = Self {
            conn: Arc::new(Mutex::new(conn)),
        };
        storage.initialize_schema()?;
        Ok(storage)
    }

    fn initialize_schema(&self) -> SqliteResult<()> {
        let conn = self.conn.lock().unwrap();
        conn.execute_batch(get_calendar_schema_sql())
    }

    pub fn create_event(&self, event: &Event) -> SqliteResult<()> {
        let event_type_json = serde_json::to_string(&event.event_type)
            .map_err(|e| rusqlite::Error::ToSqlConversionFailure(Box::new(e)))?;

        let recurrence_json = event
            .recurrence
            .as_ref()
            .map(|r| serde_json::to_string(r).ok())
            .flatten();

        let conn = self.conn.lock().unwrap();
        conn.execute(
            "INSERT INTO calendar_events 
             (id, title, description, event_type, start_time, end_time, 
              all_day, recurrence_pattern, created_at, updated_at, created_by)
             VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11)",
            params![
                event.id.to_string(),
                event.title,
                event.description,
                event_type_json,
                event.start_time.timestamp(),
                event.end_time.map(|t| t.timestamp()),
                event.all_day as i32,
                recurrence_json,
                event.created_at.timestamp(),
                event.updated_at.timestamp(),
                event.created_by,
            ],
        )?;

        self.save_reminders(event)?;
        self.save_attachments(event)?;

        Ok(())
    }

    pub fn get_event(&self, event_id: EventId) -> SqliteResult<Option<Event>> {
        let conn = self.conn.lock().unwrap();
        database_queries::get_event_query(&conn, event_id)
    }

    pub fn get_events_in_range(
        &self,
        start: DateTime<Utc>,
        end: DateTime<Utc>,
    ) -> SqliteResult<Vec<Event>> {
        let conn = self.conn.lock().unwrap();
        database_queries::get_events_in_range_query(&conn, start, end)
    }

    pub fn search_events(&self, query: &str) -> SqliteResult<Vec<Event>> {
        let conn = self.conn.lock().unwrap();
        database_queries::search_events_query(&conn, query)
    }

    pub fn update_event(&self, event: &Event) -> SqliteResult<()> {
        let event_type_json = serde_json::to_string(&event.event_type)
            .map_err(|e| rusqlite::Error::ToSqlConversionFailure(Box::new(e)))?;

        let conn = self.conn.lock().unwrap();
        conn.execute(
            "UPDATE calendar_events 
             SET title = ?1, description = ?2, event_type = ?3, 
                 start_time = ?4, end_time = ?5, updated_at = ?6
             WHERE id = ?7",
            params![
                event.title,
                event.description,
                event_type_json,
                event.start_time.timestamp(),
                event.end_time.map(|t| t.timestamp()),
                event.updated_at.timestamp(),
                event.id.to_string(),
            ],
        )?;

        Ok(())
    }

    pub fn delete_event(&self, event_id: EventId) -> SqliteResult<()> {
        let conn = self.conn.lock().unwrap();
        conn.execute(
            "DELETE FROM calendar_events WHERE id = ?1",
            params![event_id.to_string()],
        )?;
        Ok(())
    }

    fn save_reminders(&self, event: &Event) -> SqliteResult<()> {
        let conn = self.conn.lock().unwrap();
        for reminder in &event.reminders {
            conn.execute(
                "INSERT INTO event_reminders 
                 (id, event_id, minutes_before, notification_sent)
                 VALUES (?1, ?2, ?3, ?4)",
                params![
                    reminder.id.to_string(),
                    event.id.to_string(),
                    reminder.minutes_before,
                    reminder.notification_sent as i32,
                ],
            )?;
        }
        Ok(())
    }

    fn save_attachments(&self, event: &Event) -> SqliteResult<()> {
        let conn = self.conn.lock().unwrap();
        for attachment in &event.attachments {
            let attachment_type = serde_json::to_string(&attachment.attachment_type)
                .map_err(|e| rusqlite::Error::ToSqlConversionFailure(Box::new(e)))?;

            conn.execute(
                "INSERT INTO event_attachments 
                 (id, event_id, attachment_type, reference_id)
                 VALUES (?1, ?2, ?3, ?4)",
                params![
                    attachment.id.to_string(),
                    event.id.to_string(),
                    attachment_type,
                    attachment.reference_id,
                ],
            )?;
        }
        Ok(())
    }
}
