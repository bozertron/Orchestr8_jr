use crate::p2p::NetworkConfig;
use libp2p::{
    kad::{store::MemoryStore, Behaviour as Kademlia, Config as KademliaConfig},
    mdns::{tokio::Behaviour as Mdns, Config as MdnsConfig},
    swarm::NetworkBehaviour,
    PeerId, StreamProtocol,
};
use std::num::NonZeroUsize;
use std::time::Duration;

use super::events::DiscoveryBehaviourEvent;

/// Network behaviour for discovery
#[derive(NetworkBehaviour)]
#[behaviour(to_swarm = "DiscoveryBehaviourEvent")]
pub struct DiscoveryBehaviour {
    pub kademlia: Kademlia<MemoryStore>,
    pub mdns: Mdns,
}

/// Create discovery behaviour
pub fn create_discovery_behaviour(
    local_peer_id: PeerId,
    config: &NetworkConfig,
) -> Result<DiscoveryBehaviour, String> {
    // Create Kademlia DHT
    let store = MemoryStore::new(local_peer_id);
    let protocol_name = StreamProtocol::new("/ipfs/kad/1.0.0");
    let mut kad_config = KademliaConfig::new(protocol_name);
    kad_config.set_query_timeout(Duration::from_secs(60));
    kad_config.set_replication_factor(
        NonZeroUsize::new(config.dht_replication_factor).unwrap_or(NonZeroUsize::new(20).unwrap()),
    );

    let kademlia = Kademlia::with_config(local_peer_id, store, kad_config);

    // Create mDNS
    let mdns_config = MdnsConfig::default();
    let mdns = Mdns::new(mdns_config, local_peer_id)
        .map_err(|e| format!("Discovery: {}", format!("Failed to create mDNS: {}", e)))?;

    Ok(DiscoveryBehaviour { kademlia, mdns })
}
