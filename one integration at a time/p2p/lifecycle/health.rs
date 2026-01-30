use crate::p2p::{
    discovery::Discovery, manager::PeerManager, message::MessageService, service::LifecycleState,
    transport::P2PTransport, webrtc::WebRtcService,
};
use anyhow::Result;
use std::sync::Arc;
use tokio::sync::RwLock;
use tracing::{debug, warn};

/// Component health status
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ComponentHealth {
    Healthy,
    Degraded,
    Failed,
    Unknown,
}

/// Health monitor for P2P service components
pub struct HealthMonitor {
    discovery: Arc<RwLock<Discovery>>,
    transport: Arc<RwLock<P2PTransport>>,
    webrtc: Arc<RwLock<Option<WebRtcService>>>,
    peer_manager: Arc<RwLock<PeerManager>>,
    message_service: Arc<RwLock<Option<MessageService>>>,
    lifecycle_state: Arc<RwLock<LifecycleState>>,
}

impl HealthMonitor {
    /// Create new health monitor
    pub fn new(
        discovery: Arc<RwLock<Discovery>>,
        transport: Arc<RwLock<P2PTransport>>,
        webrtc: Arc<RwLock<Option<WebRtcService>>>,
        peer_manager: Arc<RwLock<PeerManager>>,
        message_service: Arc<RwLock<Option<MessageService>>>,
        lifecycle_state: Arc<RwLock<LifecycleState>>,
    ) -> Self {
        Self {
            discovery,
            transport,
            webrtc,
            peer_manager,
            message_service,
            lifecycle_state,
        }
    }

    /// Check health of all components
    pub async fn check_component_health(&self) -> Result<ComponentHealthReport> {
        debug!("Checking component health");
        let discovery_health = self.check_discovery_health().await;
        let transport_health = self.check_transport_health().await;
        let webrtc_health = self.check_webrtc_health().await;
        let peer_manager_health = self.check_peer_manager_health().await;
        let message_service_health = self.check_message_service_health().await;

        let report = ComponentHealthReport {
            discovery: discovery_health,
            transport: transport_health,
            webrtc: webrtc_health,
            peer_manager: peer_manager_health,
            message_service: message_service_health,
        };
        debug!("Component health check complete: {:?}", report);
        Ok(report)
    }

    /// Detect failed components
    pub async fn detect_failures(&self) -> Result<Vec<String>> {
        let report = self.check_component_health().await?;
        let mut failures = Vec::new();
        if report.discovery == ComponentHealth::Failed {
            failures.push("discovery".to_string());
        }
        if report.transport == ComponentHealth::Failed {
            failures.push("transport".to_string());
        }
        if report.webrtc == ComponentHealth::Failed {
            failures.push("webrtc".to_string());
        }
        if report.peer_manager == ComponentHealth::Failed {
            failures.push("peer_manager".to_string());
        }
        if report.message_service == ComponentHealth::Failed {
            failures.push("message_service".to_string());
        }
        if !failures.is_empty() {
            warn!("Detected component failures: {:?}", failures);
        }
        Ok(failures)
    }

    /// Trigger recovery for failed components
    pub async fn trigger_recovery(&self, component: &str) -> Result<()> {
        warn!("Triggering recovery for component: {}", component);
        // Recovery will be handled by RecoveryCoordinator
        Ok(())
    }

    /// Update health metrics
    pub async fn update_health_metrics(&self) -> Result<()> {
        let report = self.check_component_health().await?;

        // Determine overall lifecycle state based on component health
        let new_state = self.determine_lifecycle_state(&report);

        let mut state = self.lifecycle_state.write().await;
        if *state != new_state {
            debug!("Lifecycle state changing: {:?} -> {:?}", *state, new_state);
            *state = new_state;
        }

        Ok(())
    }

    /// Check discovery service health
    async fn check_discovery_health(&self) -> ComponentHealth {
        // Use discovery field to check actual health
        let is_running = self.discovery.read().await.is_running();
        if is_running {
            ComponentHealth::Healthy
        } else {
            ComponentHealth::Degraded
        }
    }

    /// Check transport layer health
    async fn check_transport_health(&self) -> ComponentHealth {
        // Use transport field to check actual health
        let is_connected = self.transport.read().await.is_connected();
        if is_connected {
            ComponentHealth::Healthy
        } else {
            ComponentHealth::Degraded
        }
    }

    /// Check WebRTC service health
    async fn check_webrtc_health(&self) -> ComponentHealth {
        if self.webrtc.read().await.is_some() {
            ComponentHealth::Healthy
        } else {
            ComponentHealth::Unknown
        }
    }

    /// Check peer manager health
    async fn check_peer_manager_health(&self) -> ComponentHealth {
        let peer_count = self.peer_manager.read().await.peer_count().await;
        if peer_count > 0 {
            ComponentHealth::Healthy
        } else {
            ComponentHealth::Degraded
        }
    }

    /// Check message service health
    async fn check_message_service_health(&self) -> ComponentHealth {
        if self.message_service.read().await.is_some() {
            ComponentHealth::Healthy
        } else {
            ComponentHealth::Unknown
        }
    }

    /// Determine lifecycle state from component health
    fn determine_lifecycle_state(&self, report: &ComponentHealthReport) -> LifecycleState {
        let failed_count = [
            &report.discovery,
            &report.transport,
            &report.webrtc,
            &report.peer_manager,
            &report.message_service,
        ]
        .iter()
        .filter(|&&h| *h == ComponentHealth::Failed)
        .count();

        if failed_count > 0 {
            LifecycleState::Degraded
        } else {
            LifecycleState::Running
        }
    }
}

/// Component health report
#[derive(Debug, Clone)]
pub struct ComponentHealthReport {
    pub discovery: ComponentHealth,
    pub transport: ComponentHealth,
    pub webrtc: ComponentHealth,
    pub peer_manager: ComponentHealth,
    pub message_service: ComponentHealth,
}
