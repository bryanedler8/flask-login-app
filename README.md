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


You're right, let me trim that down significantly. Here's a much shorter version:

---
## Demo Video

🎥 [Watch Demo Video](https://youtu.be/lcJffrhx_a0)

---


### What I Learned
- Writing effective KQL queries requires understanding both log structure and syntax.
- Time binning (`bin(TimeGenerated, 5m)`) is essential for spotting attack patterns.
- Regex extraction (`extract()`) is a practical skill for pulling data from free-text logs.

### Challenges I Faced
- Getting the regex pattern exactly right for the log format took trial and error.
- The `bin()` function groups time into fixed intervals, which can miss attacks that span across boundaries.
- Without IP tracking, the query can't distinguish between one user mistyping vs. a distributed attack.




---



## KQL Query for Failed Login Detection

```kusto
AppServiceConsoleLogs
| where ResultDescription contains "FAILED login attempt"
| extend Username = extract("Username: ([^,]+)", 1, ResultDescription)
| summarize FailedAttempts = count() by Username, bin(TimeGenerated, 5m)
| where FailedAttempts > 5

This detects potential brute-force attacks by flagging any username with 6+ failed login attempts within a 5-minute window.
