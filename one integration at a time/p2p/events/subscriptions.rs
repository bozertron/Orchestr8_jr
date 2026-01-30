use super::P2PEventType;
use anyhow::Result;
use std::collections::HashMap;
use std::sync::Arc;
use std::time::{Duration, Instant};
use tokio::sync::{broadcast, RwLock};
use tracing::{debug, info, warn};
use uuid::Uuid;

/// Subscription information
#[derive(Debug, Clone)]
pub struct Subscription {
    pub id: String,
    pub event_types: Vec<String>,
    pub created_at: Instant,
    pub last_activity: Instant,
}

impl Subscription {
    /// Create new subscription
    pub fn new(event_types: Vec<String>) -> Self {
        let now = Instant::now();
        Self {
            id: Uuid::new_v4().to_string(),
            event_types,
            created_at: now,
            last_activity: now,
        }
    }

    /// Update last activity timestamp
    pub fn update_activity(&mut self) {
        self.last_activity = Instant::now();
    }

    /// Check if subscription is stale
    pub fn is_stale(&self, timeout: Duration) -> bool {
        self.last_activity.elapsed() > timeout
    }
}

/// Subscription manager for managing event subscriptions
pub struct SubscriptionManager {
    subscriptions: Arc<RwLock<HashMap<String, Subscription>>>,
    receivers: Arc<RwLock<HashMap<String, broadcast::Receiver<P2PEventType>>>>,
    stale_timeout: Duration,
}

impl SubscriptionManager {
    /// Create new subscription manager
    pub fn new() -> Self {
        Self {
            subscriptions: Arc::new(RwLock::new(HashMap::new())),
            receivers: Arc::new(RwLock::new(HashMap::new())),
            stale_timeout: Duration::from_secs(300), // 5 minutes
        }
    }

    /// Create new subscription
    pub async fn create_subscription(
        &self,
        event_types: Vec<String>,
        receiver: broadcast::Receiver<P2PEventType>,
    ) -> Result<String> {
        let subscription = Subscription::new(event_types.clone());
        let subscription_id = subscription.id.clone();

        info!(
            "Creating subscription {} for event types: {:?}",
            subscription_id, event_types
        );

        // Store subscription
        self.subscriptions
            .write()
            .await
            .insert(subscription_id.clone(), subscription);

        // Store receiver
        self.receivers
            .write()
            .await
            .insert(subscription_id.clone(), receiver);

        debug!("Subscription created: {}", subscription_id);
        Ok(subscription_id)
    }

    /// Cancel subscription
    pub async fn cancel_subscription(&self, subscription_id: &str) -> Result<()> {
        info!("Cancelling subscription: {}", subscription_id);

        // Remove subscription
        self.subscriptions.write().await.remove(subscription_id);

        // Remove receiver
        self.receivers.write().await.remove(subscription_id);

        debug!("Subscription cancelled: {}", subscription_id);
        Ok(())
    }

    /// List all active subscriptions
    pub async fn list_subscriptions(&self) -> Vec<Subscription> {
        let subscriptions = self.subscriptions.read().await;
        subscriptions.values().cloned().collect()
    }

    /// Cleanup stale subscriptions
    pub async fn cleanup_stale_subscriptions(&self) -> Result<usize> {
        debug!("Cleaning up stale subscriptions");

        let mut subscriptions = self.subscriptions.write().await;
        let mut receivers = self.receivers.write().await;

        let stale_ids: Vec<String> = subscriptions
            .iter()
            .filter(|(_, sub)| sub.is_stale(self.stale_timeout))
            .map(|(id, _)| id.clone())
            .collect();

        let count = stale_ids.len();

        if count > 0 {
            warn!("Found {} stale subscriptions", count);

            for id in stale_ids {
                subscriptions.remove(&id);
                receivers.remove(&id);
                debug!("Removed stale subscription: {}", id);
            }
        }

        Ok(count)
    }

    /// Update subscription activity
    pub async fn update_subscription_activity(&self, subscription_id: &str) -> Result<()> {
        let mut subscriptions = self.subscriptions.write().await;

        if let Some(subscription) = subscriptions.get_mut(subscription_id) {
            subscription.update_activity();
            debug!("Updated activity for subscription: {}", subscription_id);
        }

        Ok(())
    }

    /// Get subscription count
    pub async fn subscription_count(&self) -> usize {
        self.subscriptions.read().await.len()
    }

    /// Get subscription by ID
    pub async fn get_subscription(&self, subscription_id: &str) -> Option<Subscription> {
        self.subscriptions
            .read()
            .await
            .get(subscription_id)
            .cloned()
    }

    /// Set stale timeout
    pub fn set_stale_timeout(&mut self, timeout: Duration) {
        self.stale_timeout = timeout;
    }

    /// Start automatic cleanup task
    pub fn start_cleanup_task(self: Arc<Self>) {
        tokio::spawn(async move {
            let mut interval = tokio::time::interval(Duration::from_secs(60));

            loop {
                interval.tick().await;

                if let Err(e) = self.cleanup_stale_subscriptions().await {
                    warn!("Error during subscription cleanup: {}", e);
                }
            }
        });
    }
}

impl Default for SubscriptionManager {
    fn default() -> Self {
        Self::new()
    }
}
