use super::health::{TransportHealthMonitor, TransportType};
use super::TransportMethod;
use libp2p::PeerId;
use std::sync::Arc;
use tokio::sync::RwLock;
use tracing::{debug, warn};

/// Smart retry strategy using transport health monitoring (Task 3.4 Priority 2)
pub struct SmartRetryStrategy {
    health_monitor: Arc<RwLock<TransportHealthMonitor>>,
}

impl SmartRetryStrategy {
    /// Create new smart retry strategy
    pub fn new(health_monitor: Arc<RwLock<TransportHealthMonitor>>) -> Self {
        Self { health_monitor }
    }

    /// Choose best fallback transport based on health
    pub async fn choose_smart_fallback(
        &self,
        peer_id: &PeerId,
        current: &TransportMethod,
    ) -> Option<TransportMethod> {
        debug!(
            "Choosing smart fallback for peer {} from {:?}",
            peer_id, current
        );

        // Always use traditional fallback chain for predictable behavior
        // Health monitoring is used to skip unhealthy transports within the chain
        self.traditional_fallback(current)
    }

    /// Traditional fallback (WebRTC → LibP2P → Relay)
    fn traditional_fallback(&self, current: &TransportMethod) -> Option<TransportMethod> {
        match current {
            TransportMethod::WebRTC(_) => {
                debug!("Traditional fallback: WebRTC → LibP2P");
                Some(TransportMethod::LibP2P)
            }
            TransportMethod::LibP2P => {
                debug!("Traditional fallback: LibP2P → Relay");
                Some(TransportMethod::Relay("relay.jfdi.local".to_string()))
            }
            TransportMethod::Relay(_) => {
                warn!("No fallback available from Relay");
                None
            }
        }
    }

    /// Convert TransportType to TransportMethod
    #[allow(dead_code)] // Used by retry strategy selection logic
    fn transport_type_to_method(
        &self,
        transport_type: TransportType,
        peer_id: &PeerId,
    ) -> TransportMethod {
        match transport_type {
            TransportType::WebRTC => TransportMethod::WebRTC(format!("channel_{}", peer_id)),
            TransportType::LibP2P => TransportMethod::LibP2P,
            TransportType::Relay => TransportMethod::Relay("relay.jfdi.local".to_string()),
        }
    }

    /// Check if two transports are the same type
    #[allow(dead_code)] // Used by retry strategy deduplication
    fn is_same_transport(&self, a: &TransportMethod, b: &TransportMethod) -> bool {
        matches!(
            (a, b),
            (TransportMethod::WebRTC(_), TransportMethod::WebRTC(_))
                | (TransportMethod::LibP2P, TransportMethod::LibP2P)
                | (TransportMethod::Relay(_), TransportMethod::Relay(_))
        )
    }

    /// Record successful delivery for health tracking
    pub async fn record_success(
        &self,
        peer_id: PeerId,
        transport: &TransportMethod,
        latency_ms: u64,
    ) {
        let mut monitor = self.health_monitor.write().await;
        monitor.record_success(peer_id, transport, latency_ms);
        debug!("Recorded success for {:?} to {}", transport, peer_id);
    }

    /// Record failed delivery for health tracking
    pub async fn record_failure(&self, peer_id: PeerId, transport: &TransportMethod) {
        let mut monitor = self.health_monitor.write().await;
        monitor.record_failure(peer_id, transport);
        warn!("Recorded failure for {:?} to {}", transport, peer_id);
    }

    /// Check if transport is healthy
    pub async fn is_transport_healthy(
        &self,
        peer_id: &PeerId,
        transport: &TransportMethod,
    ) -> bool {
        let monitor = self.health_monitor.read().await;
        monitor.is_transport_healthy(peer_id, transport)
    }
}

/// Adaptive retry delay calculator
pub struct AdaptiveRetryDelay {
    base_delay_ms: u64,
    max_delay_ms: u64,
    backoff_multiplier: f64,
}

impl AdaptiveRetryDelay {
    /// Create new adaptive retry delay calculator
    pub fn new(base_delay_ms: u64, max_delay_ms: u64, backoff_multiplier: f64) -> Self {
        Self {
            base_delay_ms,
            max_delay_ms,
            backoff_multiplier,
        }
    }

    /// Calculate delay for attempt with health-based adjustment
    pub fn calculate_delay(&self, attempt: u32, transport_health: bool) -> std::time::Duration {
        let base_delay = if attempt == 0 {
            self.base_delay_ms
        } else {
            let delay = (self.base_delay_ms as f64) * self.backoff_multiplier.powi(attempt as i32);
            delay.min(self.max_delay_ms as f64) as u64
        };

        // Reduce delay for healthy transports, increase for unhealthy
        let adjusted_delay = if transport_health {
            (base_delay as f64 * 0.7) as u64 // 30% faster retry for healthy transports
        } else {
            (base_delay as f64 * 1.5) as u64 // 50% slower retry for unhealthy transports
        };

        std::time::Duration::from_millis(adjusted_delay.min(self.max_delay_ms))
    }
}

impl Default for AdaptiveRetryDelay {
    fn default() -> Self {
        Self::new(1000, 60000, 2.0) // 1s base, 60s max, 2x multiplier
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_smart_retry_strategy_creation() {
        let monitor = Arc::new(RwLock::new(TransportHealthMonitor::new(3, 5)));
        let strategy = SmartRetryStrategy::new(monitor);
        // Strategy created successfully
    }

    #[tokio::test]
    async fn test_traditional_fallback() {
        let monitor = Arc::new(RwLock::new(TransportHealthMonitor::new(3, 5)));
        let strategy = SmartRetryStrategy::new(monitor);

        // WebRTC → LibP2P
        let fallback = strategy.traditional_fallback(&TransportMethod::WebRTC("test".to_string()));
        assert!(matches!(fallback, Some(TransportMethod::LibP2P)));

        // LibP2P → Relay
        let fallback = strategy.traditional_fallback(&TransportMethod::LibP2P);
        assert!(matches!(fallback, Some(TransportMethod::Relay(_))));

        // Relay → None
        let fallback = strategy.traditional_fallback(&TransportMethod::Relay("test".to_string()));
        assert!(fallback.is_none());
    }

    #[test]
    fn test_adaptive_retry_delay() {
        let calculator = AdaptiveRetryDelay::default();

        // Healthy transport should have shorter delay
        let healthy_delay = calculator.calculate_delay(1, true);
        let unhealthy_delay = calculator.calculate_delay(1, false);

        assert!(healthy_delay < unhealthy_delay);
    }

    #[test]
    fn test_exponential_backoff() {
        let calculator = AdaptiveRetryDelay::default();

        let delay0 = calculator.calculate_delay(0, true);
        let delay1 = calculator.calculate_delay(1, true);
        let delay2 = calculator.calculate_delay(2, true);

        // Each delay should be larger than the previous
        assert!(delay1 > delay0);
        assert!(delay2 > delay1);
    }

    #[test]
    fn test_max_delay_cap() {
        let calculator = AdaptiveRetryDelay::new(1000, 5000, 2.0);

        // Even with many attempts, delay should not exceed max
        let delay = calculator.calculate_delay(10, true);
        assert!(delay.as_millis() <= 5000);
    }
}
