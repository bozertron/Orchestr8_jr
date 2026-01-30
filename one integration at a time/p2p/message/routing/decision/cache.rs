use libp2p::PeerId;
use std::collections::HashMap;
use std::time::{Duration, Instant};

/// Connection status cache for performance
pub(super) struct ConnectionCache {
    webrtc_status: HashMap<PeerId, ConnectionStatus>,
    libp2p_status: HashMap<PeerId, ConnectionStatus>,
    cache_ttl: Duration,
}

/// Connection status with timestamp
#[derive(Debug, Clone)]
pub(super) struct ConnectionStatus {
    pub is_connected: bool,
    pub last_checked: Instant,
    #[allow(dead_code)] // Used for latency-based routing decisions
    pub latency_ms: Option<u64>,
}

impl ConnectionCache {
    pub fn new() -> Self {
        Self {
            webrtc_status: HashMap::new(),
            libp2p_status: HashMap::new(),
            cache_ttl: Duration::from_secs(5), // 5 second cache
        }
    }

    pub fn get_webrtc_status(&self, peer_id: &PeerId) -> Option<ConnectionStatus> {
        self.webrtc_status.get(peer_id).and_then(|status| {
            if status.last_checked.elapsed() < self.cache_ttl {
                Some(status.clone())
            } else {
                None
            }
        })
    }

    pub fn get_libp2p_status(&self, peer_id: &PeerId) -> Option<ConnectionStatus> {
        self.libp2p_status.get(peer_id).and_then(|status| {
            if status.last_checked.elapsed() < self.cache_ttl {
                Some(status.clone())
            } else {
                None
            }
        })
    }

    pub fn update_webrtc_status(
        &mut self,
        peer_id: PeerId,
        is_connected: bool,
        latency_ms: Option<u64>,
    ) {
        self.webrtc_status.insert(
            peer_id,
            ConnectionStatus {
                is_connected,
                last_checked: Instant::now(),
                latency_ms,
            },
        );
    }

    pub fn update_libp2p_status(
        &mut self,
        peer_id: PeerId,
        is_connected: bool,
        latency_ms: Option<u64>,
    ) {
        self.libp2p_status.insert(
            peer_id,
            ConnectionStatus {
                is_connected,
                last_checked: Instant::now(),
                latency_ms,
            },
        );
    }

    pub fn invalidate_peer(&mut self, peer_id: &PeerId) {
        self.webrtc_status.remove(peer_id);
        self.libp2p_status.remove(peer_id);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_connection_cache_ttl() {
        let mut cache = ConnectionCache::new();
        let peer_id = PeerId::random();

        // Add status to cache
        cache.update_webrtc_status(peer_id, true, Some(50));

        // Should be in cache
        assert!(cache.get_webrtc_status(&peer_id).is_some());

        // Wait for cache to expire
        tokio::time::sleep(Duration::from_secs(6)).await;

        // Should be expired
        assert!(cache.get_webrtc_status(&peer_id).is_none());
    }
}
