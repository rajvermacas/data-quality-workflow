# N8N Data Quality Alert to GitLab Issue Workflow - Product Requirements Document

**Document Version**: 1.0  
**Date**: June 29, 2025  
**Author**: Design Discussion Session  

## Executive Summary

This PRD defines the requirements for an automated n8n workflow that processes natural language data quality alerts, transforms them into structured GitLab issues using Google Gemini AI, and notifies relevant stakeholders via email.

## Problem Statement

Currently, data quality issues require manual intervention to:
- Parse unstructured alert messages
- Format them into proper GitLab issues
- Assign appropriate severity and labels
- Notify the right team members

This manual process introduces delays and inconsistencies in issue tracking and resolution.

## Objectives and Success Metrics

### Primary Objectives
- Automate the conversion of natural language alerts to structured GitLab issues
- Reduce manual effort in issue creation and assignment
- Ensure consistent formatting and categorization of data quality issues
- Provide timely notifications to stakeholders

### Success Metrics
- 100% automated processing of webhook alerts
- Consistent GitLab issue format and metadata assignment
- Reliable email notifications to assignees and administrators
- Zero manual intervention required for standard alert processing

## User Stories and Use Cases

### User Story 1: Data Quality Alert Processing
**As a** data monitoring system  
**I want to** send natural language alerts to the n8n workflow  
**So that** issues are automatically created in GitLab with proper formatting and assignment

### User Story 2: Issue Assignment and Notification
**As a** team lead  
**I want to** receive email notifications when data quality issues are created  
**So that** I can quickly respond to critical problems

### User Story 3: Contextual Issue Creation
**As a** developer  
**I want** GitLab issues to have appropriate severity levels and labels  
**So that** I can prioritize and categorize work effectively

## Functional Requirements

### FR1: Webhook Reception
- **Description**: Accept HTTP POST requests with natural language alert data
- **Input Format**: `{"message": "Natural language description including assignee email"}`
- **Example**: `{"message": "Database connection timeout in prod environment, affecting user logins. Assignee would be lubbapark1@gmail.com"}`
- **Authentication**: None required
- **Response**: Standard HTTP status codes

### FR2: AI-Powered Issue Formatting
- **Description**: Use Google Gemini 2.5 Flash to transform natural language input into structured GitLab issue format
- **Input**: Raw message from webhook
- **Processing**: Extract and structure the following components:
  - **Title**: Concise, actionable issue title
  - **Description**: Detailed description with context and technical details
  - **Severity**: Automated classification (Critical, High, Medium, Low)
  - **Labels**: Context-based labels (e.g., "database", "production", "performance")
  - **Assignee**: Extract email address from message text
- **Output**: Structured JSON for GitLab issue creation

### FR3: GitLab Issue Creation
- **Description**: Create issues in the specified GitLab project
- **Target Project**: `https://gitlab.com/my-group-name2452611/data-quality`
- **Project Owner**: `my-group-name2452611`
- **Project Name**: `data-quality`
- **Issue Fields**:
  - Title (from AI processing)
  - Description (from AI processing)
  - Labels (from AI processing)
  - Assignee (if email provided and valid GitLab user)

### FR4: Email Notification System
- **Description**: Send HTML email notifications to stakeholders
- **Primary Recipient**: `mrinalrajubereats1@gmail.com` (always included)
- **Secondary Recipient**: Assignee email (if present in original message)
- **Email Content**:
  - Issue title
  - Issue description (truncated if necessary)
  - Severity level
  - Direct link to created GitLab issue
  - Labels assigned
- **Format**: HTML template with clean, readable formatting

## Non-Functional Requirements

### NFR1: Performance
- Workflow completion time: < 30 seconds for standard alerts
- API response time: < 5 seconds for webhook acknowledgment

### NFR2: Reliability
- System uptime: 99.5% availability
- Error handling: Graceful failure with error notifications
- No input validation requirements (best-effort processing)

### NFR3: Scalability
- Support for concurrent webhook requests
- Handle varying message lengths and complexity

### NFR4: Security
- No authentication required for webhook (as specified)
- Secure API key management for Gemini integration
- GitLab token security for issue creation

## Technical Constraints

### Integration Requirements
- **n8n Platform**: Must be compatible with n8n workflow engine
- **Google Gemini API**: Requires valid API key for Gemini 2.5 Flash
- **GitLab API**: Requires GitLab access token with issue creation permissions
- **Email Service**: Compatible with n8n email sending capabilities

### Data Processing Constraints
- **Input Format**: Single JSON message field with natural language content
- **AI Processing**: Dependent on Gemini API availability and rate limits
- **Email Extraction**: Regex-based extraction from natural language text
- **Error Handling**: Display errors without stopping workflow execution

