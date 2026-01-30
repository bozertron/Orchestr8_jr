// Calendar P2P Synchronization
// Pattern Bible Compliance: File ≤200 lines, Functions ≤30 lines

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use uuid::Uuid;

use crate::calendar::{Event, EventId};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum SyncStatus {
    Pending,
    InProgress,
    Completed,
    Failed,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SyncRecord {
    pub id: Uuid,
    pub event_id: EventId,
    pub peer_id: String,
    pub status: SyncStatus,
    pub last_sync: DateTime<Utc>,
    pub version: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CalendarShare {
    pub id: Uuid,
    pub calendar_owner: String,
    pub shared_with: String,
    pub shared_at: DateTime<Utc>,
    pub permissions: SharePermissions,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum SharePermissions {
    View,
    Edit,
    Admin,
}

pub struct CalendarSync {
    sync_records: HashMap<EventId, SyncRecord>,
    shares: Vec<CalendarShare>,
    local_version: u64,
}

impl CalendarSync {
    pub fn new() -> Self {
        Self {
            sync_records: HashMap::new(),
            shares: Vec::new(),
            local_version: 0,
        }
    }

    pub fn share_calendar(
        &mut self,
        owner: String,
        contact_id: String,
        permissions: SharePermissions,
    ) -> Uuid {
        let share = CalendarShare {
            id: Uuid::new_v4(),
            calendar_owner: owner,
            shared_with: contact_id,
            shared_at: Utc::now(),
            permissions,
        };

        let id = share.id;
        self.shares.push(share);
        id
    }

    pub fn unshare_calendar(&mut self, share_id: Uuid) -> Result<(), String> {
        let initial_len = self.shares.len();
        self.shares.retain(|s| s.id != share_id);

        if self.shares.len() == initial_len {
            return Err("Share not found".to_string());
        }

        Ok(())
    }

    pub fn sync_event(&mut self, event: &Event, peer_id: String) -> Result<Uuid, String> {
        self.local_version += 1;

        let record = SyncRecord {
            id: Uuid::new_v4(),
            event_id: event.id,
            peer_id,
            status: SyncStatus::Pending,
            last_sync: Utc::now(),
            version: self.local_version,
        };

        let id = record.id;
        self.sync_records.insert(event.id, record);
        Ok(id)
    }

    pub fn update_sync_status(
        &mut self,
        event_id: EventId,
        status: SyncStatus,
    ) -> Result<(), String> {
        let record = self
            .sync_records
            .get_mut(&event_id)
            .ok_or("Sync record not found")?;

        record.status = status;
        record.last_sync = Utc::now();

        Ok(())
    }

    pub fn merge_remote_event(&mut self, local_event: &Event, remote_event: &Event) -> Event {
        // Last-write-wins conflict resolution
        if remote_event.updated_at > local_event.updated_at {
            remote_event.clone()
        } else {
            local_event.clone()
        }
    }

    pub fn handle_conflict(&self, local_event: &Event, remote_event: &Event) -> ConflictResolution {
        if local_event.updated_at > remote_event.updated_at {
            ConflictResolution::KeepLocal
        } else if remote_event.updated_at > local_event.updated_at {
            ConflictResolution::KeepRemote
        } else {
            ConflictResolution::Manual
        }
    }

    pub fn get_sync_status(&self, event_id: EventId) -> Option<SyncStatus> {
        self.sync_records.get(&event_id).map(|r| r.status)
    }

    pub fn get_pending_syncs(&self) -> Vec<&SyncRecord> {
        self.sync_records
            .values()
            .filter(|r| r.status == SyncStatus::Pending)
            .collect()
    }

    pub fn get_shared_calendars(&self, user_id: &str) -> Vec<&CalendarShare> {
        self.shares
            .iter()
            .filter(|s| s.shared_with == user_id)
            .collect()
    }

    pub fn has_permission(&self, user_id: &str, required: SharePermissions) -> bool {
        self.shares
            .iter()
            .any(|s| s.shared_with == user_id && s.permissions as u8 >= required as u8)
    }

    pub fn get_local_version(&self) -> u64 {
        self.local_version
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ConflictResolution {
    KeepLocal,
    KeepRemote,
    Manual,
}

impl Default for CalendarSync {
    fn default() -> Self {
        Self::new()
    }
}
