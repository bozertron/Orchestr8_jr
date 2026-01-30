use crate::p2p::message::types::*;
use anyhow::Result;
use libp2p::PeerId;

use super::queries_helpers::MessageFilter;
use super::PersistenceQueries;

/// Helper functions for operations implementation
pub struct OperationsImplHelpers;

impl OperationsImplHelpers {
    /// Get messages by peer (helper wrapper)
    pub async fn get_messages_by_peer_filtered(
        queries: &PersistenceQueries,
        peer_id: &PeerId,
        limit: Option<u32>,
    ) -> Result<Vec<P2PMessage>> {
        let filter = MessageFilter {
            sender_id: Some(peer_id.clone()),
            limit,
            ..Default::default()
        };
        queries.get_messages_filtered(&filter).await
    }

    /// Get recent messages (helper wrapper)
    pub async fn get_recent_messages_filtered(
        queries: &PersistenceQueries,
        limit: Option<u32>,
    ) -> Result<Vec<P2PMessage>> {
        let filter = MessageFilter {
            limit,
            ..Default::default()
        };
        queries.get_messages_filtered(&filter).await
    }

    /// Get messages by type (helper wrapper)
    pub async fn get_messages_by_type_filtered(
        queries: &PersistenceQueries,
        message_type: &str,
        limit: Option<u32>,
    ) -> Result<Vec<P2PMessage>> {
        let filter = MessageFilter {
            message_type: Some(message_type.to_string()),
            limit,
            ..Default::default()
        };
        queries.get_messages_filtered(&filter).await
    }
}
