import logging
import re
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Configure logging to output to console (stdout) for Azure App Service
# This is critical for Azure Monitor to capture logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Simple in-memory user database (for demonstration purposes)
USERS = {
    "admin": "supersecret",
    "alice": "password123",
    "bob": "securepass"
}

# HTML template for the login page (optional - for browser testing)
LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Login Demo</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 20px; border-radius: 8px; }
        input { width: 100%; padding: 10px; margin: 5px 0; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #0078d4; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #005a9e; }
        .error { color: red; }
        .success { color: green; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Login Page</h2>
        {% if message %}
            <p class="{{ status }}">{{ message }}</p>
        {% endif %}
        <form method="POST" action="/login">
            <div>
                <label>Username:</label>
                <input type="text" name="username" required>
            </div>
            <div>
                <label>Password:</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
        <p style="margin-top: 20px; font-size: 12px; color: #666;">
            <strong>Test Credentials:</strong><br>
            admin / supersecret<br>
            alice / password123<br>
            bob / securepass
        </p>
    </div>
</body>
</html>
"""


@app.route('/')
def home():
    """Home page with login form"""
    return render_template_string(LOGIN_PAGE)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login endpoint that logs attempts.
    Supports both GET (query parameters) and POST (form data).
    This flexibility makes testing easier with .http files and browsers.
    """
    
    # Extract username and password from request
    if request.method == 'GET':
        username = request.args.get('username', '')
        password = request.args.get('password', '')
    else:  # POST
        username = request.form.get('username', '')
        password = request.form.get('password', '')
    
    # Validate input
    if not username or not password:
        error_msg = "Missing username or password"
        logging.warning(f"Login attempt with missing credentials - IP: {request.remote_addr}")
        
        if request.method == 'GET':
            return jsonify({"error": error_msg}), 400
        else:
            return render_template_string(
                LOGIN_PAGE, 
                message=error_msg, 
                status="error"
            ), 400
    
    # Check credentials against our user database
    if username in USERS and USERS[username] == password:
        # SUCCESSFUL LOGIN
        success_msg = f"User {username} logged in successfully"
        logging.info(f"SUCCESSFUL login attempt - Username: {username}, IP: {request.remote_addr}")
        
        if request.method == 'GET':
            return jsonify({
                "status": "success",
                "message": success_msg,
                "username": username
            }), 200
        else:
            return render_template_string(
                LOGIN_PAGE, 
                message=f"✅ {success_msg}", 
                status="success"
            ), 200
    else:
        # FAILED LOGIN
        # Extract username for logging, but mask if it doesn't exist
        failed_msg = f"FAILED login attempt - Username: {username}, IP: {request.remote_addr}"
        logging.warning(failed_msg)
        
        if request.method == 'GET':
            return jsonify({
                "status": "failed",
                "message": "Invalid username or password",
                "username": username
            }), 401
        else:
            return render_template_string(
                LOGIN_PAGE, 
                message="❌ Invalid username or password", 
                status="error"
            ), 401


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Azure App Service"""
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    # Run the app
    # In production, Azure App Service uses Gunicorn or similar WSGI server
    app.run(host='0.0.0.0', port=5000, debug=False)