// Calendar Meeting Suggester
// Pattern Bible Compliance: File ≤200 lines, Functions ≤30 lines

#[path = "suggestions_helpers.rs"]
mod suggestions_helpers;

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use suggestions_helpers::{calculate_timezone_score, score_time_slot};

use super::availability::{AvailabilityChecker, TimeSlot, WorkingHours};
use crate::calendar::Event;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MeetingSuggestion {
    pub time_slot: TimeSlot,
    pub score: f64,
    pub reason: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TimeZonePreference {
    pub participant_id: String,
    pub timezone_offset_hours: i32,
}

pub struct MeetingSuggester {
    availability_checker: AvailabilityChecker,
}

impl MeetingSuggester {
    pub fn new(working_hours: WorkingHours) -> Self {
        Self {
            availability_checker: AvailabilityChecker::new(working_hours),
        }
    }

    pub fn suggest_meeting_times(
        &self,
        from: DateTime<Utc>,
        to: DateTime<Utc>,
        duration_minutes: i64,
        participant_calendars: &[Vec<Event>],
    ) -> Vec<MeetingSuggestion> {
        let common_free_slots =
            self.find_common_free_time(from, to, duration_minutes, participant_calendars);

        let mut suggestions: Vec<MeetingSuggestion> = common_free_slots
            .into_iter()
            .map(|slot| score_time_slot(&slot))
            .collect();

        // Sort by score (highest first)
        suggestions.sort_by(|a, b| {
            b.score
                .partial_cmp(&a.score)
                .unwrap_or(std::cmp::Ordering::Equal)
        });

        suggestions
    }

    pub fn suggest_with_timezone_preferences(
        &self,
        from: DateTime<Utc>,
        to: DateTime<Utc>,
        duration_minutes: i64,
        participant_calendars: &[Vec<Event>],
        timezone_prefs: &[TimeZonePreference],
    ) -> Vec<MeetingSuggestion> {
        let mut suggestions =
            self.suggest_meeting_times(from, to, duration_minutes, participant_calendars);

        // Adjust scores based on timezone preferences
        for suggestion in &mut suggestions {
            let tz_score = calculate_timezone_score(&suggestion.time_slot, timezone_prefs);
            suggestion.score *= tz_score;
        }

        // Re-sort after timezone adjustment
        suggestions.sort_by(|a, b| {
            b.score
                .partial_cmp(&a.score)
                .unwrap_or(std::cmp::Ordering::Equal)
        });

        suggestions
    }

    fn find_common_free_time(
        &self,
        from: DateTime<Utc>,
        to: DateTime<Utc>,
        duration_minutes: i64,
        participant_calendars: &[Vec<Event>],
    ) -> Vec<TimeSlot> {
        if participant_calendars.is_empty() {
            return Vec::new();
        }

        // Get free slots for first participant
        let mut common_slots = self.availability_checker.find_free_slots(
            from,
            to,
            duration_minutes,
            &participant_calendars[0],
        );

        // Intersect with other participants' free slots
        for calendar in &participant_calendars[1..] {
            let participant_slots =
                self.availability_checker
                    .find_free_slots(from, to, duration_minutes, calendar);

            common_slots = self.intersect_slots(&common_slots, &participant_slots);
        }

        common_slots
    }

    fn intersect_slots(&self, slots1: &[TimeSlot], slots2: &[TimeSlot]) -> Vec<TimeSlot> {
        let mut intersection = Vec::new();

        for slot1 in slots1 {
            for slot2 in slots2 {
                if slot1.overlaps(slot2) {
                    let start = slot1.start.max(slot2.start);
                    let end = slot1.end.min(slot2.end);
                    intersection.push(TimeSlot::new(start, end));
                }
            }
        }

        intersection
    }
}

impl Default for MeetingSuggester {
    fn default() -> Self {
        Self::new(WorkingHours::default())
    }
}
