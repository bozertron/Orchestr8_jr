pub mod decision;
pub mod delivery;
pub mod errors;
pub mod health;
pub mod operations;
pub mod retry;
pub mod service;
pub mod smart_retry;
pub mod transport;

pub use decision::RoutingDecisionEngine;
pub use errors::RoutingError;
pub use health::{TransportHealthMonitor, TransportStats};
pub use service::RoutingService;
pub use smart_retry::{AdaptiveRetryDelay, SmartRetryStrategy};

// Re-export main service for backward compatibility
pub use service::RoutingService as RoutingServiceImpl;

use super::types::*;
use libp2p::PeerId;
use std::time::Instant;

/// Delivery status for message tracking
#[derive(Debug, Clone, PartialEq)]
pub enum DeliveryStatus {
    Pending,
    Sent,
    Delivered,
    Failed(String),
    Timeout,
}

/// Transport method for message delivery
#[derive(Debug, Clone)]
pub enum TransportMethod {
    WebRTC(String), // channel_id
    LibP2P,
    Relay(String), // relay_address
}

/// Delivery tracking information
#[derive(Debug, Clone)]
pub struct DeliveryInfo {
    pub message_id: MessageId,
    pub to: PeerId,
    pub status: DeliveryStatus,
    pub transport: TransportMethod,
    pub created_at: Instant,
    pub attempts: u32,
    pub last_attempt: Option<Instant>,
}
