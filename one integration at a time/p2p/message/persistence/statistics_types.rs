/// Event statistics for monitoring
#[derive(Debug, Clone)]
pub struct EventStatistics {
    pub total_events: u64,
    pub unprocessed_events: u64,
    pub events_last_hour: u64,
}

impl EventStatistics {
    /// Create new event statistics
    pub fn new(total_events: u64, unprocessed_events: u64, events_last_hour: u64) -> Self {
        Self {
            total_events,
            unprocessed_events,
            events_last_hour,
        }
    }

    /// Get processing rate as percentage
    pub fn processing_rate(&self) -> f64 {
        if self.total_events == 0 {
            100.0
        } else {
            ((self.total_events - self.unprocessed_events) as f64 / self.total_events as f64)
                * 100.0
        }
    }

    /// Check if system is healthy (low unprocessed events)
    pub fn is_healthy(&self) -> bool {
        if self.total_events == 0 {
            true
        } else {
            let unprocessed_ratio = self.unprocessed_events as f64 / self.total_events as f64;
            unprocessed_ratio < 0.1 // Less than 10% unprocessed
        }
    }

    /// Get events per hour rate
    pub fn events_per_hour(&self) -> u64 {
        self.events_last_hour
    }

    /// Check if there's a backlog of unprocessed events
    pub fn has_backlog(&self) -> bool {
        self.unprocessed_events > 100 // More than 100 unprocessed events
    }

    /// Get backlog severity (0-3: none, low, medium, high)
    pub fn backlog_severity(&self) -> u8 {
        if self.unprocessed_events == 0 {
            0 // No backlog
        } else if self.unprocessed_events < 50 {
            1 // Low backlog
        } else if self.unprocessed_events < 200 {
            2 // Medium backlog
        } else {
            3 // High backlog
        }
    }
}

/// Processing performance metrics
#[derive(Debug, Clone)]
pub struct ProcessingMetrics {
    pub avg_processing_time_seconds: f64,
    pub oldest_unprocessed_timestamp: Option<i64>,
}

/// Event processing statistics for maintenance operations
#[derive(Debug, Clone)]
pub struct EventProcessingStats {
    pub total_events: u64,
    pub processed_events: u64,
    pub unprocessed_events: u64,
    pub average_processing_time: f64,
}

impl ProcessingMetrics {
    /// Create new processing metrics
    pub fn new(
        avg_processing_time_seconds: f64,
        oldest_unprocessed_timestamp: Option<i64>,
    ) -> Self {
        Self {
            avg_processing_time_seconds,
            oldest_unprocessed_timestamp,
        }
    }

    /// Check if processing is within acceptable time limits
    pub fn is_processing_healthy(&self) -> bool {
        // Consider healthy if average processing time is under 5 seconds
        self.avg_processing_time_seconds < 5.0
    }

    /// Get age of oldest unprocessed event in seconds
    pub fn oldest_unprocessed_age_seconds(&self) -> Option<i64> {
        self.oldest_unprocessed_timestamp
            .map(|timestamp| chrono::Utc::now().timestamp() - timestamp)
    }

    /// Check if there are stale unprocessed events (older than 1 hour)
    pub fn has_stale_events(&self) -> bool {
        self.oldest_unprocessed_age_seconds()
            .map_or(false, |age| age > 3600)
    }

    /// Get processing throughput estimate (events per second)
    pub fn estimated_throughput(&self) -> f64 {
        if self.avg_processing_time_seconds > 0.0 {
            1.0 / self.avg_processing_time_seconds
        } else {
            0.0
        }
    }

    /// Get performance grade (A-F based on processing time)
    pub fn performance_grade(&self) -> char {
        if self.avg_processing_time_seconds < 1.0 {
            'A'
        } else if self.avg_processing_time_seconds < 2.0 {
            'B'
        } else if self.avg_processing_time_seconds < 5.0 {
            'C'
        } else if self.avg_processing_time_seconds < 10.0 {
            'D'
        } else {
            'F'
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_event_statistics_creation() {
        let stats = EventStatistics::new(100, 10, 25);

        assert_eq!(stats.total_events, 100);
        assert_eq!(stats.unprocessed_events, 10);
        assert_eq!(stats.events_last_hour, 25);
        assert_eq!(stats.processing_rate(), 90.0);
        assert!(stats.is_healthy());
        assert!(!stats.has_backlog());
        assert_eq!(stats.backlog_severity(), 1); // Low backlog
    }

    #[test]
    fn test_event_statistics_backlog() {
        let stats_high_backlog = EventStatistics::new(1000, 300, 50);

        assert!(stats_high_backlog.has_backlog());
        assert_eq!(stats_high_backlog.backlog_severity(), 3); // High backlog
        assert!(!stats_high_backlog.is_healthy());
    }

    #[test]
    fn test_processing_metrics_creation() {
        let metrics = ProcessingMetrics::new(2.5, Some(chrono::Utc::now().timestamp() - 100));

        assert!(metrics.is_processing_healthy());
        assert!(metrics.oldest_unprocessed_age_seconds().unwrap() >= 100);
        assert!(!metrics.has_stale_events());
        assert_eq!(metrics.performance_grade(), 'C');
        assert!(metrics.estimated_throughput() > 0.0);
    }

    #[test]
    fn test_processing_metrics_stale_events() {
        let old_timestamp = chrono::Utc::now().timestamp() - 7200; // 2 hours ago
        let metrics = ProcessingMetrics::new(1.0, Some(old_timestamp));

        assert!(metrics.has_stale_events());
        assert_eq!(metrics.performance_grade(), 'A');
    }

    #[test]
    fn test_processing_metrics_performance_grades() {
        assert_eq!(ProcessingMetrics::new(0.5, None).performance_grade(), 'A');
        assert_eq!(ProcessingMetrics::new(1.5, None).performance_grade(), 'B');
        assert_eq!(ProcessingMetrics::new(3.0, None).performance_grade(), 'C');
        assert_eq!(ProcessingMetrics::new(7.0, None).performance_grade(), 'D');
        assert_eq!(ProcessingMetrics::new(15.0, None).performance_grade(), 'F');
    }
}
