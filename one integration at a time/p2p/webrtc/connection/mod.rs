pub mod handlers;
pub mod signaling;
pub mod state;
pub mod stats;

pub use state::ConnectionState;
pub use stats::ConnectionStats;

use super::config::WebRtcConfig;
use super::data_channel::DataChannel;
use libp2p::PeerId;
use std::collections::HashMap;
use std::sync::Arc;
use std::time::Instant;
use tokio::sync::{mpsc, RwLock};
use webrtc::api::APIBuilder;
use webrtc::ice_transport::ice_server::RTCIceServer;
use webrtc::peer_connection::configuration::RTCConfiguration;
use webrtc::peer_connection::RTCPeerConnection;

/// WebRTC peer connection wrapper
pub struct WebRtcConnection {
    peer_id: PeerId,
    peer_connection: Arc<RTCPeerConnection>,
    data_channels: Arc<RwLock<HashMap<String, DataChannel>>>,
    state: Arc<RwLock<ConnectionState>>,
    config: WebRtcConfig,
    created_at: Instant,
    event_sender: mpsc::UnboundedSender<super::WebRtcEvent>,
}

impl WebRtcConnection {
    /// Create new WebRTC connection
    pub async fn new(
        peer_id: PeerId,
        config: &WebRtcConfig,
        event_sender: mpsc::UnboundedSender<super::WebRtcEvent>,
    ) -> Result<Self, String> {
        let peer_connection = Self::create_peer_connection(config).await?;

        let connection = Self {
            peer_id,
            peer_connection,
            data_channels: Arc::new(RwLock::new(HashMap::new())),
            state: Arc::new(RwLock::new(ConnectionState::New)),
            config: config.clone(),
            created_at: Instant::now(),
            event_sender,
        };

        connection.setup_event_handlers().await?;
        Ok(connection)
    }

    /// Create WebRTC peer connection
    async fn create_peer_connection(
        config: &WebRtcConfig,
    ) -> Result<Arc<RTCPeerConnection>, String> {
        // Create WebRTC API
        let api = APIBuilder::new().build();

        // Convert ICE servers
        let ice_servers = Self::convert_ice_servers(config);

        // Create peer connection configuration
        let rtc_config = RTCConfiguration {
            ice_servers,
            ..Default::default()
        };

        // Create peer connection
        let peer_connection = Arc::new(api.new_peer_connection(rtc_config).await.map_err(|e| {
            format!(
                "Connection: {}",
                format!("Failed to create peer connection: {}", e)
            )
        })?);

        Ok(peer_connection)
    }

    /// Convert ICE servers from config
    fn convert_ice_servers(config: &WebRtcConfig) -> Vec<RTCIceServer> {
        config
            .ice_servers
            .iter()
            .map(|server| RTCIceServer {
                urls: server.urls.clone(),
                username: server.username.clone().unwrap_or_default(),
                credential: server.credential.clone().unwrap_or_default(),
                ..Default::default()
            })
            .collect()
    }

    /// Setup event handlers
    async fn setup_event_handlers(&self) -> Result<(), String> {
        handlers::setup_connection_handlers(
            &self.peer_connection,
            self.peer_id,
            self.state.clone(),
            self.event_sender.clone(),
        )
        .await
    }

    /// Create offer
    pub async fn create_offer(&self) -> Result<String, String> {
        signaling::create_offer(&self.peer_connection).await
    }

    /// Create answer
    pub async fn create_answer(&self, offer: String) -> Result<String, String> {
        signaling::create_answer(&self.peer_connection, offer).await
    }

    /// Set answer
    pub async fn set_answer(&self, answer: String) -> Result<(), String> {
        signaling::set_answer(&self.peer_connection, answer).await
    }

    /// Create data channel
    pub async fn create_data_channel(&self, label: String) -> Result<(), String> {
        let data_channel = DataChannel::new(
            &self.peer_connection,
            label.clone(),
            &self.config,
            self.peer_id,
            self.event_sender.clone(),
        )
        .await?;

        self.data_channels.write().await.insert(label, data_channel);
        Ok(())
    }

    /// Send data through channel
    pub async fn send_data(&self, channel_id: String, data: Vec<u8>) -> Result<(), String> {
        let channels = self.data_channels.read().await;
        if let Some(channel) = channels.get(&channel_id) {
            channel.send(data).await
        } else {
            Err(format!("Data channel '{}' not found", channel_id))
        }
    }

    /// Get connection state
    pub async fn state(&self) -> ConnectionState {
        self.state.read().await.clone()
    }

    /// Get peer ID
    pub fn peer_id(&self) -> PeerId {
        self.peer_id
    }

    /// Close connection
    pub async fn close(&self) -> Result<(), String> {
        self.peer_connection.close().await.map_err(|e| {
            format!(
                "Connection: {}",
                format!("Failed to close connection: {}", e)
            )
        })?;

        *self.state.write().await = ConnectionState::Closed;
        Ok(())
    }

    /// Get connection statistics
    pub async fn stats(&self) -> ConnectionStats {
        ConnectionStats {
            peer_id: self.peer_id,
            state: self.state().await,
            data_channels: self.data_channels.read().await.len(),
            created_at: self.created_at,
            bytes_sent: 0,     // Would be tracked by data channels
            bytes_received: 0, // Would be tracked by data channels
        }
    }
}
