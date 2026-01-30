/// Default bootstrap peers for P2P network
pub fn bootstrap_peers() -> Vec<String> {
    vec![
        "/ip4/104.131.131.82/tcp/4001/p2p/QmaCpDMGvV2BGHeYERUEnRQAwe3N8SzbUtfsmvsqQLuvuJ"
            .to_string(),
        "/ip4/104.131.131.82/udp/4001/quic/p2p/QmaCpDMGvV2BGHeYERUEnRQAwe3N8SzbUtfsmvsqQLuvuJ"
            .to_string(),
    ]
}

/// Default STUN servers for NAT traversal
pub fn stun_servers() -> Vec<String> {
    vec![
        "stun:stun.l.google.com:19302".to_string(),
        "stun:stun1.l.google.com:19302".to_string(),
    ]
}

/// Default protocols supported by JFDI
pub fn protocols() -> Vec<String> {
    vec![
        "/jfdi/chat/1.0.0".to_string(),
        "/jfdi/file/1.0.0".to_string(),
    ]
}
