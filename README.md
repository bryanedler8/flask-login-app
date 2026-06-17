# CST8919 Lab 2: Flask Login App with Azure Monitoring

## Overview
This Flask application demonstrates a login endpoint with comprehensive logging for security monitoring. It's designed to be deployed on Azure App Service with Azure Monitor integration for log analysis and alerting.

## Features
- **Login Endpoint**: `/login` with username/password authentication
- **Logging**: Logs both successful and failed login attempts
- **Azure Integration**: Console logging for Azure Monitor capture
- **Health Check**: `/health` endpoint for Azure App Service monitoring

## Local Development

### Prerequisites
- Python 3.8+
- pip

### Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd flask-login-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

## KQL Query for Failed Login Detection

```kusto
AppServiceConsoleLogs
| where TimeGenerated > ago(15m)
| where ResultDescription contains "FAILED login attempt"
| extend Username = extract("Username: ([^,]+)", 1, ResultDescription)
| summarize FailedAttempts = count() by Username, bin(TimeGenerated, 5m)
| where FailedAttempts > 5
