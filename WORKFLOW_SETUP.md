# Data Quality Alert to GitLab Issue Workflow - Setup Guide

## Overview
This n8n workflow automatically processes natural language data quality alerts, transforms them into structured GitLab issues using Google Gemini AI, and sends email notifications to stakeholders.

## Workflow File
- **File**: `data-quality-alert-workflow.json`
- **Nodes**: 5 nodes (Webhook → Gemini AI → Response Parser → GitLab → Email)

## Import Instructions

### 1. Import the Workflow
1. Open your n8n instance
2. Click the **three dots (⋯)** in the top navigation
3. Select **"Import from File"**
4. Upload the `data-quality-alert-workflow.json` file
5. The workflow will appear in your workflows list

## Required Credentials Setup

### 1. Google AI API Key
**Credential Type**: `Google AI`
**Name**: `Google AI API`

**Setup Steps**:
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key
3. In n8n, create a new credential:
   - Type: **Google AI**
   - Name: `Google AI API`
   - API Key: `[Your Google AI API Key]`
   - API Host: `https://generativelanguage.googleapis.com` (default)

### 2. GitLab API Token
**Credential Type**: `GitLab API`
**Name**: `GitLab API Token`

**Setup Steps**:
1. Go to GitLab → Settings → Access Tokens
2. Create a personal access token with `api` scope
3. In n8n, create a new credential:
   - Type: **GitLab API**
   - Name: `GitLab API Token`
   - GitLab Server: `https://gitlab.com`
   - Access Token: `[Your GitLab Token]`

### 3. SMTP Email Settings
**Credential Type**: `SMTP`
**Name**: `SMTP Email Settings`

**Setup Steps**:
1. Configure your email provider SMTP settings
2. In n8n, create a new credential:
   - Type: **SMTP**
   - Name: `SMTP Email Settings`
   - Host: `[Your SMTP Host]` (e.g., smtp.gmail.com)
   - Port: `[Port Number]` (e.g., 587 for TLS, 465 for SSL)
   - User: `[Your Email Address]`
   - Password: `[Your Email Password/App Password]`

## Workflow Configuration

### Node Details

#### 1. Data Quality Alert Webhook
- **Path**: `/data-quality-alerts`
- **Method**: POST
- **Authentication**: None
- **Expected Input**: `{"message": "Natural language alert with optional assignee email"}`

#### 2. Gemini AI Processor
- **Node Type**: HTTP Request (for Google Gemini API)
- **Model**: `gemini-1.5-flash`
- **Endpoint**: `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent`
- **Function**: Transforms natural language to structured GitLab format using direct API calls

#### 3. Parse Gemini Response
- **Type**: Function Node
- **Purpose**: Extracts and validates JSON response from Gemini HTTP API
- **Error Handling**: Multiple fallback layers for robust parsing
- **Features**: Handles both clean JSON and markdown-formatted responses

#### 4. Create GitLab Issue
- **Project**: `my-group-name2452611/data-quality`
- **Fields**: Title, Description, Labels, Assignee
- **Auto-adds**: Severity labels and original message context

#### 5. Send Email Notification
- **Recipients**: 
  - Primary: `mrinalrajubereats1@gmail.com` (always)
  - Secondary: Assignee email (if present)
- **Format**: HTML with styled template
- **Content**: Issue details, severity, labels, GitLab link

## Testing the Workflow

### 1. Activate the Workflow
1. Open the imported workflow
2. Click **"Activate"** in the top right
3. The webhook URL will be generated

### 2. Test Webhook Call
Send a POST request to your webhook URL:
```bash
curl -X POST "https://your-n8n-instance/webhook/data-quality-alerts" \
  -H "Content-Type: application/json" \
  -d '{"message": "Database connection timeout in prod environment, affecting user logins. Assignee would be lubbapark1@gmail.com"}'
```

### 3. Expected Results
1. ✅ Webhook receives the alert
2. ✅ Gemini AI processes and structures the alert
3. ✅ GitLab issue is created with proper formatting
4. ✅ Email notifications sent to admin and assignee

## Customization Options

### Modify Email Recipients
To change the primary recipient from `mrinalrajubereats1@gmail.com`:
1. Edit the **Send Email Notification** node
2. Update the `toEmail` parameter

### Update GitLab Project
To target a different GitLab project:
1. Edit the **Create GitLab Issue** node
2. Update `projectOwner` and `projectName` parameters

### Customize Gemini Prompt
To modify how issues are formatted:
1. Edit the **Gemini AI Processor** node
2. Update the `jsonBody` prompt template

### Email Template Styling
To customize email appearance:
1. Edit the **Send Email Notification** node
2. Modify the HTML template in the `html` parameter

## Troubleshooting

### Common Issues

#### 1. Google AI API Errors
- **Error**: Authentication failed or 400 Bad Request
- **Solution**: Verify Google AI API key in credentials and check quota limits
- **Test**: Use curl to test API access: `curl -H "Content-Type: application/json" -d '{"contents":[{"parts":[{"text":"test"}]}]}' "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=YOUR_API_KEY"`

#### 2. GitLab Authentication
- **Error**: 401 Unauthorized
- **Solution**: Check token permissions and project access
- **Required Scopes**: `api`, `write_repository`

#### 3. Email Delivery Issues
- **Error**: SMTP connection failed
- **Solution**: Verify SMTP settings and authentication
- **Gmail**: Use App Passwords instead of regular password

#### 4. Workflow Execution Errors
- **Check**: Execution log for detailed error messages
- **Debug**: Test each node individually
- **Reset**: Clear workflow data and re-run

## Security Considerations

1. **API Keys**: Store securely in n8n credentials, never hardcode
2. **Webhook**: Consider adding authentication if needed
3. **Email**: Don't include sensitive data in email notifications
4. **GitLab**: Use project-specific tokens with minimal permissions

## Support

For issues with:
- **n8n**: Check [n8n Community](https://community.n8n.io/)
- **Google AI API**: Review [Google AI Documentation](https://ai.google.dev/)
- **GitLab API**: See [GitLab API Docs](https://docs.gitlab.com/ee/api/)
- **LangChain Nodes**: Check [n8n LangChain Documentation](https://docs.n8n.io/integrations/builtin/cluster-nodes/)

---

**Created**: June 29, 2025  
**Version**: 1.0  
**Compatible with**: n8n v1.0+