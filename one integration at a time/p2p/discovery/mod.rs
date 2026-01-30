pub mod behaviour;
pub mod events;

pub use behaviour::{create_discovery_behaviour, DiscoveryBehaviour};
pub use events::{DiscoveryBehaviourEvent, DiscoveryEvent};

use crate::p2p::{NetworkConfig, P2PEvent};
use libp2p::{Multiaddr, PeerId};
use std::collections::{HashMap, HashSet};
use tokio::sync::mpsc;

/// Discovery service for finding peers
pub struct Discovery {
    local_peer_id: PeerId,
    discovered_peers: HashSet<PeerId>,
    peer_addresses: HashMap<PeerId, Vec<Multiaddr>>,
    event_sender: mpsc::UnboundedSender<P2PEvent>,
    config: NetworkConfig,
}

impl Discovery {
    /// Create new discovery service
    pub async fn new(
        config: &NetworkConfig,
        event_sender: mpsc::UnboundedSender<P2PEvent>,
    ) -> Result<Self, String> {
        let local_peer_id = PeerId::random();

        Ok(Self {
            local_peer_id,
            discovered_peers: HashSet::new(),
            peer_addresses: HashMap::new(),
            event_sender,
            config: config.clone(),
        })
    }

    /// Start discovery service
    pub async fn start(&mut self) -> Result<(), String> {
        if self.config.enable_mdns {
            self.start_mdns_discovery().await?;
        }

        if self.config.enable_dht {
            self.start_dht_discovery().await?;
        }

        Ok(())
    }

    /// Stop discovery service
    pub async fn stop(&mut self) -> Result<(), String> {
        self.discovered_peers.clear();
        self.peer_addresses.clear();
        Ok(())
    }

    /// Start mDNS discovery for local peers
    async fn start_mdns_discovery(&mut self) -> Result<(), String> {
        // mDNS discovery will be handled by the swarm
        Ok(())
    }

    /// Start DHT discovery for remote peers
    async fn start_dht_discovery(&mut self) -> Result<(), String> {
        // DHT bootstrap will be handled by the swarm
        Ok(())
    }

    /// Handle discovery events
    pub async fn handle_event(&mut self, event: DiscoveryBehaviourEvent) -> Result<(), String> {
        match event {
            DiscoveryBehaviourEvent::Mdns(mdns_event) => {
                self.handle_mdns_event(mdns_event).await?;
            }
            DiscoveryBehaviourEvent::Kademlia(kad_event) => {
                self.handle_kademlia_event(kad_event).await?;
            }
        }
        Ok(())
    }

    /// Handle mDNS events
    async fn handle_mdns_event(&mut self, event: libp2p::mdns::Event) -> Result<(), String> {
        match event {
            libp2p::mdns::Event::Discovered(peers) => {
                for (peer_id, multiaddr) in peers {
                    if peer_id != self.local_peer_id {
                        self.add_discovered_peer(peer_id, vec![multiaddr]).await?;
                    }
                }
            }
            libp2p::mdns::Event::Expired(peers) => {
                for (peer_id, _) in peers {
                    self.remove_discovered_peer(peer_id).await?;
                }
            }
        }
        Ok(())
    }

    /// Handle Kademlia events
    async fn handle_kademlia_event(&mut self, event: libp2p::kad::Event) -> Result<(), String> {
        match event {
            libp2p::kad::Event::OutboundQueryProgressed { result, .. } => {
                match result {
                    libp2p::kad::QueryResult::GetClosestPeers(Ok(peers)) => {
                        for peer_info in peers.peers {
                            if peer_info.peer_id != self.local_peer_id {
                                // Query for addresses
                                self.query_peer_addresses(peer_info.peer_id).await?;
                            }
                        }
                    }
                    libp2p::kad::QueryResult::Bootstrap(Ok(_)) => {
                        self.send_event(P2PEvent::PeerDiscovered {
                            peer_id: self.local_peer_id,
                            addr: "/ip4/127.0.0.1/tcp/0".parse().unwrap(),
                        })
                        .await?;
                    }
                    _ => {}
                }
            }
            _ => {}
        }
        Ok(())
    }

    /// Add discovered peer
    async fn add_discovered_peer(
        &mut self,
        peer_id: PeerId,
        addresses: Vec<Multiaddr>,
    ) -> Result<(), String> {
        if self.discovered_peers.insert(peer_id) {
            self.peer_addresses.insert(peer_id, addresses.clone());

            for addr in addresses {
                self.send_event(P2PEvent::PeerDiscovered { peer_id, addr })
                    .await?;
            }
        }
        Ok(())
    }

    /// Remove discovered peer
    async fn remove_discovered_peer(&mut self, peer_id: PeerId) -> Result<(), String> {
        if self.discovered_peers.remove(&peer_id) {
            self.peer_addresses.remove(&peer_id);
            self.send_event(P2PEvent::PeerDisconnected { peer_id })
                .await?;
        }
        Ok(())
    }

    /// Query peer addresses
    async fn query_peer_addresses(&mut self, _peer_id: PeerId) -> Result<(), String> {
        // Implementation would query DHT for peer addresses
        Ok(())
    }

    /// Send event
    async fn send_event(&self, event: P2PEvent) -> Result<(), String> {
        self.event_sender
            .send(event)
            .map_err(|_| format!("Discovery: {}", "Failed to send event".to_string()))?;
        Ok(())
    }

    /// Get discovered peer count
    pub async fn discovered_count(&self) -> usize {
        self.discovered_peers.len()
    }

    /// Get discovered peers
    pub async fn discovered_peers(&self) -> HashSet<PeerId> {
        self.discovered_peers.clone()
    }

    /// Check if discovery is running
    pub fn is_running(&self) -> bool {
        // Discovery is considered running if we have a config enabled
        self.config.enable_mdns || self.config.enable_dht
    }

    /// Create discovery service for testing
    pub fn new_for_testing() -> Self {
        let (event_sender, _) = mpsc::unbounded_channel();
        Self {
            local_peer_id: PeerId::random(),
            discovered_peers: HashSet::new(),
            peer_addresses: HashMap::new(),
            event_sender,
            config: NetworkConfig::default(),
        }
    }
}
