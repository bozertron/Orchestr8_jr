#[cfg(test)]
mod tests {
    use super::super::*;
    use tempfile::tempdir;
    use std::sync::Arc;
    use crate::p2p::message::persistence::{ConnectionManager, SchemaManager};

    #[tokio::test]
    async fn test_delivery_status_update_with_error() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = Arc::new(ConnectionManager::create_pool(&db_path).unwrap());
        
        SchemaManager::initialize_schema(&pool).unwrap();
        let ops = PersistenceOperations::new(pool);

        // Store a message
        let message_id = MessageId::new_v4();
        let peer_id = PeerId::random();
        let message = P2PMessage::new_chat("test message".to_string());

        ops.store_sent_message(
            &message_id,
            &peer_id,
            &message,
            &TransportMethod::Direct,
        ).await.unwrap();

        // Update with error message
        ops.update_delivery_status(
            &message_id,
            &peer_id,
            &DeliveryStatus::Failed("test error".to_string()),
            Some("Connection timeout"),
        ).await.unwrap();
    }

    #[tokio::test]
    async fn test_multiple_delivery_statuses() {
        let (ops, message_id, peer1, peer2, message) = Self::setup_multiple_delivery_test().await;

        Self::store_initial_message(&ops, &message_id, &peer1, &message).await;
        Self::add_second_peer_delivery(&ops, &message_id, &peer2).await;
        Self::update_delivery_statuses(&ops, &message_id, &peer1, &peer2).await;
    }

    async fn setup_multiple_delivery_test() -> (PersistenceOperations, MessageId, PeerId, PeerId, P2PMessage) {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = Arc::new(ConnectionManager::create_pool(&db_path).unwrap());
        SchemaManager::initialize_schema(&pool).unwrap();
        let ops = PersistenceOperations::new(pool);

        let message_id = MessageId::new_v4();
        let peer1 = PeerId::random();
        let peer2 = PeerId::random();
        let message = P2PMessage::new_chat("broadcast message".to_string());

        (ops, message_id, peer1, peer2, message)
    }

    async fn store_initial_message(
        ops: &PersistenceOperations,
        message_id: &MessageId,
        peer1: &PeerId,
        message: &P2PMessage,
    ) {
        ops.store_sent_message(message_id, peer1, message, &TransportMethod::Direct).await.unwrap();
    }

    async fn add_second_peer_delivery(
        ops: &PersistenceOperations,
        message_id: &MessageId,
        peer2: &PeerId,
    ) {
        let pool_clone = ops.pool.clone();
        let message_id = message_id.clone();
        let peer2 = peer2.to_string();
        tokio::task::spawn_blocking(move || {
            let conn = pool_clone.get().unwrap();
            PersistenceOperations::insert_delivery_status(
                &conn, &message_id, &peer2, &DeliveryStatus::Pending, &TransportMethod::Relay
            )
        }).await.unwrap().unwrap();
    }

    async fn update_delivery_statuses(
        ops: &PersistenceOperations,
        message_id: &MessageId,
        peer1: &PeerId,
        peer2: &PeerId,
    ) {
        ops.update_delivery_status(message_id, peer1, &DeliveryStatus::Delivered, None).await.unwrap();
        ops.update_delivery_status(message_id, peer2, &DeliveryStatus::Failed("Peer unreachable".to_string()), Some("Peer unreachable")).await.unwrap();
    }

    #[tokio::test]
    async fn test_concurrent_operations() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = Arc::new(ConnectionManager::create_pool(&db_path).unwrap());
        
        SchemaManager::initialize_schema(&pool).unwrap();
        let ops = Arc::new(PersistenceOperations::new(pool));

        let peer_id = PeerId::random();
        
        // Spawn multiple concurrent operations
        let mut handles = Vec::new();
        
        for i in 0..10 {
            let ops_clone = ops.clone();
            let peer_id_clone = peer_id;
            
            let handle = tokio::spawn(async move {
                let message = P2PMessage::new_chat(format!("message {}", i));
                ops_clone.store_received_message(&message, &peer_id_clone, None).await
            });
            
            handles.push(handle);
        }

        // Wait for all operations to complete
        for handle in handles {
            handle.await.unwrap().unwrap();
        }
    }

    #[tokio::test]
    async fn test_large_message_storage() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = Arc::new(ConnectionManager::create_pool(&db_path).unwrap());
        
        SchemaManager::initialize_schema(&pool).unwrap();
        let ops = PersistenceOperations::new(pool);

        let peer_id = PeerId::random();
        
        // Create a large message (1MB of data)
        let large_content = "x".repeat(1024 * 1024);
        let large_message = P2PMessage::new_chat(large_content);

        // Should handle large messages without issues
        let stored_id = ops.store_received_message(&large_message, &peer_id, None).await.unwrap();
        assert!(!stored_id.to_string().is_empty());
    }

    #[tokio::test]
    async fn test_delivery_status_transitions() {
        let (ops, message_id, peer_id, message) = Self::setup_status_transition_test().await;

        Self::store_message_for_transition(&ops, &message_id, &peer_id, &message).await;
        Self::execute_status_transitions(&ops, &message_id, &peer_id).await;
    }

    async fn setup_status_transition_test() -> (PersistenceOperations, MessageId, PeerId, P2PMessage) {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = Arc::new(ConnectionManager::create_pool(&db_path).unwrap());
        SchemaManager::initialize_schema(&pool).unwrap();
        let ops = PersistenceOperations::new(pool);

        let message_id = MessageId::new_v4();
        let peer_id = PeerId::random();
        let message = P2PMessage::new_chat("status transition test".to_string());

        (ops, message_id, peer_id, message)
    }

    async fn store_message_for_transition(
        ops: &PersistenceOperations,
        message_id: &MessageId,
        peer_id: &PeerId,
        message: &P2PMessage,
    ) {
        ops.store_sent_message(message_id, peer_id, message, &TransportMethod::Direct).await.unwrap();
    }

    async fn execute_status_transitions(
        ops: &PersistenceOperations,
        message_id: &MessageId,
        peer_id: &PeerId,
    ) {
        // Test status transitions: Pending -> InTransit -> Delivered
        ops.update_delivery_status(message_id, peer_id, &DeliveryStatus::InTransit, None).await.unwrap();
        ops.update_delivery_status(message_id, peer_id, &DeliveryStatus::Delivered, None).await.unwrap();
    }
}
