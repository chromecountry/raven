# Time Window Feature for Email Processing

## Overview

The Raven receipt processing system now supports time window constraints when processing emails. This allows you to specify a date range to limit which emails are processed, making it easier to process emails from specific time periods.

## Usage

### Command Line Interface

```bash
# Process all unread emails
./app.sh process-emails

# Process emails from a specific start date
./app.sh process-emails 2024-01-01

# Process emails within a date range
./app.sh process-emails 2024-01-01 2024-01-31

# Process emails with environment specification
./app.sh --env dev process-emails 2024-01-01 2024-01-31
```

### Python Script

```python
# Process all unread emails
python src/ui/main.py process-emails

# Process emails from a specific start date
python src/ui/main.py process-emails 2024-01-01

# Process emails within a date range
python src/ui/main.py process-emails 2024-01-01 2024-01-31
```

### API Endpoints

#### Process Emails with Time Window

```bash
# Process all unread emails
curl -X POST http://localhost:5000/api/process-emails

# Process emails from a specific start date
curl -X POST http://localhost:5000/api/process-emails \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2024-01-01"}'

# Process emails within a date range
curl -X POST http://localhost:5000/api/process-emails \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2024-01-01", "end_date": "2024-01-31"}'
```

#### Web Interface

```bash
# Process all unread emails
curl -X POST http://localhost:5000/process-emails

# Process emails from a specific start date
curl -X POST http://localhost:5000/process-emails \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2024-01-01"}'

# Process emails within a date range
curl -X POST http://localhost:5000/process-emails \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2024-01-01", "end_date": "2024-01-31"}'
```

## Date Format

All dates must be provided in ISO format: `YYYY-MM-DD`

Examples:
- `2024-01-01` - January 1, 2024
- `2024-12-31` - December 31, 2024
- `2023-06-15` - June 15, 2023

## How It Works

1. **IMAP Search Criteria**: The system uses IMAP search criteria to filter emails at the server level:
   - `SINCE date` - Only emails received on or after the specified date
   - `BEFORE date` - Only emails received before the specified date

2. **Email Date Parsing**: For additional accuracy, the system also parses the email's `Date` header to ensure emails fall within the specified range.

3. **Date Range Logic**:
   - If only `start_date` is provided: Process emails from that date onwards
   - If only `end_date` is provided: Process emails up to (but not including) that date
   - If both dates are provided: Process emails within the inclusive range

## Examples

### Process Recent Emails

```bash
# Process emails from the last week
./app.sh process-emails 2024-01-08 2024-01-15
```

### Process Historical Emails

```bash
# Process emails from a specific month
./app.sh process-emails 2023-12-01 2023-12-31
```

### Process Emails from a Specific Period

```bash
# Process emails from a specific quarter
./app.sh process-emails 2024-01-01 2024-03-31
```

## Response Format

When using the API endpoints, the response includes information about the time window used:

```json
{
  "success": true,
  "processed_count": 5,
  "results": [
    {
      "filename": "receipt.pdf",
      "merchant": "Walmart",
      "amount": "45.67",
      "date": "01/15/24"
    }
  ],
  "time_window": {
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
  }
}
```

## Error Handling

- **Invalid Date Format**: Returns 400 error with message "Invalid start_date/end_date format. Use YYYY-MM-DD"
- **Date Parsing Errors**: Gracefully handles malformed email dates by skipping those emails
- **Connection Errors**: Standard error handling for IMAP connection issues

## Benefits

1. **Performance**: Reduces the number of emails to process, improving performance
2. **Targeted Processing**: Process specific time periods for reconciliation or analysis
3. **Incremental Processing**: Process emails in batches by date ranges
4. **Historical Analysis**: Process historical emails without affecting current processing

## Notes

- The time window feature works with all existing email processing functionality
- Date filtering is applied at both the IMAP server level and email header level for accuracy
- The feature is backward compatible - existing scripts without date parameters continue to work
- Time zones are handled according to the email server's timezone settings 