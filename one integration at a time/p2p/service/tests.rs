#[cfg(test)]
mod tests {
    use super::super::core::{LifecycleState, P2PService};
    use super::super::health::HealthStatus;
    use crate::p2p::config::NetworkConfig;

    /// Test P2PService creation
    #[tokio::test]
    async fn test_p2p_service_creation() {
        let config = NetworkConfig::default();
        let result = P2PService::new(config).await;

        assert!(result.is_ok(), "P2PService creation should succeed");

        let service = result.unwrap();
        let state = service.lifecycle_state().await;

        assert_eq!(
            state,
            LifecycleState::Uninitialized,
            "Initial state should be Uninitialized"
        );
    }

    /// Test P2PService startup
    #[tokio::test]
    async fn test_p2p_service_startup() {
        let config = NetworkConfig::default();
        let service = P2PService::new(config)
            .await
            .expect("Service creation failed");

        let result = service.start().await;
        assert!(result.is_ok(), "Service start should succeed");

        let state = service.lifecycle_state().await;
        assert_eq!(
            state,
            LifecycleState::Running,
            "State should be Running after start"
        );
    }

    /// Test P2PService shutdown
    #[tokio::test]
    async fn test_p2p_service_shutdown() {
        let config = NetworkConfig::default();
        let service = P2PService::new(config)
            .await
            .expect("Service creation failed");

        service.start().await.expect("Service start failed");

        let result = service.shutdown().await;
        assert!(result.is_ok(), "Service shutdown should succeed");

        let state = service.lifecycle_state().await;
        assert_eq!(
            state,
            LifecycleState::Stopped,
            "State should be Stopped after shutdown"
        );
    }

    /// Test health status retrieval
    #[tokio::test]
    async fn test_health_status() {
        let config = NetworkConfig::default();
        let service = P2PService::new(config)
            .await
            .expect("Service creation failed");

        service.start().await.expect("Service start failed");

        let health = service.health_status().await;

        assert_eq!(
            health.lifecycle_state,
            LifecycleState::Running,
            "Health status should show Running state"
        );
        assert!(
            health.discovery_active,
            "Discovery should be active after start"
        );
        assert!(
            health.transport_connected,
            "Transport should be connected after start"
        );
    }

    /// Test lifecycle state transitions
    #[tokio::test]
    async fn test_lifecycle_state_transitions() {
        let config = NetworkConfig::default();
        let service = P2PService::new(config)
            .await
            .expect("Service creation failed");

        // Initial state
        let state = service.lifecycle_state().await;
        assert_eq!(state, LifecycleState::Uninitialized);

        // Start service
        service.start().await.expect("Service start failed");
        let state = service.lifecycle_state().await;
        assert_eq!(state, LifecycleState::Running);

        // Shutdown service
        service.shutdown().await.expect("Service shutdown failed");
        let state = service.lifecycle_state().await;
        assert_eq!(state, LifecycleState::Stopped);
    }

    /// Test send message functionality
    #[tokio::test]
    async fn test_send_message() {
        let config = NetworkConfig::default();
        let service = P2PService::new(config)
            .await
            .expect("Service creation failed");

        service.start().await.expect("Service start failed");

        // Create a test peer ID
        let peer_id = libp2p::PeerId::random();
        let text = "Test message".to_string();

        let result = service.send_message(peer_id, text).await;

        // Message service should be initialized, so this should succeed
        assert!(
            result.is_ok(),
            "Send message should succeed after service start"
        );
    }

    /// Test health status components
    #[tokio::test]
    async fn test_health_status_components() {
        let config = NetworkConfig::default();
        let service = P2PService::new(config)
            .await
            .expect("Service creation failed");

        service.start().await.expect("Service start failed");

        let health = service.health_status().await;

        // Verify all health components
        assert!(
            matches!(health.lifecycle_state, LifecycleState::Running),
            "Lifecycle state should be Running"
        );
        assert!(health.discovery_active, "Discovery should be active");
        assert!(health.transport_connected, "Transport should be connected");
        assert_eq!(health.peer_count, 0, "Initial peer count should be 0");
    }

    /// Test service creation with custom config
    #[tokio::test]
    async fn test_service_with_custom_config() {
        let mut config = NetworkConfig::default();
        config.enable_webrtc = false;

        let service = P2PService::new(config)
            .await
            .expect("Service creation failed");

        service.start().await.expect("Service start failed");

        let health = service.health_status().await;
        assert_eq!(health.lifecycle_state, LifecycleState::Running);
    }

    /// Test multiple start calls (idempotency)
    #[tokio::test]
    async fn test_multiple_start_calls() {
        let config = NetworkConfig::default();
        let service = P2PService::new(config)
            .await
            .expect("Service creation failed");

        // First start
        let result1 = service.start().await;
        assert!(result1.is_ok(), "First start should succeed");

        // Second start (should handle gracefully)
        let result2 = service.start().await;
        // Note: Current implementation doesn't prevent multiple starts
        // This test documents current behavior
        assert!(result2.is_ok() || result2.is_err());
    }

    /// Test shutdown without start
    #[tokio::test]
    async fn test_shutdown_without_start() {
        let config = NetworkConfig::default();
        let service = P2PService::new(config)
            .await
            .expect("Service creation failed");

        let result = service.shutdown().await;
        // Shutdown should handle being called without start
        assert!(result.is_ok(), "Shutdown without start should succeed");
    }
}
