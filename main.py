from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

# The Home Page Design
HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AbeSearch</title>
    <style>
        body { background: #121212; color: white; font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        h1 { font-size: 3rem; margin-bottom: 20px; color: #00ff88; text-shadow: 0 0 10px #00ff88; }
        .search-box { width: 80%; max-width: 600px; display: flex; gap: 10px; }
        input { flex: 1; padding: 15px; border-radius: 25px; border: 1px solid #333; background: #1e1e1e; color: white; outline: none; }
        button { padding: 15px 25px; border-radius: 25px; border: none; background: #00ff88; color: black; font-weight: bold; cursor: pointer; }
        button:hover { background: #00cc6e; }
        p { color: #888; margin-top: 20px; font-size: 0.9rem; }
    </style>
</head>
<body>
    <h1>AbeSearch</h1>
    <form action="/view" method="get" class="search-box">
        <input type="text" name="url" placeholder="Paste a link here (e.g. https://wikipedia.org)" required>
        <button type="submit">Go</button>
    </form>
    <p>Developed by Abraham | Stealth Mode Active</p>
</body>
</html>
"""

@app.route('/')
def home():
    return HOME_HTML

@app.route('/view')
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return "Please provide a URL", 400
    
    if not target_url.startswith('http'):
        target_url = 'https://' + target_url

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        resp = requests.get(target_url, headers=headers, timeout=10)
        
        # This keeps the site from knowing it's in a frame
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection', 'x-frame-options', 'content-security-policy']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]

        return Response(resp.content, resp.status_code, headers)
    except Exception as e:
        return f"Error connecting to site: {e}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
