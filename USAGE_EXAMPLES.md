# Usage Examples - Data Quality Alert Workflow

## Testing Your Workflow

### 1. Using the Test Script (Recommended)

After setting up your workflow, use the provided Python test script:

```bash
# Install required dependency
pip install requests

# Run all test cases
python scripts/test_webhook.py "https://your-n8n-instance/webhook/data-quality-alerts"

# Run a specific test case
python scripts/test_webhook.py "https://your-n8n-instance/webhook/data-quality-alerts" --test-case 1

# Run with custom delay between tests
python scripts/test_webhook.py "https://your-n8n-instance/webhook/data-quality-alerts" --delay 10
```

### 2. Manual cURL Testing

```bash
# Basic database issue with assignee
curl -X POST "https://your-n8n-instance/webhook/data-quality-alerts" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Database connection timeout in prod environment, affecting user logins. Assignee would be lubbapark1@gmail.com"
  }'

# Performance issue without assignee
curl -X POST "https://your-n8n-instance/webhook/data-quality-alerts" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "API response times have increased by 300% over the last hour. Users are experiencing slow page loads and timeouts."
  }'

# Security alert
curl -X POST "https://your-n8n-instance/webhook/data-quality-alerts" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Unusual login attempts detected from multiple IP addresses. Security team member alex.security@company.com needs to investigate immediately."
  }'
```

### 3. JavaScript/Node.js Example

```javascript
const axios = require('axios');

const webhookUrl = 'https://your-n8n-instance/webhook/data-quality-alerts';

async function sendAlert(message) {
  try {
    const response = await axios.post(webhookUrl, {
      message: message
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    console.log('Alert sent successfully:', response.status);
    return response.data;
  } catch (error) {
    console.error('Failed to send alert:', error.message);
    throw error;
  }
}

// Example usage
sendAlert('Database connection timeout in prod environment, affecting user logins. Assignee would be lubbapark1@gmail.com');
```

### 4. Python Integration Example

```python
import requests
import json

def send_data_quality_alert(message, webhook_url):
    """Send a data quality alert to the n8n workflow"""
    payload = {"message": message}
    
    try:
        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Alert sent successfully")
            return True
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send alert: {e}")
        return False

# Example usage
webhook_url = "https://your-n8n-instance/webhook/data-quality-alerts"
message = "ETL pipeline failed during customer data migration. 10,000 records not processed. Data integrity check required. Assign to data engineering team lead robert.data@company.com"

send_data_quality_alert(message, webhook_url)
```

## Expected Workflow Output

### 1. GitLab Issue Creation
The workflow will create a GitLab issue with:
- **Title**: AI-generated concise title (max 80 chars)
- **Description**: Structured description with context
- **Labels**: Auto-generated labels based on content + severity
- **Assignee**: Extracted email (if valid GitLab user)

Example GitLab issue:
```
Title: Database Connection Timeout - Production Environment

Description:
Critical database connection timeout issue affecting user login functionality in production environment.

**Severity:** Critical

**Original Alert:**
Database connection timeout in prod environment, affecting user logins. Assignee would be lubbapark1@gmail.com

Labels: database, production, timeout, critical
Assignee: lubbapark1@gmail.com
```

### 2. Email Notification
Recipients will receive an HTML-formatted email containing:
- Issue title and severity (color-coded)
- Full description
- Assigned labels
- Original alert message
- Direct link to GitLab issue
- Professional styling

## Integration Patterns

### 1. Monitoring System Integration
```bash
# From Prometheus AlertManager
curl -X POST "https://your-n8n-instance/webhook/data-quality-alerts" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Alert: {{ $labels.alertname }} - {{ $annotations.summary }}. Contact: {{ $labels.contact_email }}"
  }'
```

### 2. Application Error Handler
```python
def handle_critical_error(error_msg, assignee_email=None):
    message = f"Critical application error: {error_msg}"
    if assignee_email:
        message += f" Assignee would be {assignee_email}"
    
    send_data_quality_alert(message, WEBHOOK_URL)
```

### 3. Data Pipeline Integration
```python
def report_pipeline_failure(pipeline_name, error_details, data_engineer_email):
    message = f"""
    Data pipeline '{pipeline_name}' failed with error: {error_details}
    Data integrity may be compromised. Immediate investigation required.
    Assign to data engineer {data_engineer_email}
    """
    
    send_data_quality_alert(message.strip(), WEBHOOK_URL)
```

## Message Format Best Practices

### ✅ Good Examples
- Include specific details about the issue
- Mention impact on users/systems
- Provide assignee email when known
- Use clear, descriptive language

### ❌ Avoid
- Vague messages like "something is wrong"
- Technical jargon without context
- Missing critical information
- Overly long messages (>500 words)

### Message Template
```
[Issue Type]: [Brief Description]
Impact: [Who/what is affected]
Environment: [production/staging/development]
[Optional: Assignee would be email@domain.com]
[Optional: Additional context or error details]
```

## Monitoring and Debugging

### Check Workflow Status
- Monitor n8n execution log for errors
- Verify GitLab issues are being created
- Confirm email notifications are sent
- Review Gemini API usage and quotas

### Common Troubleshooting
- **No GitLab issue created**: Check GitLab API token permissions
- **No email sent**: Verify SMTP credentials and recipient addresses
- **AI processing fails**: Check Gemini API key and quota limits
- **Webhook not triggering**: Verify webhook URL and POST method

---

**Tip**: Start with the test script to validate your setup before integrating with production systems.