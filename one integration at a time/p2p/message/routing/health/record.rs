use std::time::Instant;

/// Health record for a transport
#[derive(Debug, Clone)]
pub(super) struct HealthRecord {
    pub success_count: u32,
    pub failure_count: u32,
    pub last_success: Option<Instant>,
    pub last_failure: Option<Instant>,
    pub avg_latency_ms: Option<u64>,
    pub is_healthy: bool,
}

impl HealthRecord {
    pub fn new() -> Self {
        Self {
            success_count: 0,
            failure_count: 0,
            last_success: None,
            last_failure: None,
            avg_latency_ms: None,
            is_healthy: true,
        }
    }

    pub fn update_latency(&mut self, latency_ms: u64) {
        self.avg_latency_ms = Some(match self.avg_latency_ms {
            Some(avg) => (avg + latency_ms) / 2,
            None => latency_ms,
        });
    }

    pub fn update_health_status(&mut self, success_threshold: u32, failure_threshold: u32) {
        let total = self.success_count + self.failure_count;
        if total >= success_threshold {
            let success_rate = (self.success_count as f64) / (total as f64);
            self.is_healthy = success_rate >= 0.7; // 70% success rate threshold
        } else if self.failure_count >= failure_threshold {
            self.is_healthy = false;
        }
    }

    pub fn calculate_success_rate(&self) -> f64 {
        let total = self.success_count + self.failure_count;
        if total == 0 {
            1.0
        } else {
            (self.success_count as f64) / (total as f64)
        }
    }

    pub fn last_activity(&self) -> Option<Instant> {
        match (self.last_success, self.last_failure) {
            (Some(s), Some(f)) => Some(s.max(f)),
            (Some(s), None) => Some(s),
            (None, Some(f)) => Some(f),
            (None, None) => None,
        }
    }
}
