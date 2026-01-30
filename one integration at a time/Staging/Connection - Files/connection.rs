use webrtc::api::media_engine::MediaEngine;
use webrtc::api::APIBuilder;
use webrtc::peer_connection::configuration::RTCConfiguration;
use webrtc::peer_connection::ice_server::RTCIceServer;
use webrtc::peer_connection::peer_connection_state::RTCPeerConnectionState;
use webrtc::peer_connection::sdp::session_description::RTCSessionDescription;
use webrtc::ice_transport::ice_candidate::RTCIceCandidateInit;

use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::Mutex;
use uuid::Uuid;
use tauri::{AppHandle, Manager}; // To emit signals back to frontend

use crate::state::AppState; // Keep AppState for potential future use within manager logic
use crate::models::ClientSignal; // Corrected import path
use crate::error::{CommandResult, CommandError}; // Use orchestr8 error types
use log::{info, warn, error, debug}; // Added log import
use serde_json; // Added for JSON handling

// Event name for sending signals back to the frontend for a specific peer
const EVENT_PEER_SIGNAL: &str = "webrtc://peer-signal";
const EVENT_PEER_CONNECTED: &str = "webrtc://peer-connected";
const EVENT_PEER_DISCONNECTED: &str = "webrtc://peer-disconnected";
// TODO: Add events for data channel messages, media tracks, etc.

// Manages all active WebRTC peer connections
// This manager instance will be stored within AppState
pub struct WebRtcManager {
    // Map Peer Client ID -> Peer Connection details
    // Using Arc<Mutex<...>> for individual peer connection might be needed
    // depending on how the webrtc library handles threading.
    // A more robust implementation would likely involve spawning tasks per connection.
    // Using tokio::sync::Mutex for async locking.
    pub peers: Mutex<HashMap<Uuid, PeerConnectionInfo>>,
    // AppHandle needed to emit events back to the frontend
    pub app_handle: AppHandle,
    pub self_id: Uuid, // The ID of the local client owning this manager
}

#[derive(Debug)] // Added Debug derive
pub struct PeerConnectionInfo {
    // Placeholder for actual webrtc::peer_connection::RTCPeerConnection
    // Needs Arc<Mutex<RTCPeerConnection>> likely
    // connection: Arc<webrtc::peer_connection::RTCPeerConnection>,
    pub target_id: Uuid,
    // Add state flags, data channels, etc. as needed
}

impl WebRtcManager {
    pub fn new(app_handle: AppHandle, self_id: Uuid) -> Self {
        WebRtcManager {
            peers: Mutex::new(HashMap::new()),
            app_handle,
            self_id,
        }
    }

    // --- Core WebRTC Logic (Placeholders) ---

