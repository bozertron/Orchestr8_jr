// Calendar Recurrence Engine
// Pattern Bible Compliance: File ≤200 lines, Functions ≤30 lines

use chrono::{DateTime, Datelike, Duration, Utc, Weekday};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum RecurrencePattern {
    Daily { interval: u32 },
    Weekly { interval: u32, days: Vec<Weekday> },
    Monthly { interval: u32, day_of_month: u8 },
    Yearly { interval: u32, month: u8, day: u8 },
    Custom { rule: String }, // iCalendar RRULE format
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RecurrenceRule {
    pub pattern: RecurrencePattern,
    pub start_date: DateTime<Utc>,
    pub end_date: Option<DateTime<Utc>>,
    pub occurrences: Option<u32>,
    pub exceptions: Vec<DateTime<Utc>>, // Dates to skip
}

impl RecurrenceRule {
    pub fn new(pattern: RecurrencePattern, start_date: DateTime<Utc>) -> Self {
        Self {
            pattern,
            start_date,
            end_date: None,
            occurrences: None,
            exceptions: vec![],
        }
    }

    pub fn with_end_date(mut self, end_date: DateTime<Utc>) -> Self {
        self.end_date = Some(end_date);
        self
    }

    pub fn with_occurrences(mut self, count: u32) -> Self {
        self.occurrences = Some(count);
        self
    }

    pub fn add_exception(&mut self, date: DateTime<Utc>) {
        self.exceptions.push(date);
    }

    pub fn generate_occurrences(
        &self,
        from: DateTime<Utc>,
        to: DateTime<Utc>,
    ) -> Vec<DateTime<Utc>> {
        let mut occurrences = Vec::new();
        let mut current = self.start_date;
        let mut count = 0;

        while current <= to {
            if current >= from && !self.is_exception(current) {
                occurrences.push(current);
                count += 1;

                if let Some(max) = self.occurrences {
                    if count >= max {
                        break;
                    }
                }
            }

            if let Some(end) = self.end_date {
                if current >= end {
                    break;
                }
            }

            current = self.next_occurrence(current);
        }

        occurrences
    }

    fn next_occurrence(&self, current: DateTime<Utc>) -> DateTime<Utc> {
        match &self.pattern {
            RecurrencePattern::Daily { interval } => current + Duration::days(*interval as i64),
            RecurrencePattern::Weekly { interval, days } => {
                self.next_weekly(current, *interval, days)
            }
            RecurrencePattern::Monthly {
                interval,
                day_of_month,
            } => self.next_monthly(current, *interval, *day_of_month),
            RecurrencePattern::Yearly {
                interval,
                month,
                day,
            } => self.next_yearly(current, *interval, *month, *day),
            RecurrencePattern::Custom { .. } => {
                // Simplified: advance by 1 day for custom rules
                current + Duration::days(1)
            }
        }
    }

    fn next_weekly(
        &self,
        current: DateTime<Utc>,
        interval: u32,
        days: &[Weekday],
    ) -> DateTime<Utc> {
        let mut next = current + Duration::days(1);
        let target_week = current + Duration::weeks(interval as i64);

        while next < target_week {
            if days.contains(&next.weekday()) {
                return next;
            }
            next = next + Duration::days(1);
        }

        target_week
    }

    fn next_monthly(
        &self,
        current: DateTime<Utc>,
        interval: u32,
        day_of_month: u8,
    ) -> DateTime<Utc> {
        let mut year = current.year();
        let mut month = current.month() + interval;

        while month > 12 {
            year += 1;
            month -= 12;
        }

        current
            .with_year(year)
            .and_then(|d| d.with_month(month))
            .and_then(|d| d.with_day(day_of_month as u32))
            .unwrap_or(current + Duration::days(30))
    }

    fn next_yearly(
        &self,
        current: DateTime<Utc>,
        interval: u32,
        month: u8,
        day: u8,
    ) -> DateTime<Utc> {
        let year = current.year() + interval as i32;

        current
            .with_year(year)
            .and_then(|d| d.with_month(month as u32))
            .and_then(|d| d.with_day(day as u32))
            .unwrap_or(current + Duration::days(365))
    }

    fn is_exception(&self, date: DateTime<Utc>) -> bool {
        self.exceptions
            .iter()
            .any(|&exception| exception.date_naive() == date.date_naive())
    }
}
