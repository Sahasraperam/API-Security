from flask import Flask, request, render_template
from flask_cors import CORS
import requests
from urllib.parse import urlparse
import random
import string

app = Flask(__name__)
CORS(app)

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def check_cors(url):
    try:
        response = requests.options(url, headers={"Origin": "https://example.com"})
        if "Access-Control-Allow-Origin" in response.headers:
            return "CORS is enabled and may be misconfigured"
        return "CORS is not enabled"
    except requests.RequestException:
        return "Unable to check CORS"

def check_ssl(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme == "https"

def check_auth(url, auth_type, username, password):
    try:
        if auth_type == "basic":
            response = requests.get(url, auth=(username, password))
        elif auth_type == "bearer":
            headers = {"Authorization": f"Bearer {password}"}
            response = requests.get(url, headers=headers)
        else:
            return "Unsupported authentication type"

        if response.status_code == 200:
            return "Authentication successful"
        elif response.status_code == 401:
            return "Authentication failed"
        else:
            return f"Unexpected status code: {response.status_code}"
    except requests.RequestException as e:
        return f"Error: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        auth_type = request.form.get('auth_type')
        username = request.form.get('username')
        password = request.form.get('password')

        if not url:
            return render_template('index.html', error="URL is required")

        results = {
            "cors": check_cors(url),
            "ssl": "SSL is enabled" if check_ssl(url) else "SSL is not enabled",
            "auth": check_auth(url, auth_type, username, password) if auth_type else "Authentication not tested"
        }

        # Generate random data for the hacker interface
        random_data = {
            "ip_address": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "port_scan": [random.randint(1, 65535) for _ in range(5)],
            "encryption": generate_random_string(32),
            "packets": random.randint(1000, 9999)
        }

        return render_template('index.html', results=results, random_data=random_data)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

print("Hacker API Security Scanner is running. Access it at http://127.0.0.1:5000")