// Helper functions for meeting suggestions
//
// Pattern Bible Compliance:
// - File: Helper module for suggestions.rs
// - Extracted to maintain ≤200 lines per file
// - Contains scoring logic for time slots and timezone preferences

use chrono::Timelike;

use crate::calendar::scheduling::availability::TimeSlot;
use crate::calendar::scheduling::suggestions::{MeetingSuggestion, TimeZonePreference};

/// Score a time slot based on time of day
///
/// Prefers mid-morning (10-11) and early afternoon (14-15)
pub(crate) fn score_time_slot(slot: &TimeSlot) -> MeetingSuggestion {
    let hour = slot.start.time().hour();

    // Prefer mid-morning (10-11) and early afternoon (14-15)
    let time_score = match hour {
        10..=11 => 1.0,
        14..=15 => 0.9,
        9 | 13 => 0.8,
        12 | 16 => 0.7,
        8 | 17 => 0.5,
        _ => 0.3,
    };

    let reason = format!("Meeting at {}:00 (score: {:.1})", hour, time_score * 100.0);

    MeetingSuggestion {
        time_slot: slot.clone(),
        score: time_score,
        reason,
    }
}

/// Calculate timezone score for a time slot
///
/// Scores based on how reasonable the time is for all participants
pub(crate) fn calculate_timezone_score(
    slot: &TimeSlot,
    timezone_prefs: &[TimeZonePreference],
) -> f64 {
    if timezone_prefs.is_empty() {
        return 1.0;
    }

    let mut total_score = 0.0;

    for pref in timezone_prefs {
        let local_hour =
            (slot.start.time().hour() as i32 + pref.timezone_offset_hours).rem_euclid(24) as u32;

        // Score based on local time for participant
        let participant_score = match local_hour {
            9..=17 => 1.0, // Working hours
            8 | 18 => 0.7, // Early/late
            7 | 19 => 0.4, // Very early/late
            _ => 0.1,      // Outside reasonable hours
        };

        total_score += participant_score;
    }

    total_score / timezone_prefs.len() as f64
}
