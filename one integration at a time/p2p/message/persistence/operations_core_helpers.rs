/// Operations statistics
#[derive(Debug, Clone)]
pub struct OperationsStats {
    pub total_messages: u64,
    pub pending_deliveries: u64,
    pub last_operation: i64,
}

impl OperationsStats {
    /// Check if operations are healthy
    pub fn is_healthy(&self) -> bool {
        // Consider healthy if pending deliveries are less than 10% of total
        if self.total_messages == 0 {
            true
        } else {
            let pending_ratio = self.pending_deliveries as f64 / self.total_messages as f64;
            pending_ratio < 0.1
        }
    }

    /// Get delivery success rate
    pub fn delivery_success_rate(&self) -> f64 {
        if self.total_messages == 0 {
            100.0
        } else {
            let successful = self.total_messages - self.pending_deliveries;
            (successful as f64 / self.total_messages as f64) * 100.0
        }
    }
}
