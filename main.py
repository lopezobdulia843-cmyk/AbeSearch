from flask import Flask, request, Response
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

app = Flask(__name__)

# --- THE DESIGN ---
HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AbeSearch</title>
    <style>
        body { background: #121212; color: white; font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        h1 { font-size: 3rem; margin-bottom: 20px; color: #00ff88; text-shadow: 0 0 10px #00ff88; }
        .search-box { width: 80%; max-width: 600px; display: flex; gap: 10px; }
        input { flex: 1; padding: 15px; border-radius: 25px; border: 1px solid #333; background: #1e1e1e; color: white; outline: none; border: 1px solid #00ff88; }
        button { padding: 15px 25px; border-radius: 25px; border: none; background: #00ff88; color: black; font-weight: bold; cursor: pointer; }
        p { color: #888; margin-top: 20px; font-size: 0.9rem; }
    </style>
</head>
<body>
    <h1>AbeSearch</h1>
    <form action="/view" method="get" class="search-box">
        <input type="text" name="url" placeholder="Enter URL (e.g. https://wikipedia.org)" required>
        <button type="submit">Go</button>
    </form>
    <p>Stealth Mode: Active | Developed by Abe</p>
</body>
</html>
"""

# --- THE LOGIC ---
@app.route('/')
def home():
    return HOME_HTML

@app.route('/view')
def proxy():
    target_url = request.args.get('url')
    if not target_url: return "No URL provided", 400
    if not target_url.startswith('http'): target_url = 'https://' + target_url

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        resp = requests.get(target_url, headers=headers, timeout=10)
        
        # If it's a webpage, fix the links so they stay in AbeSearch
        if "text/html" in resp.headers.get("Content-Type", ""):
            soup = BeautifulSoup(resp.content, 'html.parser')
            for tag in soup.find_all(['a', 'form', 'link', 'script', 'img']):
                attr = 'href' if tag.name in ['a', 'link'] else 'src'
                if tag.name == 'form': attr = 'action'
                if tag.has_attr(attr):
                    tag[attr] = f"/view?url={urljoin(target_url, tag[attr])}"
            content = soup.prettify()
        else:
            content = resp.content

        excluded = ['content-encoding', 'content-length', 'transfer-encoding', 'connection', 'x-frame-options', 'content-security-policy']
        headers = [(n, v) for (n, v) in resp.raw.headers.items() if n.lower() not in excluded]
        return Response(content, resp.status_code, headers)
    except Exception as e:
        return f"Proxy Error: {e}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
