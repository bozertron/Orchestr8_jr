use super::errors::RoutingError;
use super::TransportMethod;
use crate::p2p::manager::peer_ops::PeerOperations;
use crate::p2p::message::types::EncryptedMessage;
use crate::p2p::{PeerManager, WebRtcService};
use libp2p::PeerId;
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;

pub struct RelayClient;
impl RelayClient {
    async fn send(&self, to: PeerId, relay_addr: String, data: Vec<u8>) -> Result<(), String> {
        log::debug!(
            "Relay send to {} via {} ({} bytes)",
            to,
            relay_addr,
            data.len()
        );
        Ok(())
    }
}

pub struct TransportManager {
    webrtc_connections: HashMap<PeerId, String>, // PeerId -> channel_id
    libp2p_connections: HashMap<PeerId, bool>,   // PeerId -> connected
    relay_addresses: HashMap<PeerId, String>,    // PeerId -> relay_address
    // Injected backends
    webrtc_service: Option<Arc<RwLock<WebRtcService>>>,
    peer_manager: Option<Arc<RwLock<PeerManager>>>,
    relay_client: Option<Arc<RwLock<RelayClient>>>,
}

impl TransportManager {
    pub fn new() -> Self {
        Self {
            webrtc_connections: HashMap::new(),
            libp2p_connections: HashMap::new(),
            relay_addresses: HashMap::new(),
            webrtc_service: None,
            peer_manager: None,
            relay_client: None,
        }
    }

    pub fn with_webrtc_service(mut self, svc: Arc<RwLock<WebRtcService>>) -> Self {
        self.webrtc_service = Some(svc);
        self
    }

    pub fn with_peer_manager(mut self, mgr: Arc<RwLock<PeerManager>>) -> Self {
        self.peer_manager = Some(mgr);
        self
    }

    pub fn with_relay_client(mut self, client: Arc<RwLock<RelayClient>>) -> Self {
        self.relay_client = Some(client);
        self
    }

    pub async fn select_transport(&self, to: &PeerId) -> Result<TransportMethod, String> {
        // Priority 1: WebRTC data channel (direct P2P, lowest latency)
        if let Some(channel_id) = self.webrtc_connections.get(to) {
            return Ok(TransportMethod::WebRTC(channel_id.clone()));
        }

        // Priority 2: libp2p transport (reliable fallback)
        if self.libp2p_connections.get(to).copied().unwrap_or(false) {
            return Ok(TransportMethod::LibP2P);
        }

        // Priority 3: Relay routing (for NAT traversal)
        if let Some(relay_addr) = self.relay_addresses.get(to) {
            return Ok(TransportMethod::Relay(relay_addr.clone()));
        }

        Err(format!("No transport available for peer: {}", to))
    }

    pub async fn send_message(
        &self,
        to: PeerId,
        encrypted_message: EncryptedMessage,
        transport: &TransportMethod,
    ) -> Result<(), String> {
        match transport {
            TransportMethod::WebRTC(channel_id) => {
                self.send_via_webrtc(to, encrypted_message, channel_id)
                    .await
            }
            TransportMethod::LibP2P => self.send_via_libp2p(to, encrypted_message).await,
            TransportMethod::Relay(relay_addr) => {
                self.send_via_relay(to, encrypted_message, relay_addr).await
            }
        }
    }

    async fn send_via_webrtc(
        &self,
        to: PeerId,
        encrypted_message: EncryptedMessage,
        channel_id: &str,
    ) -> Result<(), String> {
        // Serialize encrypted message
        let data = serde_json::to_vec(&encrypted_message)
            .map_err(|e| format!("Serialization failed: {}", e))?;

        // Check message size limits for WebRTC
        if data.len() > 65536 {
            // 64KB limit for WebRTC data channels
            return Err(format!("{}", RoutingError::MessageTooLarge(data.len())));
        }

        if let Some(ref svc) = self.webrtc_service {
            let mut svc = svc.write().await;
            svc.send_data(to, channel_id.to_string(), data)
                .await
                .map_err(|e| format!("WebRTC send failed: {}", e))?;
            return Ok(());
        }
        Err(format!(
            "{}",
            RoutingError::TransportError("WebRTC service not available".into())
        ))
    }

    async fn send_via_libp2p(
        &self,
        to: PeerId,
        encrypted_message: EncryptedMessage,
    ) -> Result<(), String> {
        // Serialize encrypted message
        let data = serde_json::to_vec(&encrypted_message)
            .map_err(|e| format!("Serialization failed: {}", e))?;

        if let Some(ref mgr) = self.peer_manager {
            let mut mgr = mgr.write().await;
            mgr.send_message(to, data)
                .await
                .map_err(|e| format!("libp2p send failed: {}", e))?;
            return Ok(());
        }
        Err(format!(
            "{}",
            RoutingError::TransportError("libp2p PeerManager not available".into())
        ))
    }

    async fn send_via_relay(
        &self,
        to: PeerId,
        encrypted_message: EncryptedMessage,
        relay_addr: &str,
    ) -> Result<(), String> {
        // Serialize encrypted message
        let data = serde_json::to_vec(&encrypted_message)
            .map_err(|e| format!("Serialization failed: {}", e))?;

        if let Some(ref client) = self.relay_client {
            let client = client.read().await;
            client
                .send(to, relay_addr.to_string(), data)
                .await
                .map_err(|e| format!("relay send failed: {}", e))?;
            return Ok(());
        }
        Err(format!(
            "{}",
            RoutingError::TransportError("Relay client not available".into())
        ))
    }

    pub fn update_webrtc_connection(&mut self, peer_id: PeerId, channel_id: Option<String>) {
        match channel_id {
            Some(id) => {
                self.webrtc_connections.insert(peer_id, id);
            }
            None => {
                self.webrtc_connections.remove(&peer_id);
            }
        }
    }

    pub fn update_libp2p_connection(&mut self, peer_id: PeerId, connected: bool) {
        if connected {
            self.libp2p_connections.insert(peer_id, true);
        } else {
            self.libp2p_connections.remove(&peer_id);
        }
    }

    pub fn update_relay_address(&mut self, peer_id: PeerId, relay_addr: Option<String>) {
        match relay_addr {
            Some(addr) => {
                self.relay_addresses.insert(peer_id, addr);
            }
            None => {
                self.relay_addresses.remove(&peer_id);
            }
        }
    }

    pub fn has_transport(&self, peer_id: &PeerId) -> bool {
        self.webrtc_connections.contains_key(peer_id)
            || self
                .libp2p_connections
                .get(peer_id)
                .copied()
                .unwrap_or(false)
            || self.relay_addresses.contains_key(peer_id)
    }
}
