// Recovery Retry Logic
// Pattern Bible Compliance: File ≤200 lines, Functions ≤30 lines
// Solves: Retry logic and backoff calculations separated from core recovery

use std::time::Duration;
use tracing::debug;

/// Calculate exponential backoff duration
pub fn calculate_backoff(retry_count: u32) -> Duration {
    let base_delay = 2u64; // 2 seconds
    let max_delay = 60u64; // 60 seconds

    let delay = base_delay.saturating_pow(retry_count).min(max_delay);
    Duration::from_secs(delay)
}

/// Apply exponential backoff with logging
pub async fn apply_backoff(retry_count: u32) {
    let backoff_duration = calculate_backoff(retry_count);
    debug!(
        "Waiting {} seconds before recovery attempt",
        backoff_duration.as_secs()
    );
    tokio::time::sleep(backoff_duration).await;
}

/// Check if max retries exceeded
pub fn is_max_retries_exceeded(retry_count: u32, max_retries: u32) -> bool {
    retry_count >= max_retries
}
