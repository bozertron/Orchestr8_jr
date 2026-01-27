// Calendar Scheduling Module
// Pattern Bible Compliance: File ≤200 lines, Functions ≤30 lines

pub mod availability;
pub mod conflicts;
pub mod suggestions;

// Re-export core types
pub use availability::{AvailabilityChecker, TimeSlot, WorkingHours};
pub use conflicts::{
    Conflict, ConflictDetector, ConflictResolution, ConflictSeverity, ResolutionType,
};
pub use suggestions::{MeetingSuggester, MeetingSuggestion, TimeZonePreference};
