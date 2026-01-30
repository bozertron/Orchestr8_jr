pub mod events;
pub mod handlers;
pub mod stats;

pub use events::DataChannelEvent;
pub use stats::DataChannelStats;

use super::config::WebRtcConfig;
use libp2p::PeerId;
use std::sync::Arc;
use tokio::sync::{mpsc, RwLock};

use webrtc::data_channel::RTCDataChannel;
use webrtc::peer_connection::RTCPeerConnection;

/// Data channel states
#[derive(Debug, Clone, PartialEq)]
pub enum DataChannelState {
    Connecting,
    Open,
    Closing,
    Closed,
}

/// WebRTC data channel wrapper
pub struct DataChannel {
    label: String,
    peer_id: PeerId,
    channel: Arc<RTCDataChannel>,
    state: Arc<RwLock<DataChannelState>>,
    config: WebRtcConfig,
    event_sender: mpsc::UnboundedSender<super::WebRtcEvent>,
    bytes_sent: Arc<RwLock<u64>>,
    bytes_received: Arc<RwLock<u64>>,
}

impl DataChannel {
    /// Create new data channel
    pub async fn new(
        peer_connection: &Arc<RTCPeerConnection>,
        label: String,
        config: &WebRtcConfig,
        peer_id: PeerId,
        event_sender: mpsc::UnboundedSender<super::WebRtcEvent>,
    ) -> Result<Self, String> {
        let channel = Self::create_rtc_data_channel(peer_connection, &label, config).await?;

        let data_channel = Self {
            label: label.clone(),
            peer_id,
            channel,
            state: Arc::new(RwLock::new(DataChannelState::Connecting)),
            config: config.clone(),
            event_sender,
            bytes_sent: Arc::new(RwLock::new(0)),
            bytes_received: Arc::new(RwLock::new(0)),
        };

        data_channel.setup_event_handlers().await?;
        Ok(data_channel)
    }

    /// Create RTC data channel
    async fn create_rtc_data_channel(
        peer_connection: &Arc<RTCPeerConnection>,
        label: &str,
        config: &WebRtcConfig,
    ) -> Result<Arc<RTCDataChannel>, String> {
        use webrtc::data_channel::data_channel_init::RTCDataChannelInit;

        let data_channel_config = RTCDataChannelInit {
            ordered: Some(config.ordered_delivery),
            max_retransmits: config.max_retransmits,
            max_packet_life_time: config.max_packet_lifetime.map(|d| d.as_millis() as u16),
            ..Default::default()
        };

        peer_connection
            .create_data_channel(label, Some(data_channel_config))
            .await
            .map_err(|e| {
                format!(
                    "Connection: {}",
                    format!("Failed to create data channel: {}", e)
                )
            })
    }

    /// Setup event handlers
    async fn setup_event_handlers(&self) -> Result<(), String> {
        handlers::setup_data_channel_handlers(
            &self.channel,
            self.label.clone(),
            self.peer_id,
            self.state.clone(),
            self.event_sender.clone(),
            self.bytes_received.clone(),
        )
        .await
    }

    /// Send data through channel
    pub async fn send(&self, data: Vec<u8>) -> Result<(), String> {
        self.validate_send_conditions(&data).await?;
        self.send_data_and_update_stats(data).await
    }

    /// Validate conditions for sending data
    async fn validate_send_conditions(&self, data: &[u8]) -> Result<(), String> {
        // Check if channel is open
        if *self.state.read().await != DataChannelState::Open {
            return Err("Data channel is not open".to_string());
        }

        // Check message size
        if data.len() > self.config.max_message_size {
            return Err(format!(
                "Message size {} exceeds maximum {}",
                data.len(),
                self.config.max_message_size
            ));
        }

        Ok(())
    }

    /// Send data and update statistics
    async fn send_data_and_update_stats(&self, data: Vec<u8>) -> Result<(), String> {
        let data_len = data.len() as u64;

        self.channel
            .send(&data.into())
            .await
            .map_err(|e| format!("Connection: {}", format!("Failed to send data: {}", e)))?;

        *self.bytes_sent.write().await += data_len;
        Ok(())
    }

    /// Get channel label
    pub fn label(&self) -> &str {
        &self.label
    }

    /// Get channel state
    pub async fn state(&self) -> DataChannelState {
        self.state.read().await.clone()
    }

    /// Get peer ID
    pub fn peer_id(&self) -> PeerId {
        self.peer_id
    }

    /// Close channel
    pub async fn close(&self) -> Result<(), String> {
        *self.state.write().await = DataChannelState::Closing;

        self.channel.close().await.map_err(|e| {
            format!(
                "Connection: {}",
                format!("Failed to close data channel: {}", e)
            )
        })?;

        Ok(())
    }

    /// Get channel statistics
    pub async fn stats(&self) -> DataChannelStats {
        DataChannelStats {
            label: self.label.clone(),
            peer_id: self.peer_id,
            state: self.state().await,
            bytes_sent: *self.bytes_sent.read().await,
            bytes_received: *self.bytes_received.read().await,
            buffer_size: self.config.data_channel_buffer_size,
            ordered: self.config.ordered_delivery,
        }
    }
}
