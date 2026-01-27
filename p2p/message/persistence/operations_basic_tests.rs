#[cfg(test)]
mod tests {
    use super::super::*;
    use tempfile::tempdir;
    use std::sync::Arc;
    use crate::p2p::message::persistence::{ConnectionManager, SchemaManager};

    #[tokio::test]
    async fn test_store_sent_message() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = Arc::new(ConnectionManager::create_pool(&db_path).unwrap());
        
        SchemaManager::initialize_schema(&pool).unwrap();
        let ops = PersistenceOperations::new(pool);

        let message_id = MessageId::generate();
        let peer_id = PeerId::random();
        let message = P2PMessage::new_chat("test message".to_string());

        ops.store_sent_message(
            &message_id,
            &peer_id,
            &message,
            &TransportMethod::Direct,
        ).await.unwrap();
    }

    #[tokio::test]
    async fn test_store_received_message() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = Arc::new(ConnectionManager::create_pool(&db_path).unwrap());
        
        SchemaManager::initialize_schema(&pool).unwrap();
        let ops = PersistenceOperations::new(pool);

        let peer_id = PeerId::random();
        let message = P2PMessage::new_chat("received message".to_string());

        let stored_id = ops.store_received_message(
            &message,
            &peer_id,
            None,
        ).await.unwrap();

        assert!(!stored_id.to_string().is_empty());
    }

    #[tokio::test]
    async fn test_update_delivery_status() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = Arc::new(ConnectionManager::create_pool(&db_path).unwrap());
        
        SchemaManager::initialize_schema(&pool).unwrap();
        let ops = PersistenceOperations::new(pool);

        // First store a message
        let message_id = MessageId::generate();
        let peer_id = PeerId::random();
        let message = P2PMessage::new_chat("test message".to_string());

        ops.store_sent_message(
            &message_id,
            &peer_id,
            &message,
            &TransportMethod::Direct,
        ).await.unwrap();

        // Then update its delivery status
        ops.update_delivery_status(
            &message_id,
            &peer_id,
            &DeliveryStatus::Delivered,
            None,
        ).await.unwrap();
    }

    #[tokio::test]
    async fn test_delete_message() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = Arc::new(ConnectionManager::create_pool(&db_path).unwrap());
        
        SchemaManager::initialize_schema(&pool).unwrap();
        let ops = PersistenceOperations::new(pool);

        // Store a message
        let message_id = MessageId::generate();
        let peer_id = PeerId::random();
        let message = P2PMessage::new_chat("test message".to_string());

        ops.store_sent_message(
            &message_id,
            &peer_id,
            &message,
            &TransportMethod::Direct,
        ).await.unwrap();

        // Delete the message
        let deleted = ops.delete_message(&message_id).await.unwrap();
        assert!(deleted);

        // Try to delete again - should return false
        let deleted_again = ops.delete_message(&message_id).await.unwrap();
        assert!(!deleted_again);
    }

    #[tokio::test]
    async fn test_store_received_message_with_id() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = Arc::new(ConnectionManager::create_pool(&db_path).unwrap());
        
        SchemaManager::initialize_schema(&pool).unwrap();
        let ops = PersistenceOperations::new(pool);

        let peer_id = PeerId::random();
        let message = P2PMessage::new_chat("received message".to_string());
        let expected_id = MessageId::generate();

        let stored_id = ops.store_received_message(
            &message,
            &peer_id,
            Some(expected_id.clone()),
        ).await.unwrap();

        assert_eq!(stored_id, expected_id);
    }

    #[tokio::test]
    async fn test_message_types() {
        let temp_dir = tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let pool = Arc::new(ConnectionManager::create_pool(&db_path).unwrap());
        
        SchemaManager::initialize_schema(&pool).unwrap();
        let ops = PersistenceOperations::new(pool);

        let peer_id = PeerId::random();

        // Test different message types
        let chat_message = P2PMessage::new_chat("chat message".to_string());
        let file_message = P2PMessage::new_file_transfer("file.txt".to_string(), vec![1, 2, 3]);
        let control_message = P2PMessage::new_control("ping".to_string());

        // Store each type
        ops.store_received_message(&chat_message, &peer_id, None).await.unwrap();
        ops.store_received_message(&file_message, &peer_id, None).await.unwrap();
        ops.store_received_message(&control_message, &peer_id, None).await.unwrap();
    }
}
