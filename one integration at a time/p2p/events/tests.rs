#[cfg(test)]
mod tests {
    use super::super::bus::EventBus;
    use super::super::handlers::EventHandlerRegistry;
    use super::super::subscriptions::SubscriptionManager;
    use super::super::P2PEventType;
    use std::sync::Arc;
    use std::time::Duration;
    use tokio::sync::RwLock;

    /// Test EventBus creation
    #[tokio::test]
    async fn test_event_bus_creation() {
        let event_bus = EventBus::new();
        let count = event_bus.subscriber_count().await;

        assert_eq!(count, 0, "Initial subscriber count should be 0");
    }

    /// Test event publishing
    #[tokio::test]
    async fn test_event_publishing() {
        let event_bus = EventBus::new();
        let event = P2PEventType::ServiceStarted;

        let result = event_bus.publish(event).await;
        assert!(result.is_ok(), "Event publishing should succeed");
    }

    /// Test event subscription
    #[tokio::test]
    async fn test_event_subscription() {
        let event_bus = EventBus::new();

        let _receiver = event_bus.subscribe().await;
        let count = event_bus.subscriber_count().await;

        assert_eq!(count, 1, "Subscriber count should be 1 after subscription");
    }

    /// Test event delivery
    #[tokio::test]
    async fn test_event_delivery() {
        let event_bus = EventBus::new();
        let mut receiver = event_bus.subscribe().await;

        let event = P2PEventType::ServiceStarted;
        event_bus.publish(event.clone()).await.unwrap();

        // Try to receive the event with timeout
        let result = tokio::time::timeout(Duration::from_millis(100), receiver.recv()).await;

        assert!(result.is_ok(), "Should receive event within timeout");
        let received_event = result.unwrap();
        assert!(received_event.is_ok(), "Received event should be Ok");
    }

    /// Test multiple subscribers
    #[tokio::test]
    async fn test_multiple_subscribers() {
        let event_bus = EventBus::new();

        let mut receiver1 = event_bus.subscribe().await;
        let mut receiver2 = event_bus.subscribe().await;

        let count = event_bus.subscriber_count().await;
        assert_eq!(count, 2, "Should have 2 subscribers");

        let event = P2PEventType::ServiceStarted;
        event_bus.publish(event).await.unwrap();

        // Both receivers should get the event
        let result1 = tokio::time::timeout(Duration::from_millis(100), receiver1.recv()).await;
        let result2 = tokio::time::timeout(Duration::from_millis(100), receiver2.recv()).await;

        assert!(result1.is_ok(), "Receiver 1 should get event");
        assert!(result2.is_ok(), "Receiver 2 should get event");
    }
}

#[cfg(test)]
mod handler_tests {
    use super::super::handlers::EventHandlerRegistry;
    use super::super::P2PEventType;
    use std::sync::Arc;

    /// Test handler clearing
    #[tokio::test]
    async fn test_handler_clearing() {
        let registry = EventHandlerRegistry::new();

        let handler = Arc::new(|_event: P2PEventType| Ok(()));

        registry
            .register_handler("test_event", handler)
            .await
            .unwrap();

        let result = registry.clear_handlers().await;
        assert!(result.is_ok(), "Handler clearing should succeed");

        let count = registry.handler_count("test_event").await;
        assert_eq!(count, 0, "Handler count should be 0 after clearing");
    }
}
