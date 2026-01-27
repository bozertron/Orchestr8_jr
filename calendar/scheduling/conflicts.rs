// Calendar Conflict Detector
// Pattern Bible Compliance: File ≤200 lines, Functions ≤30 lines

use chrono::{DateTime, Duration, Utc};
use serde::{Deserialize, Serialize};

use super::availability::TimeSlot;
use crate::calendar::{Event, EventId};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Conflict {
    pub event1_id: EventId,
    pub event2_id: EventId,
    pub overlap_start: DateTime<Utc>,
    pub overlap_end: DateTime<Utc>,
    pub severity: ConflictSeverity,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum ConflictSeverity {
    Minor,    // Partial overlap
    Major,    // Significant overlap
    Critical, // Complete overlap
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConflictResolution {
    pub resolution_type: ResolutionType,
    pub suggested_time: Option<DateTime<Utc>>,
    pub reason: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ResolutionType {
    RescheduleFirst,
    RescheduleSecond,
    ShortenFirst,
    ShortenSecond,
    Cancel,
}

pub struct ConflictDetector;

impl ConflictDetector {
    pub fn new() -> Self {
        Self
    }

    pub fn detect_conflicts(&self, events: &[Event]) -> Vec<Conflict> {
        let mut conflicts = Vec::new();

        for i in 0..events.len() {
            for j in (i + 1)..events.len() {
                if let Some(conflict) = self.check_conflict(&events[i], &events[j]) {
                    conflicts.push(conflict);
                }
            }
        }

        conflicts
    }

    pub fn check_conflict(&self, event1: &Event, event2: &Event) -> Option<Conflict> {
        let slot1 = self.event_to_slot(event1);
        let slot2 = self.event_to_slot(event2);

        if !slot1.overlaps(&slot2) {
            return None;
        }

        let overlap_start = slot1.start.max(slot2.start);
        let overlap_end = slot1.end.min(slot2.end);
        let severity = self.calculate_severity(&slot1, &slot2, overlap_start, overlap_end);

        Some(Conflict {
            event1_id: event1.id,
            event2_id: event2.id,
            overlap_start,
            overlap_end,
            severity,
        })
    }

    pub fn check_participant_conflicts(
        &self,
        participant_id: &str,
        events: &[Event],
    ) -> Vec<Conflict> {
        let participant_events: Vec<&Event> = events
            .iter()
            .filter(|e| self.has_participant(e, participant_id))
            .collect();

        let mut conflicts = Vec::new();
        for i in 0..participant_events.len() {
            for j in (i + 1)..participant_events.len() {
                if let Some(conflict) =
                    self.check_conflict(participant_events[i], participant_events[j])
                {
                    conflicts.push(conflict);
                }
            }
        }

        conflicts
    }

    pub fn is_double_booked(&self, time_slot: &TimeSlot, events: &[Event]) -> bool {
        events
            .iter()
            .filter(|e| {
                let event_slot = self.event_to_slot(e);
                time_slot.overlaps(&event_slot)
            })
            .count()
            > 1
    }

    pub fn suggest_resolution(&self, conflict: &Conflict) -> ConflictResolution {
        match conflict.severity {
            ConflictSeverity::Minor => ConflictResolution {
                resolution_type: ResolutionType::ShortenFirst,
                suggested_time: Some(conflict.overlap_end),
                reason: "Minor overlap - suggest shortening first event".to_string(),
            },
            ConflictSeverity::Major => ConflictResolution {
                resolution_type: ResolutionType::RescheduleSecond,
                suggested_time: Some(conflict.overlap_end + Duration::hours(1)),
                reason: "Major overlap - suggest rescheduling second event".to_string(),
            },
            ConflictSeverity::Critical => ConflictResolution {
                resolution_type: ResolutionType::Cancel,
                suggested_time: None,
                reason: "Critical overlap - one event must be cancelled".to_string(),
            },
        }
    }

    fn event_to_slot(&self, event: &Event) -> TimeSlot {
        TimeSlot::new(
            event.start_time,
            event
                .end_time
                .unwrap_or(event.start_time + Duration::hours(1)),
        )
    }

    fn calculate_severity(
        &self,
        slot1: &TimeSlot,
        slot2: &TimeSlot,
        overlap_start: DateTime<Utc>,
        overlap_end: DateTime<Utc>,
    ) -> ConflictSeverity {
        let overlap_minutes = (overlap_end - overlap_start).num_minutes();
        let slot1_minutes = slot1.duration_minutes();
        let slot2_minutes = slot2.duration_minutes();

        let overlap_percentage =
            (overlap_minutes as f64) / (slot1_minutes.min(slot2_minutes) as f64) * 100.0;

        if overlap_percentage >= 80.0 {
            ConflictSeverity::Critical
        } else if overlap_percentage >= 40.0 {
            ConflictSeverity::Major
        } else {
            ConflictSeverity::Minor
        }
    }

    fn has_participant(&self, event: &Event, participant_id: &str) -> bool {
        match &event.event_type {
            crate::calendar::EventType::Meeting { participants, .. } => {
                participants.contains(&participant_id.to_string())
            }
            _ => false,
        }
    }
}

impl Default for ConflictDetector {
    fn default() -> Self {
        Self::new()
    }
}
