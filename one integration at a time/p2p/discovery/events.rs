use libp2p::{
    kad::{Event as KademliaEvent, QueryResult},
    mdns::Event as MdnsEvent,
    Multiaddr, PeerId,
};

/// Discovery events
#[derive(Debug, Clone)]
pub enum DiscoveryEvent {
    PeerDiscovered {
        peer_id: PeerId,
        addresses: Vec<Multiaddr>,
    },
    PeerExpired {
        peer_id: PeerId,
    },
    BootstrapComplete,
    QueryComplete {
        peer_id: PeerId,
        result: QueryResult,
    },
}

/// Combined discovery behaviour events
#[derive(Debug)]
pub enum DiscoveryBehaviourEvent {
    Kademlia(KademliaEvent),
    Mdns(MdnsEvent),
}

impl From<KademliaEvent> for DiscoveryBehaviourEvent {
    fn from(event: KademliaEvent) -> Self {
        DiscoveryBehaviourEvent::Kademlia(event)
    }
}

impl From<MdnsEvent> for DiscoveryBehaviourEvent {
    fn from(event: MdnsEvent) -> Self {
        DiscoveryBehaviourEvent::Mdns(event)
    }
}