    /// Initiates a connection to a target peer. Called by a Tauri command.
    pub async fn connect_to_peer(&self, target_id: Uuid) -> CommandResult<()> { // Updated return type
        info!("Attempting to connect to peer: {}", target_id); // Use info! directly
        let mut peers = self.peers.lock().await;
        if peers.contains_key(&target_id) {
            warn!("Already have a connection or pending connection with peer: {}", target_id); // Use warn!
            return Ok(()); // Or return an error? For now, Ok is fine.
        }

        // 1. Create MediaEngine
        let mut m = MediaEngine::default();
        // TODO: Register codecs if needed (e.g., for audio/video)
        // m.register_default_codecs()?; // Example

        // 2. Create API
        let api = APIBuilder::new().with_media_engine(m).build();

        // 3. Prepare ICE server configuration (e.g., STUN servers)
        let config = RTCConfiguration {
            ice_servers: vec![RTCIceServer {
                urls: vec!["stun:stun.l.google.com:19302".to_owned()],
                ..Default::default()
            }],
            ..Default::default()
        };

        // 4. Create PeerConnection
        // The `?` here will now correctly map webrtc::Error to CommandError::WebRTC
        let peer_connection = Arc::new(api.new_peer_connection(config).await?);

        // TODO: Create DataChannel(s) if needed for chat/file transfer
        // let data_channel = peer_connection.create_data_channel("data", None).await?; // Needs error mapping if used
        // data_channel.on_open(...)
        // data_channel.on_message(...)
        // data_channel.on_close(...)

        // --- Setup Event Handlers ---
        let app_handle_clone = self.app_handle.clone();
        let self_id_clone = self.self_id;
        let target_id_clone = target_id; // Clone target_id for use in closures

        // Handle ICE Candidates: Send them to the peer via signaling
        peer_connection.on_ice_candidate(Box::new(move |c: Option<webrtc::ice_transport::ice_candidate::RTCIceCandidate>| {
            let app_handle = app_handle_clone.clone();
            let target_id = target_id_clone; // Use cloned target_id
            let self_id = self_id_clone;
            Box::pin(async move {
                if let Some(candidate) = c {
                            match candidate.to_json() { // webrtc::Error potential here
                                Ok(candidate_init) => {
                                    debug!("Generated ICE candidate for {}: {:?}", target_id, candidate_init); // Use debug!
                                    // Map potential serde_json error during value conversion
                                    let signal_value = serde_json::to_value(candidate_init)
                                        .map_err(|e| CommandError::WebRTC(format!("ICE candidate serialization failed: {}", e)))?; // Map serde error

                                    let signal_payload = ClientSignal {
                                        client_id: self_id, // Sender is self
                                        target_client_id: target_id,
                                        signal: signal_value,
                                    };
                                     // Emit signal event back to frontend to send via command
                                     if let Err(e) = app_handle.emit(EVENT_PEER_SIGNAL, signal_payload) {
                                         error!("Failed to emit ICE candidate signal event: {}", e); // Use error!
                                         // Note: Cannot return error directly from here easily due to Box::pin
                                     }
                                }
                                Err(e) => {
                                    error!("Failed to serialize ICE candidate: {}", e); // Use error!
                                }
                            }
                        } else {
                            debug!("ICE Candidate gathering complete for peer {}", target_id); // Use debug!
                        }
                    })
                })); // Note: Error handling within callbacks is tricky. Best effort logging for now.

        // Handle Connection State Changes
        let app_handle_clone2 = self.app_handle.clone();
        let target_id_clone2 = target_id;
        peer_connection.on_peer_connection_state_change(Box::new(move |s: RTCPeerConnectionState| {
             let app_handle = app_handle_clone2.clone();
             let target_id = target_id_clone2;
            info!("Peer connection state with {} changed: {}", target_id, s); // Use info!
            Box::pin(async move {
                match s {
                    RTCPeerConnectionState::Connected => {
                         info!("Peer {} connected!", target_id); // Use info!
                         if let Err(e) = app_handle.emit(EVENT_PEER_CONNECTED, target_id) {
                             error!("Failed to emit peer-connected event: {}", e); // Use error!
                         }
                    },
                    RTCPeerConnectionState::Disconnected | RTCPeerConnectionState::Failed | RTCPeerConnectionState::Closed => {
                         info!("Peer {} disconnected/failed/closed.", target_id); // Use info!
                         if let Err(e) = app_handle.emit(EVENT_PEER_DISCONNECTED, target_id) {
                             error!("Failed to emit peer-disconnected event: {}", e); // Use error!
                         }
                         // TODO: Add cleanup logic here (remove peer from manager, close channels)
                         // This might involve sending a message back to the manager task/thread
                    },
                    _ => {} // Other states ignored for now
                }
            })
        }));

        // TODO: Handle DataChannel events (on_data_channel)
        // TODO: Handle Track events for audio/video (on_track)

        // 5. Create Offer
        let offer = peer_connection.create_offer(None).await?; // Maps webrtc::Error
        // Set local description (and start gathering ICE candidates)
        peer_connection.set_local_description(offer.clone()).await?; // Maps webrtc::Error

        // 6. Send Offer to Peer via Signaling (emit event to frontend)
        // Map potential serde_json error during value conversion
        let signal_value = serde_json::to_value(offer)
            .map_err(|e| CommandError::WebRTC(format!("Offer serialization failed: {}", e)))?; // Map serde error

        let signal_payload = ClientSignal {
            client_id: self.self_id,
            target_client_id: target_id,
            signal: signal_value,
        };
         if let Err(e) = self.app_handle.emit(EVENT_PEER_SIGNAL, signal_payload) {
             error!("Failed to emit offer signal event: {}", e); // Use error!
             // Map Tauri error to CommandError::TauriError
             return Err(CommandError::TauriError(e));
         }

        // Store placeholder info (replace with actual Arc<Mutex<RTCPeerConnection>>)
        peers.insert(target_id, PeerConnectionInfo { target_id });
        info!("Offer sent to peer {}, connection initiated.", target_id); // Use info!

        Ok(())
    }

