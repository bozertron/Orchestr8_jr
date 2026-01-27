use anyhow::Result;
use rusqlite::params;

use super::DeliveryStatistics;

/// Query count for a specific status
fn query_status_count(conn: &rusqlite::Connection, status_condition: &str) -> Result<u32> {
    let count: u32 = conn.query_row(
        &format!(
            "SELECT COUNT(*) FROM p2p_delivery_status WHERE {}",
            status_condition
        ),
        [],
        |row| row.get(0),
    )?;
    Ok(count)
}

/// Query count for a specific status with time period
fn query_status_count_period(
    conn: &rusqlite::Connection,
    status_condition: &str,
    start: i64,
    end: i64,
) -> Result<u32> {
    let count: u32 = conn.query_row(
        &format!(
            "SELECT COUNT(*) FROM p2p_delivery_status WHERE {} AND created_at BETWEEN ?1 AND ?2",
            status_condition
        ),
        params![start, end],
        |row| row.get(0),
    )?;
    Ok(count)
}

/// Execute delivery status count queries
pub fn execute_status_queries(conn: &rusqlite::Connection) -> Result<(u32, u32, u32, u32, u32)> {
    let pending = query_status_count(conn, "status = 'pending'")?;
    let sent = query_status_count(conn, "status = 'sent'")?;
    let delivered = query_status_count(conn, "status = 'delivered'")?;
    let failed = query_status_count(conn, "status LIKE 'failed:%'")?;
    let timeout = query_status_count(conn, "status = 'timeout'")?;

    Ok((pending, sent, delivered, failed, timeout))
}

/// Execute period-filtered delivery status count queries
pub fn execute_period_status_queries(
    conn: &rusqlite::Connection,
    start_timestamp: i64,
    end_timestamp: i64,
) -> Result<(u32, u32, u32, u32, u32)> {
    let pending =
        query_status_count_period(conn, "status = 'pending'", start_timestamp, end_timestamp)?;
    let sent = query_status_count_period(conn, "status = 'sent'", start_timestamp, end_timestamp)?;
    let delivered =
        query_status_count_period(conn, "status = 'delivered'", start_timestamp, end_timestamp)?;
    let failed = query_status_count_period(
        conn,
        "status LIKE 'failed:%'",
        start_timestamp,
        end_timestamp,
    )?;
    let timeout =
        query_status_count_period(conn, "status = 'timeout'", start_timestamp, end_timestamp)?;

    Ok((pending, sent, delivered, failed, timeout))
}

/// Build DeliveryStatistics from query results
pub fn build_delivery_statistics(
    pending: u32,
    sent: u32,
    delivered: u32,
    failed: u32,
    timeout: u32,
) -> DeliveryStatistics {
    DeliveryStatistics {
        pending,
        sent,
        delivered,
        failed,
        timeout,
        total: pending + sent + delivered + failed + timeout,
    }
}
