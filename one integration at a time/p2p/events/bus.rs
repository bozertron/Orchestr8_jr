use anyhow::Result;
use std::sync::Arc;
use tokio::sync::{broadcast, RwLock};
use tracing::{debug, info};

use super::{handlers::EventHandlerRegistry, subscriptions::SubscriptionManager, P2PEventType};

/// Event bus for P2P service events
pub struct EventBus {
    sender: broadcast::Sender<P2PEventType>,
    subscriber_count: Arc<RwLock<usize>>,
    handler_registry: Arc<EventHandlerRegistry>,
    subscription_manager: Arc<SubscriptionManager>,
}

impl EventBus {
    /// Create new event bus
    pub fn new() -> Self {
        let (sender, _receiver) = broadcast::channel(1000);
        let handler_registry = Arc::new(EventHandlerRegistry::new());
        let subscription_manager = Arc::new(SubscriptionManager::new());

        // Start automatic cleanup task
        Arc::clone(&subscription_manager).start_cleanup_task();

        Self {
            sender,
            subscriber_count: Arc::new(RwLock::new(0)),
            handler_registry,
            subscription_manager,
        }
    }

    /// Publish event to all subscribers
    pub async fn publish(&self, event: P2PEventType) -> Result<()> {
        debug!("Publishing event: {:?}", event);

        // Dispatch to registered handlers
        self.handler_registry.dispatch_event(event.clone()).await?;

        // Send event to all subscribers
        let _ = self.sender.send(event);

        Ok(())
    }

    /// Subscribe to events
    pub async fn subscribe(&self) -> broadcast::Receiver<P2PEventType> {
        let mut count = self.subscriber_count.write().await;
        *count += 1;

        info!("New subscriber registered (total: {})", *count);

        let receiver = self.sender.subscribe();

        // Register subscription with manager
        let event_types = vec!["all".to_string()];
        if let Err(e) = self
            .subscription_manager
            .create_subscription(event_types, self.sender.subscribe())
            .await
        {
            debug!("Failed to register subscription: {}", e);
        }

        receiver
    }

    /// Get subscriber count
    pub async fn subscriber_count(&self) -> usize {
        *self.subscriber_count.read().await
    }

    /// Shutdown event bus
    pub async fn shutdown(&self) -> Result<()> {
        info!("Shutting down event bus");

        // Clear all handlers
        self.handler_registry.clear_handlers().await?;

        // Cleanup subscriptions
        self.subscription_manager
            .cleanup_stale_subscriptions()
            .await?;

        Ok(())
    }

    /// Get handler registry
    pub fn handler_registry(&self) -> Arc<EventHandlerRegistry> {
        Arc::clone(&self.handler_registry)
    }

    /// Get subscription manager
    pub fn subscription_manager(&self) -> Arc<SubscriptionManager> {
        Arc::clone(&self.subscription_manager)
    }
}

impl Default for EventBus {
    fn default() -> Self {
        Self::new()
    }
}

impl Clone for EventBus {
    fn clone(&self) -> Self {
        Self {
            sender: self.sender.clone(),
            subscriber_count: Arc::clone(&self.subscriber_count),
            handler_registry: Arc::clone(&self.handler_registry),
            subscription_manager: Arc::clone(&self.subscription_manager),
        }
    }
}