    /// Handles an incoming signal (offer, answer, candidate) from a peer
    pub async fn handle_incoming_signal(&self, signal_data: ClientSignal) -> CommandResult<()> { // Updated return type
        let from_id = signal_data.client_id;
        info!("Handling incoming signal from peer: {}", from_id); // Use info!
        let _peers = self.peers.lock().await; // Lock peers, use _peers if not modifying directly yet

        // Deserialize the signal payload (assuming it's either SDP or ICE candidate)
        // This part is complex and depends heavily on the exact structure sent by the frontend
        // We need to differentiate between Offer, Answer, and ICE Candidate

        // Example placeholder logic:
        // Try deserializing as SDP first
        if let Ok(sdp) = serde_json::from_value::<RTCSessionDescription>(signal_data.signal.clone()) {
             debug!("Received SDP ({}) from {}", sdp.sdp_type, from_id); // Use debug!
             // TODO: Get or create the peer connection for `from_id`
             // TODO: Set remote description (if offer, create answer; if answer, connection established)
             //       Ensure errors within this block are mapped to CommandError
             // Example:
             // if let Some(pc_info) = peers.get(&from_id) {
             //     let pc = pc_info.connection.lock().await; // Assuming Arc<Mutex<RTCPeerConnection>>
             //     pc.set_remote_description(sdp).await?;
             //     if sdp.sdp_type == RTCSdpType::Offer {
             //         let answer = pc.create_answer(None).await?;
             //         pc.set_local_description(answer.clone()).await?;
             //         // Send answer back via signaling (emit event)
             //     }
             // } else { // Need to create connection if receiving offer first
             //      // ... create peer connection similar to connect_to_peer ...
             //      // set remote description, create answer, set local, send answer...
             // }

        // If not SDP, try deserializing as ICE candidate
        } else if let Ok(candidate) = serde_json::from_value::<RTCIceCandidateInit>(signal_data.signal.clone()) { // Clone signal data again
             debug!("Received ICE Candidate from {}: {:?}", from_id, candidate.candidate); // Use debug!
             // TODO: Get the peer connection for `from_id`
             // TODO: Add the ICE candidate
             //       Ensure errors within this block are mapped to CommandError
             // Example:
             // if let Some(pc_info) = peers.get(&from_id) {
             //     let pc = pc_info.connection.lock().await;
             //     pc.add_ice_candidate(candidate).await?; // Maps webrtc::Error
             // } else {
             //     warn!("Received ICE candidate for unknown peer: {}", from_id); // Use warn!
             // }
        } else {
            warn!("Received unknown signal structure from {}: {:?}", from_id, signal_data.signal); // Use warn!
            // Map unknown format to CommandError::WebRTC
            return Err(CommandError::WebRTC(format!("Unknown signal format received from {}", from_id)));
        }


        Ok(())
    }

     /// Cleans up connection for a disconnected peer. Called internally or by a command.
     pub async fn peer_disconnected(&self, target_id: Uuid) {
         info!("Cleaning up connection for peer: {}", target_id); // Use info!
         let mut peers = self.peers.lock().await;
         if let Some(_pc_info) = peers.remove(&target_id) {
              // TODO: Add actual cleanup logic if RTCPeerConnection was stored
              // e.g., pc_info.connection.close().await; // Needs error handling
              info!("Removed peer {} from manager.", target_id); // Use info!
         } else {
             warn!("Attempted to clean up non-existent peer: {}", target_id); // Use warn!
         }
     }

}

// Implement Drop for cleanup if needed, though manual cleanup via commands might be better
// impl Drop for WebRtcManager { ... }

// Note: From<webrtc::Error> for CommandError was added in error.rs
