use super::errors::RoutingError;
use super::{DeliveryStatus, TransportMethod};
use crate::p2p::message::types::{EncryptedMessage, MessageId};

use super::delivery::DeliveryTracker;
use super::transport::TransportManager;
use libp2p::PeerId;
use std::sync::Arc;
use std::time::Duration;
use tokio::sync::RwLock;
use tokio::time::sleep;
#[derive(Debug, Clone)]
pub struct RetryConfig {
    pub max_attempts: u32,
    pub initial_delay: Duration,
    pub max_delay: Duration,
    pub backoff_multiplier: f64,
}

impl Default for RetryConfig {
    fn default() -> Self {
        Self {
            max_attempts: 3,
            initial_delay: Duration::from_secs(5),
            max_delay: Duration::from_secs(60),
            backoff_multiplier: 2.0,
        }
    }
}
pub struct RetryManager {
    config: RetryConfig,
}

impl RetryManager {
    pub fn new(config: RetryConfig) -> Self {
        Self { config }
    }

    pub fn calculate_delay(&self, attempt: u32) -> Duration {
        if attempt == 0 {
            return self.config.initial_delay;
        }

        let delay_secs = self.config.initial_delay.as_secs_f64()
            * self.config.backoff_multiplier.powi(attempt as i32 - 1);

        let delay = Duration::from_secs_f64(delay_secs.min(self.config.max_delay.as_secs_f64()));
        delay
    }

    pub fn should_retry(&self, attempt: u32, error: &RoutingError) -> bool {
        if attempt >= self.config.max_attempts {
            return false;
        }

        // Determine if error is retryable
        match error {
            RoutingError::NoTransportAvailable(_) => true,
            RoutingError::DeliveryTimeout(_) => true,
            RoutingError::TransportError(_) => true,
            RoutingError::PeerNotConnected(_) => true,
            RoutingError::MessageTooLarge(_) => false, // Not retryable
            RoutingError::RetryLimitExceeded(_) => false, // Not retryable
            RoutingError::InvalidMessage(_) => false,  // Not retryable
        }
    }

    async fn should_continue_retry(&self, attempt: u32, last_error: &Option<String>) -> bool {
        // Check if we should retry
        if let Some(routing_error) = self.extract_routing_error(last_error) {
            if !self.should_retry(attempt + 1, &routing_error) {
                return false;
            }
        }

        // Wait before retry (except for last attempt)
        if attempt + 1 < self.config.max_attempts {
            let delay = self.calculate_delay(attempt + 1);
            sleep(delay).await;
        }

        true
    }

    fn extract_routing_error(&self, error: &Option<String>) -> Option<RoutingError> {
        // This is a simplified extraction - in practice, you might want
        // more sophisticated error type detection
        if let Some(msg) = error {
            if msg.contains("Connection") {
                if msg.contains("timeout") {
                    Some(RoutingError::DeliveryTimeout(Duration::from_secs(30)))
                } else if msg.contains("not connected") {
                    Some(RoutingError::PeerNotConnected(msg.clone()))
                } else if msg.contains("transport") {
                    Some(RoutingError::TransportError(msg.clone()))
                } else {
                    Some(RoutingError::TransportError(msg.clone()))
                }
            } else {
                Some(RoutingError::TransportError(msg.clone()))
            }
        } else {
            None
        }
    }

    fn choose_fallback(current: &TransportMethod) -> Option<TransportMethod> {
        match current {
            TransportMethod::WebRTC { .. } => Some(TransportMethod::LibP2P),
            TransportMethod::LibP2P => Some(TransportMethod::Relay(String::new())),
            TransportMethod::Relay(_) => None,
        }
    }
    async fn note_attempt(
        &self,
        delivery_tracker: &Arc<RwLock<DeliveryTracker>>,
        message_id: MessageId,
    ) {
        let dt = delivery_tracker.write().await;
        let _ = dt.increment_attempts(message_id);
    }
    async fn try_send(
        &self,
        transport_manager: &Arc<RwLock<TransportManager>>,
        to: PeerId,
        encrypted_message: &EncryptedMessage,
        transport: &TransportMethod,
    ) -> Result<(), String> {
        let tm = transport_manager.read().await;
        tm.send_message(to, encrypted_message.clone(), transport)
            .await
    }

    async fn mark_sent(
        &self,
        delivery_tracker: &Arc<RwLock<DeliveryTracker>>,
        message_id: MessageId,
    ) -> Result<(), String> {
        let dt = delivery_tracker.write().await;
        dt.update_status(message_id, DeliveryStatus::Sent).await
    }

    async fn mark_failed(
        &self,
        delivery_tracker: &Arc<RwLock<DeliveryTracker>>,
        message_id: MessageId,
        err_msg: String,
    ) {
        let dt = delivery_tracker.write().await;
        let _ = dt
            .update_status(message_id, DeliveryStatus::Failed(err_msg))
            .await;
    }
    async fn handle_send_result(
        &self,
        delivery_tracker: &Arc<RwLock<DeliveryTracker>>,
        message_id: MessageId,
        res: Result<(), String>,
    ) -> Result<(), String> {
        match res {
            Ok(()) => {
                self.mark_sent(delivery_tracker, message_id)
                    .await
                    .map_err(|e| e.to_string())?;
                Ok(())
            }
            Err(e) => Err(e),
        }
    }
    pub async fn execute_with_retry_ctx(
        &self,
        transport_manager: Arc<RwLock<TransportManager>>,
        delivery_tracker: Arc<RwLock<DeliveryTracker>>,
        to: PeerId,
        message_id: MessageId,
        encrypted_message: EncryptedMessage,
        mut transport: TransportMethod,
    ) -> Result<(), String> {
        let mut last_error: Option<String> = None;
        for attempt in 0..self.config.max_attempts {
            self.note_attempt(&delivery_tracker, message_id).await;
            let res = self
                .try_send(&transport_manager, to, &encrypted_message, &transport)
                .await;
            match self
                .handle_send_result(&delivery_tracker, message_id, res)
                .await
            {
                Ok(()) => return Ok(()),
                Err(e) => {
                    last_error = Some(e);
                    if !self.should_continue_retry(attempt, &last_error).await {
                        break;
                    }
                    if let Some(next) = Self::choose_fallback(&transport) {
                        transport = next;
                    }
                }
            }
        }

        let err = last_error.unwrap_or_else(|| {
            format!(
                "Retry limit exceeded: {} attempts",
                self.config.max_attempts
            )
        });
        self.mark_failed(&delivery_tracker, message_id, err.clone())
            .await;
        Err(err)
    }
}
