mod record;

use super::TransportMethod;
use libp2p::PeerId;
use record::HealthRecord;
use std::collections::HashMap;
use std::time::{Duration, Instant};

/// Transport health monitoring for smart fallback decisions (Task 3.4 Priority 2)
pub struct TransportHealthMonitor {
    health_records: HashMap<(PeerId, TransportType), HealthRecord>,
    failure_threshold: u32,
    success_threshold: u32,
}

/// Transport type for health tracking
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum TransportType {
    WebRTC,
    LibP2P,
    Relay,
}

impl TransportHealthMonitor {
    /// Create new transport health monitor
    pub fn new(failure_threshold: u32, success_threshold: u32) -> Self {
        Self {
            health_records: HashMap::new(),
            failure_threshold,
            success_threshold,
        }
    }

    /// Record successful delivery
    pub fn record_success(
        &mut self,
        peer_id: PeerId,
        transport: &TransportMethod,
        latency_ms: u64,
    ) {
        let transport_type = Self::get_transport_type(transport);
        let key = (peer_id, transport_type);

        let record = self
            .health_records
            .entry(key)
            .or_insert_with(HealthRecord::new);
        record.success_count += 1;
        record.last_success = Some(Instant::now());
        record.update_latency(latency_ms);
        record.update_health_status(self.success_threshold, self.failure_threshold);
    }

    /// Record failed delivery
    pub fn record_failure(&mut self, peer_id: PeerId, transport: &TransportMethod) {
        let transport_type = Self::get_transport_type(transport);
        let key = (peer_id, transport_type);

        let record = self
            .health_records
            .entry(key)
            .or_insert_with(HealthRecord::new);
        record.failure_count += 1;
        record.last_failure = Some(Instant::now());
        record.update_health_status(self.success_threshold, self.failure_threshold);
    }

    /// Check if transport is healthy for peer
    pub fn is_transport_healthy(&self, peer_id: &PeerId, transport: &TransportMethod) -> bool {
        let transport_type = Self::get_transport_type(transport);
        let key = (*peer_id, transport_type);

        self.health_records
            .get(&key)
            .map(|record| record.is_healthy)
            .unwrap_or(true) // Assume healthy if no history
    }

    /// Get best available transport for peer
    pub fn get_best_transport(&self, peer_id: &PeerId) -> Option<TransportType> {
        let transports = [
            TransportType::WebRTC,
            TransportType::LibP2P,
            TransportType::Relay,
        ];

        transports
            .iter()
            .find(|&&transport_type| {
                let key = (*peer_id, transport_type);
                self.health_records
                    .get(&key)
                    .map(|record| record.is_healthy)
                    .unwrap_or(true)
            })
            .copied()
    }

    /// Get transport statistics
    pub fn get_stats(
        &self,
        peer_id: &PeerId,
        transport: &TransportMethod,
    ) -> Option<TransportStats> {
        let transport_type = Self::get_transport_type(transport);
        let key = (*peer_id, transport_type);

        self.health_records.get(&key).map(|record| TransportStats {
            success_count: record.success_count,
            failure_count: record.failure_count,
            success_rate: record.calculate_success_rate(),
            avg_latency_ms: record.avg_latency_ms,
            is_healthy: record.is_healthy,
        })
    }

    /// Clear old records (call periodically)
    pub fn cleanup_old_records(&mut self, max_age: Duration) {
        let now = Instant::now();
        self.health_records.retain(|_, record| {
            if let Some(last_activity) = record.last_activity() {
                now.duration_since(last_activity) < max_age
            } else {
                false
            }
        });
    }

    /// Get transport type from TransportMethod
    fn get_transport_type(transport: &TransportMethod) -> TransportType {
        match transport {
            TransportMethod::WebRTC(_) => TransportType::WebRTC,
            TransportMethod::LibP2P => TransportType::LibP2P,
            TransportMethod::Relay(_) => TransportType::Relay,
        }
    }
}

/// Transport statistics
#[derive(Debug, Clone)]
pub struct TransportStats {
    pub success_count: u32,
    pub failure_count: u32,
    pub success_rate: f64,
    pub avg_latency_ms: Option<u64>,
    pub is_healthy: bool,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_health_monitor_creation() {
        let monitor = TransportHealthMonitor::new(3, 5);
        assert_eq!(monitor.failure_threshold, 3);
        assert_eq!(monitor.success_threshold, 5);
    }

    #[test]
    fn test_record_success() {
        let mut monitor = TransportHealthMonitor::new(3, 5);
        let peer_id = PeerId::random();
        let transport = TransportMethod::LibP2P;

        monitor.record_success(peer_id, &transport, 50);

        let stats = monitor.get_stats(&peer_id, &transport).unwrap();
        assert_eq!(stats.success_count, 1);
        assert_eq!(stats.failure_count, 0);
        assert!(stats.is_healthy);
    }

    #[test]
    fn test_record_failure() {
        let mut monitor = TransportHealthMonitor::new(3, 5);
        let peer_id = PeerId::random();
        let transport = TransportMethod::LibP2P;

        // Record multiple failures
        for _ in 0..3 {
            monitor.record_failure(peer_id, &transport);
        }

        let stats = monitor.get_stats(&peer_id, &transport).unwrap();
        assert_eq!(stats.failure_count, 3);
        assert!(!stats.is_healthy); // Should be unhealthy after threshold
    }

    #[test]
    fn test_get_best_transport() {
        let mut monitor = TransportHealthMonitor::new(3, 5);
        let peer_id = PeerId::random();

        // Mark WebRTC as unhealthy
        for _ in 0..3 {
            monitor.record_failure(peer_id, &TransportMethod::WebRTC("test".to_string()));
        }

        // Best transport should be LibP2P (next in priority)
        let best = monitor.get_best_transport(&peer_id);
        assert_eq!(best, Some(TransportType::LibP2P));
    }
}
