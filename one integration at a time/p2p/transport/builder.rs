use crate::p2p::NetworkConfig;
use libp2p::{identity::Keypair, PeerId};

use super::P2PTransport;

/// Transport configuration builder
pub struct TransportBuilder {
    config: NetworkConfig,
    keypair: Option<Keypair>,
}

impl TransportBuilder {
    /// Create new transport builder
    pub fn new(config: NetworkConfig) -> Self {
        Self {
            config,
            keypair: None,
        }
    }

    /// Set keypair
    pub fn with_keypair(mut self, keypair: Keypair) -> Self {
        self.keypair = Some(keypair);
        self
    }

    /// Build transport
    pub async fn build(self) -> Result<P2PTransport, String> {
        let keypair = self.keypair.unwrap_or_else(|| Keypair::generate_ed25519());
        let peer_id = PeerId::from(keypair.public());

        let mut transport = P2PTransport::new(&self.config).await?;
        transport.keypair = keypair;
        transport.peer_id = peer_id;

        transport.validate_config()?;
        Ok(transport)
    }
}
