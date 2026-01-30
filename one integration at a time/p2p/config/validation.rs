use super::network::NetworkConfig;

/// Validate network configuration
pub fn validate_network_config(config: &NetworkConfig) -> Result<(), String> {
    validate_peer_limits(config)?;
    validate_timeouts(config)?;
    validate_sizes(config)?;
    Ok(())
}

/// Validate peer-related limits
fn validate_peer_limits(config: &NetworkConfig) -> Result<(), String> {
    if config.max_peers == 0 {
        return Err("max_peers must be greater than 0".to_string());
    }
    Ok(())
}

/// Validate timeout settings
fn validate_timeouts(config: &NetworkConfig) -> Result<(), String> {
    if config.connection_timeout.as_secs() == 0 {
        return Err("connection_timeout must be greater than 0".to_string());
    }
    Ok(())
}

/// Validate size settings
fn validate_sizes(config: &NetworkConfig) -> Result<(), String> {
    if config.max_message_size == 0 {
        return Err("max_message_size must be greater than 0".to_string());
    }

    if config.buffer_size == 0 {
        return Err("buffer_size must be greater than 0".to_string());
    }

    Ok(())
}