## Workflow Architecture

### Node 1: Webhook Receiver
- **Type**: n8n-nodes-base.webhook
- **Configuration**:
  - Path: `data-quality-alerts`
  - Method: POST
  - Authentication: None
- **Output**: Raw JSON message

### Node 2: Gemini AI Processor
- **Type**: n8n-nodes-base.httpRequest (to Gemini API)
- **Configuration**:
  - URL: Google Gemini API endpoint
  - Method: POST
  - Authentication: API Key
- **Prompt Template**:
```
You are a technical issue formatter. Transform the following natural language alert into a structured GitLab issue format.

Input: {webhook_message}

Please extract and format:
1. Title: Create a concise, actionable title (max 80 chars)
2. Description: Detailed technical description with context
3. Severity: Classify as Critical, High, Medium, or Low based on impact
4. Labels: Suggest 2-3 relevant labels based on content (e.g., database, production, performance)
5. Assignee: Extract email address if mentioned in the text

Return as JSON:
{
  "title": "...",
  "description": "...",
  "severity": "...",
  "labels": [...],
  "assignee": "email@domain.com or null"
}
```

### Node 3: GitLab Issue Creator
- **Type**: n8n-nodes-base.gitlab
- **Configuration**:
  - Resource: issue
  - Operation: create
  - Project Owner: `my-group-name2452611`
  - Project Name: `data-quality`
  - Title: `={{$json.title}}`
  - Body: `={{$json.description}}`
  - Labels: `={{$json.labels}}`
  - Assignee: `={{$json.assignee}}`

### Node 4: Email Notification
- **Type**: n8n-nodes-base.emailSend
- **Configuration**:
  - To: `mrinalrajubereats1@gmail.com,{{$json.assignee}}`
  - Subject: `Data Quality Alert: {{$json.title}}`
  - HTML Template: Custom HTML with issue details and GitLab link

## Dependencies

### External Services
- **Google Gemini API**: For AI-powered text processing
- **GitLab API**: For issue creation and management
- **Email Service**: For notification delivery
- **n8n Platform**: For workflow orchestration

### API Keys and Tokens
- Google Gemini API key (user-provided)
- GitLab access token with project permissions
- Email service credentials (if required)

## Timeline and Milestones

### Phase 1: Core Workflow Setup (Week 1)
- Configure webhook node
- Set up basic HTTP request to Gemini API
- Test end-to-end connectivity

### Phase 2: AI Integration (Week 2)
- Implement Gemini prompt engineering
- Test various input scenarios
- Refine output formatting

### Phase 3: GitLab Integration (Week 3)
- Configure GitLab issue creation
- Test assignee assignment logic
- Validate label and severity assignment

### Phase 4: Email Notification (Week 4)
- Design HTML email template
- Implement recipient logic
- Test notification delivery

### Phase 5: Testing and Refinement (Week 5)
- End-to-end testing with various scenarios
- Error handling validation
- Performance optimization

## Risk Assessment

### High Risk
- **Gemini API Rate Limits**: May impact processing during high alert volumes
- **Mitigation**: Implement retry logic and queue management

### Medium Risk
- **Email Extraction Accuracy**: Natural language processing may miss or misidentify assignee emails
- **Mitigation**: Provide fallback to admin notification only

### Low Risk
- **GitLab API Changes**: API deprecation could affect issue creation
- **Mitigation**: Monitor GitLab API versioning and updates

## Acceptance Criteria

### Webhook Processing
- ✅ Accepts POST requests with JSON message payload
- ✅ Processes natural language input without validation
- ✅ Returns appropriate HTTP status codes

### AI Formatting
- ✅ Generates structured GitLab issue format from natural language
- ✅ Assigns appropriate severity levels (Critical, High, Medium, Low)
- ✅ Suggests contextual labels based on content
- ✅ Extracts assignee email addresses when present

### GitLab Integration
- ✅ Creates issues in specified project
- ✅ Populates all required fields (title, description, labels)
- ✅ Assigns issues to valid GitLab users when email provided

### Email Notifications
- ✅ Always sends to admin email (`mrinalrajubereats1@gmail.com`)
- ✅ Includes assignee email when present in original message
- ✅ Contains all relevant issue information and GitLab link
- ✅ Uses clean HTML formatting

### Error Handling
- ✅ Continues workflow execution despite individual node failures
- ✅ Provides meaningful error messages for debugging
- ✅ Maintains workflow stability under various input conditions

---

**End of Document**

This PRD serves as the comprehensive specification for implementing the N8N Data Quality Alert to GitLab Issue workflow. All stakeholders should review and approve before implementation begins.