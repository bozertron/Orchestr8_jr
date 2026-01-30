// Calendar Database Query Builders
// Pattern Bible Compliance: File ≤200 lines, Functions ≤30 lines
// Solves: Complex query builders separated from core operations

use chrono::{DateTime, Utc};
use rusqlite::{params, Connection, Result as SqliteResult, Row};
use serde_json;

use crate::calendar::{Event, EventId};

/// Get single event by ID
pub fn get_event_query(conn: &Connection, event_id: EventId) -> SqliteResult<Option<Event>> {
    let mut stmt = conn.prepare(
        "SELECT id, title, description, event_type, start_time, end_time,
                all_day, recurrence_pattern, created_at, updated_at, created_by
         FROM calendar_events WHERE id = ?1",
    )?;

    let result = stmt.query_row(params![event_id.to_string()], |row| row_to_event(row));

    match result {
        Ok(event) => Ok(Some(event)),
        Err(rusqlite::Error::QueryReturnedNoRows) => Ok(None),
        Err(e) => Err(e),
    }
}

/// Get events in time range
pub fn get_events_in_range_query(
    conn: &Connection,
    start: DateTime<Utc>,
    end: DateTime<Utc>,
) -> SqliteResult<Vec<Event>> {
    let mut stmt = conn.prepare(
        "SELECT id, title, description, event_type, start_time, end_time,
                all_day, recurrence_pattern, created_at, updated_at, created_by
         FROM calendar_events 
         WHERE start_time >= ?1 AND start_time <= ?2
         ORDER BY start_time ASC",
    )?;

    let events = stmt
        .query_map(params![start.timestamp(), end.timestamp()], |row| {
            row_to_event(row)
        })?
        .collect::<SqliteResult<Vec<Event>>>()?;

    Ok(events)
}

/// Search events by text query
pub fn search_events_query(conn: &Connection, query: &str) -> SqliteResult<Vec<Event>> {
    let search_pattern = format!("%{}%", query);
    let mut stmt = conn.prepare(
        "SELECT id, title, description, event_type, start_time, end_time,
                all_day, recurrence_pattern, created_at, updated_at, created_by
         FROM calendar_events 
         WHERE title LIKE ?1 OR description LIKE ?1
         ORDER BY start_time DESC",
    )?;

    let events = stmt
        .query_map(params![search_pattern], |row| row_to_event(row))?
        .collect::<SqliteResult<Vec<Event>>>()?;

    Ok(events)
}

/// Convert database row to Event
pub fn row_to_event(row: &Row) -> SqliteResult<Event> {
    // Simplified event reconstruction - full implementation would load reminders/attachments
    Ok(Event::new(
        row.get(1)?,
        serde_json::from_str(&row.get::<_, String>(3)?).unwrap(),
        DateTime::from_timestamp(row.get(4)?, 0).unwrap(),
        row.get(10)?,
    ))
}
