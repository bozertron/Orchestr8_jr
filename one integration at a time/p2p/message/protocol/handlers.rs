use super::super::types::*;
use super::builders::MessageBuilders;
use super::state::*;

use std::collections::HashMap;

/// Message protocol handler
pub struct MessageProtocol {
    pending_confirmations: HashMap<MessageId, PendingConfirmation>,
    file_transfers: HashMap<TransferId, FileTransferState>,
    active_calls: HashMap<CallId, CallState>,
}

impl MessageProtocol {
    /// Create new message protocol handler
    pub fn new() -> Self {
        Self {
            pending_confirmations: HashMap::new(),
            file_transfers: HashMap::new(),
            active_calls: HashMap::new(),
        }
    }

    /// Handle incoming message and generate appropriate responses
    pub fn handle_message(&mut self, message: P2PMessage) -> Result<Vec<P2PMessage>, String> {
        match &message {
            P2PMessage::Chat { id, .. } => self.handle_chat_message(*id),
            P2PMessage::FileOffer { id, name, size, .. } => {
                self.handle_file_offer(*id, name, *size)
            }
            P2PMessage::FileChunk { id, data, .. } => self.handle_file_chunk(*id, data),
            P2PMessage::CallInvite {
                call_id, call_type, ..
            } => self.handle_call_invite(*call_id, call_type),
            P2PMessage::CallAnswer {
                call_id, accepted, ..
            } => self.handle_call_answer(*call_id, *accepted),
            P2PMessage::CallHangup { call_id, .. } => self.handle_call_hangup(*call_id),
            P2PMessage::Ping { nonce, .. } => self.handle_ping(*nonce),
            P2PMessage::DeliveryConfirmation { message_id, .. } => {
                self.handle_delivery_confirmation(*message_id)
            }
            _ => Ok(Vec::new()),
        }
    }

    /// Handle chat message
    fn handle_chat_message(&mut self, id: MessageId) -> Result<Vec<P2PMessage>, String> {
        Ok(vec![MessageBuilders::create_delivery_confirmation(id)])
    }

    /// Handle file offer
    fn handle_file_offer(
        &mut self,
        id: TransferId,
        name: &str,
        size: u64,
    ) -> Result<Vec<P2PMessage>, String> {
        self.file_transfers.insert(
            id,
            FileTransferState {
                transfer_id: id,
                filename: name.to_string(),
                total_size: size,
                received_bytes: 0,
                status: TransferStatus::Offered,
            },
        );
        Ok(Vec::new())
    }

    /// Handle file chunk
    fn handle_file_chunk(
        &mut self,
        id: TransferId,
        data: &[u8],
    ) -> Result<Vec<P2PMessage>, String> {
        if let Some(transfer) = self.file_transfers.get_mut(&id) {
            transfer.received_bytes += data.len() as u64;
            if transfer.received_bytes >= transfer.total_size {
                transfer.status = TransferStatus::Complete;
                return Ok(vec![P2PMessage::FileComplete { id }]);
            }
        }
        Ok(Vec::new())
    }

    /// Handle call invite
    fn handle_call_invite(
        &mut self,
        call_id: CallId,
        call_type: &CallType,
    ) -> Result<Vec<P2PMessage>, String> {
        self.active_calls.insert(
            call_id,
            CallState {
                call_id,
                call_type: call_type.clone(),
                status: CallStatus::Incoming,
            },
        );
        Ok(Vec::new())
    }

    /// Handle call answer
    fn handle_call_answer(
        &mut self,
        call_id: CallId,
        accepted: bool,
    ) -> Result<Vec<P2PMessage>, String> {
        if let Some(call) = self.active_calls.get_mut(&call_id) {
            call.status = if accepted {
                CallStatus::Active
            } else {
                CallStatus::Declined
            };
        }
        Ok(Vec::new())
    }

    /// Handle call hangup
    fn handle_call_hangup(&mut self, call_id: CallId) -> Result<Vec<P2PMessage>, String> {
        self.active_calls.remove(&call_id);
        Ok(Vec::new())
    }

    /// Handle ping
    fn handle_ping(&mut self, nonce: u64) -> Result<Vec<P2PMessage>, String> {
        Ok(vec![MessageBuilders::create_pong(nonce)])
    }

    /// Handle delivery confirmation
    fn handle_delivery_confirmation(
        &mut self,
        message_id: MessageId,
    ) -> Result<Vec<P2PMessage>, String> {
        self.pending_confirmations.remove(&message_id);
        Ok(Vec::new())
    }

    /// Get pending file transfers
    pub fn get_file_transfers(&self) -> &HashMap<TransferId, FileTransferState> {
        &self.file_transfers
    }

    /// Get active calls
    pub fn get_active_calls(&self) -> &HashMap<CallId, CallState> {
        &self.active_calls
    }

    /// Accept file transfer
    pub fn accept_file_transfer(&mut self, transfer_id: TransferId) -> Result<(), String> {
        if let Some(transfer) = self.file_transfers.get_mut(&transfer_id) {
            transfer.status = TransferStatus::Accepted;
            Ok(())
        } else {
            Err(format!(
                "Connection: {}",
                format!("File transfer {} not found", transfer_id)
            ))
        }
    }

    /// Cancel file transfer
    pub fn cancel_file_transfer(&mut self, transfer_id: TransferId, reason: String) -> P2PMessage {
        self.file_transfers.remove(&transfer_id);
        P2PMessage::FileCancel {
            id: transfer_id,
            reason,
        }
    }

    /// Answer call
    pub fn answer_call(
        &mut self,
        call_id: CallId,
        accepted: bool,
        sdp_answer: Option<String>,
    ) -> Result<P2PMessage, String> {
        if let Some(call) = self.active_calls.get_mut(&call_id) {
            call.status = if accepted {
                CallStatus::Active
            } else {
                CallStatus::Declined
            };

            Ok(P2PMessage::CallAnswer {
                call_id,
                accepted,
                sdp_answer,
            })
        } else {
            Err(format!(
                "Connection: {}",
                format!("Call {} not found", call_id)
            ))
        }
    }

    /// Hangup call
    pub fn hangup_call(&mut self, call_id: CallId, reason: HangupReason) -> P2PMessage {
        self.active_calls.remove(&call_id);
        P2PMessage::CallHangup { call_id, reason }
    }
}

impl Default for MessageProtocol {
    fn default() -> Self {
        Self::new()
    }
}
