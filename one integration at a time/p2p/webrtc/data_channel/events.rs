/// Data channel events
#[derive(Debug, Clone)]
pub enum DataChannelEvent {
    Opened { channel_id: String },
    Closed { channel_id: String },
    MessageReceived { channel_id: String, data: Vec<u8> },
    Error { channel_id: String, error: String },
}
