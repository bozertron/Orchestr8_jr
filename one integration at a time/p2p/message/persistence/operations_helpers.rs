use anyhow::Result;
use rusqlite::Connection;

use crate::p2p::message::routing::{DeliveryStatus, TransportMethod};
use crate::p2p::message::types::*;

// Import modular helper components
use super::helpers_delivery::DeliveryHelpers;
use super::helpers_message::MessageHelpers;

/// Helper functions for database operations
pub struct OperationHelpers {
    message_helpers: MessageHelpers,
    delivery_helpers: DeliveryHelpers,
}

impl Default for OperationHelpers {
    fn default() -> Self {
        Self::new()
    }
}

impl OperationHelpers {
    /// Create new operation helpers
    pub fn new() -> Self {
        Self {
            message_helpers: MessageHelpers::new(),
            delivery_helpers: DeliveryHelpers::new(),
        }
    }
    /// Insert message record into database
    pub fn insert_message_record(
        &self,
        conn: &Connection,
        message_id: &MessageId,
        message: &P2PMessage,
        sender_id: Option<&str>,
        recipient_id: Option<&str>,
    ) -> Result<()> {
        self.message_helpers.insert_message_record(
            conn,
            message_id,
            message,
            sender_id,
            recipient_id,
        )
    }

    /// Insert delivery status record
    pub fn insert_delivery_status(
        &self,
        conn: &Connection,
        message_id: &MessageId,
        peer_id: &str,
        status: &DeliveryStatus,
        transport_method: &TransportMethod,
    ) -> Result<()> {
        self.delivery_helpers.insert_delivery_status(
            conn,
            message_id,
            peer_id,
            status,
            transport_method,
        )
    }

    /// Insert routing history record
    pub fn insert_routing_history(
        &self,
        conn: &Connection,
        message_id: &MessageId,
        hop_peer_id: &str,
        transport_method: &TransportMethod,
        success: bool,
        error_details: Option<&str>,
    ) -> Result<()> {
        self.delivery_helpers.insert_routing_history(
            conn,
            message_id,
            hop_peer_id,
            transport_method,
            success,
            error_details,
        )
    }

    /// Convert DeliveryStatus to string representation
    pub fn delivery_status_to_string(status: &DeliveryStatus) -> &'static str {
        DeliveryHelpers::delivery_status_to_string(status)
    }

    /// Convert TransportMethod to string representation
    pub fn transport_method_to_string(transport: &TransportMethod) -> &'static str {
        DeliveryHelpers::transport_method_to_string(transport)
    }

    /// Convert string to DeliveryStatus
    pub fn string_to_delivery_status(status_str: &str) -> DeliveryStatus {
        DeliveryHelpers::string_to_delivery_status(status_str)
    }

    /// Convert string to TransportMethod
    pub fn string_to_transport_method(transport_str: &str) -> TransportMethod {
        DeliveryHelpers::string_to_transport_method(transport_str)
    }

    /// Get message type string from content
    pub fn get_message_type_string(content: &P2PMessage) -> &'static str {
        MessageHelpers::get_message_type_string(content)
    }

    /// Serialize message content to JSON
    pub fn serialize_message_content(content: &P2PMessage) -> Result<String> {
        MessageHelpers::serialize_message_content(content)
    }

    /// Serialize message metadata to JSON
    pub fn serialize_message_metadata(metadata: &StoredMessage) -> Result<String> {
        MessageHelpers::serialize_message_metadata(&metadata.message)
    }

    /// Deserialize message content from JSON
    pub fn deserialize_message_content(json: &str) -> Result<P2PMessage> {
        MessageHelpers::deserialize_message_content(json)
    }

    /// Deserialize message metadata from JSON
    pub fn deserialize_message_metadata(json: &str) -> Result<StoredMessage> {
        MessageHelpers::deserialize_message_metadata(json)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_delivery_status_conversion() {
        assert_eq!(
            OperationHelpers::delivery_status_to_string(&DeliveryStatus::Pending),
            "pending"
        );
        assert_eq!(
            OperationHelpers::delivery_status_to_string(&DeliveryStatus::Sent),
            "sent"
        );
        assert_eq!(
            OperationHelpers::delivery_status_to_string(&DeliveryStatus::Delivered),
            "delivered"
        );
        assert_eq!(
            OperationHelpers::delivery_status_to_string(&DeliveryStatus::Failed(
                "test error".to_string()
            )),
            "failed"
        );
        assert_eq!(
            OperationHelpers::delivery_status_to_string(&DeliveryStatus::Timeout),
            "timeout"
        );

        assert!(matches!(
            OperationHelpers::string_to_delivery_status("pending"),
            DeliveryStatus::Pending
        ));
        assert!(matches!(
            OperationHelpers::string_to_delivery_status("sent"),
            DeliveryStatus::Sent
        ));
        assert!(matches!(
            OperationHelpers::string_to_delivery_status("delivered"),
            DeliveryStatus::Delivered
        ));
        assert!(matches!(
            OperationHelpers::string_to_delivery_status("failed"),
            DeliveryStatus::Failed(_)
        ));
        assert!(matches!(
            OperationHelpers::string_to_delivery_status("timeout"),
            DeliveryStatus::Timeout
        ));
        assert!(matches!(
            OperationHelpers::string_to_delivery_status("invalid"),
            DeliveryStatus::Failed(_)
        ));
    }

    #[test]
    fn test_transport_method_conversion() {
        assert_eq!(
            OperationHelpers::transport_method_to_string(&TransportMethod::LibP2P),
            "libp2p"
        );
        assert_eq!(
            OperationHelpers::transport_method_to_string(&TransportMethod::Relay(
                "test".to_string()
            )),
            "relay"
        );
        assert_eq!(
            OperationHelpers::transport_method_to_string(&TransportMethod::WebRTC(
                "test".to_string()
            )),
            "webrtc"
        );

        assert!(matches!(
            OperationHelpers::string_to_transport_method("libp2p"),
            TransportMethod::LibP2P
        ));
        assert!(matches!(
            OperationHelpers::string_to_transport_method("relay"),
            TransportMethod::Relay(_)
        ));
        assert!(matches!(
            OperationHelpers::string_to_transport_method("webrtc"),
            TransportMethod::WebRTC(_)
        ));
        assert!(matches!(
            OperationHelpers::string_to_transport_method("invalid"),
            TransportMethod::LibP2P
        ));
    }

    #[test]
    fn test_message_type_string() {
        let chat_content = P2PMessage::Chat {
            id: MessageId::new_v4(),
            text: "test".to_string(),
            timestamp: chrono::Utc::now(),
            reply_to: None,
        };
        assert_eq!(
            OperationHelpers::get_message_type_string(&chat_content),
            "chat"
        );

        let ping_content = P2PMessage::Ping {
            nonce: 123,
            timestamp: chrono::Utc::now(),
        };
        assert_eq!(
            OperationHelpers::get_message_type_string(&ping_content),
            "ping"
        );
    }
}
