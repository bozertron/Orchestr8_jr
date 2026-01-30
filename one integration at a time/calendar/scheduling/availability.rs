// Calendar Availability Checker
// Pattern Bible Compliance: File ≤200 lines, Functions ≤30 lines

use chrono::{DateTime, Datelike, Duration, NaiveTime, Utc, Weekday};
use serde::{Deserialize, Serialize};

use crate::calendar::Event;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WorkingHours {
    pub start_time: NaiveTime,
    pub end_time: NaiveTime,
    pub working_days: Vec<Weekday>,
}

impl Default for WorkingHours {
    fn default() -> Self {
        Self {
            start_time: NaiveTime::from_hms_opt(9, 0, 0).unwrap(),
            end_time: NaiveTime::from_hms_opt(17, 0, 0).unwrap(),
            working_days: vec![
                Weekday::Mon,
                Weekday::Tue,
                Weekday::Wed,
                Weekday::Thu,
                Weekday::Fri,
            ],
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TimeSlot {
    pub start: DateTime<Utc>,
    pub end: DateTime<Utc>,
}

impl TimeSlot {
    pub fn new(start: DateTime<Utc>, end: DateTime<Utc>) -> Self {
        Self { start, end }
    }

    pub fn duration_minutes(&self) -> i64 {
        (self.end - self.start).num_minutes()
    }

    pub fn overlaps(&self, other: &TimeSlot) -> bool {
        self.start < other.end && other.start < self.end
    }
}

pub struct AvailabilityChecker {
    working_hours: WorkingHours,
}

impl AvailabilityChecker {
    pub fn new(working_hours: WorkingHours) -> Self {
        Self { working_hours }
    }

    pub fn is_available(&self, time_slot: &TimeSlot, events: &[Event]) -> bool {
        // Check if slot is within working hours
        if !self.is_within_working_hours(time_slot) {
            return false;
        }

        // Check for conflicts with existing events
        !self.has_conflicts(time_slot, events)
    }

    pub fn find_free_slots(
        &self,
        from: DateTime<Utc>,
        to: DateTime<Utc>,
        duration_minutes: i64,
        events: &[Event],
    ) -> Vec<TimeSlot> {
        let mut free_slots = Vec::new();
        let mut current = from;

        while current < to {
            let slot_end = current + Duration::minutes(duration_minutes);

            if slot_end > to {
                break;
            }

            let slot = TimeSlot::new(current, slot_end);

            if self.is_available(&slot, events) {
                free_slots.push(slot);
            }

            // Move to next potential slot (15-minute increments)
            current = current + Duration::minutes(15);
        }

        free_slots
    }

    pub fn calculate_busy_percentage(
        &self,
        from: DateTime<Utc>,
        to: DateTime<Utc>,
        events: &[Event],
    ) -> f64 {
        let total_minutes = (to - from).num_minutes() as f64;
        if total_minutes == 0.0 {
            return 0.0;
        }

        let busy_minutes = self.calculate_busy_minutes(from, to, events);
        (busy_minutes / total_minutes) * 100.0
    }

    fn is_within_working_hours(&self, slot: &TimeSlot) -> bool {
        let start_time = slot.start.time();
        let end_time = slot.end.time();
        let weekday = slot.start.weekday();

        // Check if day is a working day
        if !self.working_hours.working_days.contains(&weekday) {
            return false;
        }

        // Check if time is within working hours
        start_time >= self.working_hours.start_time && end_time <= self.working_hours.end_time
    }

    fn has_conflicts(&self, slot: &TimeSlot, events: &[Event]) -> bool {
        events.iter().any(|event| {
            let event_slot = TimeSlot::new(
                event.start_time,
                event
                    .end_time
                    .unwrap_or(event.start_time + Duration::hours(1)),
            );
            slot.overlaps(&event_slot)
        })
    }

    fn calculate_busy_minutes(
        &self,
        from: DateTime<Utc>,
        to: DateTime<Utc>,
        events: &[Event],
    ) -> f64 {
        let mut busy_minutes = 0.0;

        for event in events {
            let event_start = event.start_time.max(from);
            let event_end = event
                .end_time
                .unwrap_or(event.start_time + Duration::hours(1))
                .min(to);

            if event_start < event_end {
                busy_minutes += (event_end - event_start).num_minutes() as f64;
            }
        }

        busy_minutes
    }

    pub fn get_working_hours(&self) -> &WorkingHours {
        &self.working_hours
    }

    pub fn update_working_hours(&mut self, working_hours: WorkingHours) {
        self.working_hours = working_hours;
    }
}

impl Default for AvailabilityChecker {
    fn default() -> Self {
        Self::new(WorkingHours::default())
    }
}
