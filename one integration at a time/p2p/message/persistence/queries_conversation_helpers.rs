use libp2p::PeerId;

use crate::p2p::message::persistence::queries_helpers::row_to_message;
use crate::p2p::message::types::StoredMessage;

/// Build SQL query for recent conversations
pub fn build_recent_conversations_query() -> &'static str {
    "SELECT DISTINCT
        CASE
            WHEN sender_id = (SELECT sender_id FROM p2p_messages LIMIT 1)
            THEN recipient_id
            ELSE sender_id
        END as peer_id,
        id, message_type, content, sender_id, recipient_id,
        timestamp, signature, encryption_key_id, content_hash, metadata
     FROM p2p_messages
     WHERE timestamp = (
         SELECT MAX(timestamp)
         FROM p2p_messages m2
         WHERE m2.sender_id = p2p_messages.sender_id
            OR m2.recipient_id = p2p_messages.recipient_id
     )
     ORDER BY timestamp DESC
     LIMIT ?1"
}

/// Parse conversation row into (PeerId, StoredMessage) tuple
pub fn parse_conversation_row(row: &rusqlite::Row) -> rusqlite::Result<(PeerId, StoredMessage)> {
    let peer_id_str: String = row.get("peer_id")?;
    let peer_id = PeerId::from_bytes(&peer_id_str.as_bytes()).map_err(|_| {
        rusqlite::Error::InvalidColumnType(0, "peer_id".to_string(), rusqlite::types::Type::Text)
    })?;
    let message = row_to_message(row)?;
    Ok((peer_id, message))
}
