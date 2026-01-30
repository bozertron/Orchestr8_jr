use std::sync::Arc;
use webrtc::peer_connection::sdp::session_description::RTCSessionDescription;
use webrtc::peer_connection::RTCPeerConnection;

/// Create WebRTC offer
pub async fn create_offer(peer_connection: &Arc<RTCPeerConnection>) -> Result<String, String> {
    let offer = peer_connection
        .create_offer(None)
        .await
        .map_err(|e| format!("Connection: {}", format!("Failed to create offer: {}", e)))?;

    peer_connection
        .set_local_description(offer.clone())
        .await
        .map_err(|e| {
            format!(
                "Connection: {}",
                format!("Failed to set local description: {}", e)
            )
        })?;

    Ok(offer.sdp)
}

/// Create WebRTC answer
pub async fn create_answer(
    peer_connection: &Arc<RTCPeerConnection>,
    offer: String,
) -> Result<String, String> {
    let offer_desc = RTCSessionDescription::offer(offer)
        .map_err(|e| format!("Connection: {}", format!("Invalid offer: {}", e)))?;

    peer_connection
        .set_remote_description(offer_desc)
        .await
        .map_err(|e| {
            format!(
                "Connection: {}",
                format!("Failed to set remote description: {}", e)
            )
        })?;

    let answer = peer_connection
        .create_answer(None)
        .await
        .map_err(|e| format!("Connection: {}", format!("Failed to create answer: {}", e)))?;

    peer_connection
        .set_local_description(answer.clone())
        .await
        .map_err(|e| {
            format!(
                "Connection: {}",
                format!("Failed to set local description: {}", e)
            )
        })?;

    Ok(answer.sdp)
}

/// Set WebRTC answer
pub async fn set_answer(
    peer_connection: &Arc<RTCPeerConnection>,
    answer: String,
) -> Result<(), String> {
    let answer_desc = RTCSessionDescription::answer(answer)
        .map_err(|e| format!("Connection: {}", format!("Invalid answer: {}", e)))?;

    peer_connection
        .set_remote_description(answer_desc)
        .await
        .map_err(|e| {
            format!(
                "Connection: {}",
                format!("Failed to set remote description: {}", e)
            )
        })?;

    Ok(())
}
