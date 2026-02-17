use crate::p2p::message::types::MessageId;
use libp2p::PeerId;

/// Event types for message persistence tracking
#[derive(Debug, Clone)]
pub enum PersistenceEventType {
    MessageStored,
    MessageRetrieved,
    DeliveryStatusUpdated,
    MessageDeleted,
    SearchPerformed,
}

/// Persistence event data
#[derive(Debug, Clone)]
pub struct PersistenceEvent {
    pub event_type: PersistenceEventType,
    pub message_id: MessageId,
    pub peer_id: Option<PeerId>,
    pub timestamp: i64,
    pub metadata: Option<String>,
}

impl PersistenceEvent {
    /// Create new persistence event
    pub fn new(
        event_type: PersistenceEventType,
        message_id: MessageId,
        peer_id: Option<PeerId>,
        timestamp: i64,
        metadata: Option<String>,
    ) -> Self {
        Self {
            event_type,
            message_id,
            peer_id,
            timestamp,
            metadata,
        }
    }

    /// Create message stored event
    pub fn message_stored(message_id: MessageId, peer_id: Option<PeerId>, timestamp: i64) -> Self {
        Self::new(
            PersistenceEventType::MessageStored,
            message_id,
            peer_id,
            timestamp,
            None,
        )
    }

    /// Create message retrieved event
    pub fn message_retrieved(
        message_id: MessageId,
        peer_id: Option<PeerId>,
        timestamp: i64,
    ) -> Self {
        Self::new(
            PersistenceEventType::MessageRetrieved,
            message_id,
            peer_id,
            timestamp,
            None,
        )
    }

    /// Create delivery status updated event
    pub fn delivery_status_updated(
        message_id: MessageId,
        peer_id: Option<PeerId>,
        timestamp: i64,
        status_info: Option<String>,
    ) -> Self {
        Self::new(
            PersistenceEventType::DeliveryStatusUpdated,
            message_id,
            peer_id,
            timestamp,
            status_info,
        )
    }

    /// Create message deleted event
    pub fn message_deleted(message_id: MessageId, peer_id: Option<PeerId>, timestamp: i64) -> Self {
        Self::new(
            PersistenceEventType::MessageDeleted,
            message_id,
            peer_id,
            timestamp,
            None,
        )
    }

    /// Create search performed event
    pub fn search_performed(
        message_id: MessageId,
        peer_id: Option<PeerId>,
        timestamp: i64,
        search_query: Option<String>,
    ) -> Self {
        Self::new(
            PersistenceEventType::SearchPerformed,
            message_id,
            peer_id,
            timestamp,
            search_query,
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use libp2p::PeerId;

    #[test]
    fn test_persistence_event_creation() {
        let message_id = MessageId::new_v4();
        let peer_id = Some(PeerId::random());
        let timestamp = chrono::Utc::now().timestamp();

        let event = PersistenceEvent::message_stored(message_id.clone(), peer_id, timestamp);

        assert!(matches!(
            event.event_type,
            PersistenceEventType::MessageStored
        ));
        assert_eq!(event.message_id, message_id);
        assert_eq!(event.peer_id, peer_id);
        assert_eq!(event.timestamp, timestamp);
        assert!(event.metadata.is_none());
    }

    #[test]
    fn test_delivery_status_event_with_metadata() {
        let message_id = MessageId::new_v4();
        let peer_id = Some(PeerId::random());
        let timestamp = chrono::Utc::now().timestamp();
        let status_info = Some("Delivered successfully".to_string());

        let event = PersistenceEvent::delivery_status_updated(
            message_id.clone(),
            peer_id,
            timestamp,
            status_info.clone(),
        );

        assert!(matches!(
            event.event_type,
            PersistenceEventType::DeliveryStatusUpdated
        ));
        assert_eq!(event.message_id, message_id);
        assert_eq!(event.peer_id, peer_id);
        assert_eq!(event.timestamp, timestamp);
        assert_eq!(event.metadata, status_info);
    }
}
