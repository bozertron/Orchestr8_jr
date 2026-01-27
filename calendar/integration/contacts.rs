// Calendar Contact Integration
// Pattern Bible Compliance: File ≤200 lines, Functions ≤30 lines

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::calendar::EventId;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum RsvpStatus {
    NoResponse,
    Accepted,
    Declined,
    Tentative,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Participant {
    pub contact_id: String,
    pub rsvp_status: RsvpStatus,
    pub responded_at: Option<DateTime<Utc>>,
    pub is_organizer: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Invitation {
    pub id: Uuid,
    pub event_id: EventId,
    pub contact_id: String,
    pub sent_at: DateTime<Utc>,
    pub message: Option<String>,
}

pub struct ContactIntegration {
    participants: Vec<Participant>,
    invitations: Vec<Invitation>,
}

impl ContactIntegration {
    pub fn new() -> Self {
        Self {
            participants: Vec::new(),
            invitations: Vec::new(),
        }
    }

    pub fn add_participant(
        &mut self,
        contact_id: String,
        is_organizer: bool,
    ) -> Result<(), String> {
        if self.has_participant(&contact_id) {
            return Err("Participant already added".to_string());
        }

        self.participants.push(Participant {
            contact_id,
            rsvp_status: RsvpStatus::NoResponse,
            responded_at: None,
            is_organizer,
        });

        Ok(())
    }

    pub fn remove_participant(&mut self, contact_id: &str) -> Result<(), String> {
        let initial_len = self.participants.len();
        self.participants.retain(|p| p.contact_id != contact_id);

        if self.participants.len() == initial_len {
            return Err("Participant not found".to_string());
        }

        Ok(())
    }

    pub fn update_rsvp(&mut self, contact_id: &str, status: RsvpStatus) -> Result<(), String> {
        let participant = self
            .participants
            .iter_mut()
            .find(|p| p.contact_id == contact_id)
            .ok_or("Participant not found")?;

        participant.rsvp_status = status;
        participant.responded_at = Some(Utc::now());

        Ok(())
    }

    pub fn send_invitation(
        &mut self,
        event_id: EventId,
        contact_id: String,
        message: Option<String>,
    ) -> Uuid {
        let invitation = Invitation {
            id: Uuid::new_v4(),
            event_id,
            contact_id,
            sent_at: Utc::now(),
            message,
        };

        let id = invitation.id;
        self.invitations.push(invitation);
        id
    }

    pub fn get_participants(&self) -> &[Participant] {
        &self.participants
    }

    pub fn get_participant(&self, contact_id: &str) -> Option<&Participant> {
        self.participants
            .iter()
            .find(|p| p.contact_id == contact_id)
    }

    pub fn get_accepted_participants(&self) -> Vec<&Participant> {
        self.participants
            .iter()
            .filter(|p| p.rsvp_status == RsvpStatus::Accepted)
            .collect()
    }

    pub fn get_pending_responses(&self) -> Vec<&Participant> {
        self.participants
            .iter()
            .filter(|p| p.rsvp_status == RsvpStatus::NoResponse)
            .collect()
    }

    pub fn has_participant(&self, contact_id: &str) -> bool {
        self.participants.iter().any(|p| p.contact_id == contact_id)
    }

    pub fn get_invitations_for_event(&self, event_id: EventId) -> Vec<&Invitation> {
        self.invitations
            .iter()
            .filter(|i| i.event_id == event_id)
            .collect()
    }
}

impl Default for ContactIntegration {
    fn default() -> Self {
        Self::new()
    }
}
