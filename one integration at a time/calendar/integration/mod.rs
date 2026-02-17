// Calendar Integration Module
// Pattern Bible Compliance: File ≤200 lines, Functions ≤30 lines

pub mod chat;
pub mod contacts;
pub mod documents;

// Re-export core types
pub use chat::{ChatIntegration, ChatLink, EventUpdate, UpdateType};
pub use contacts::{ContactIntegration, Invitation, Participant, RsvpStatus};
pub use documents::{AccessLevel, DocumentAccess, DocumentAttachment, DocumentIntegration};
