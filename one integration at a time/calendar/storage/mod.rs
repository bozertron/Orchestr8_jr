// Calendar Storage Module
// Pattern Bible Compliance: File ≤200 lines, Functions ≤30 lines

pub mod database;
pub mod sync;

// Re-export core types
pub use database::CalendarStorage;
pub use sync::{
    CalendarShare, CalendarSync, ConflictResolution, SharePermissions, SyncRecord, SyncStatus,
};
