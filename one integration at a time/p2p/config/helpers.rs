use super::network::NetworkConfig;

/// Get effective bootstrap peers for the network
pub fn effective_bootstrap_peers(config: &NetworkConfig) -> Vec<String> {
    if config.bootstrap_peers.is_empty() {
        get_default_bootstrap_peers()
    } else {
        config.bootstrap_peers.clone()
    }
}

/// Get default bootstrap peers when none are configured
fn get_default_bootstrap_peers() -> Vec<String> {
    vec![
        "/ip4/104.131.131.82/tcp/4001/p2p/QmaCpDMGvV2BGHeYERUEnRQAwe3N8SzbUtfsmvsqQLuvuJ"
            .to_string(),
    ]
}
