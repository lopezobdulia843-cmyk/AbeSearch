from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>AbeSearch is Live</h1><p>Type /view?url=https://google.com at the end of the URL!</p>"

@app.route('/view')
def proxy():
    url = request.args.get('url')
    if not url:
        return "No URL provided!", 400
    
    # We pretend to be a normal Google Chrome browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Fetch the site
        resp = requests.get(url, headers=headers, timeout=10)
        
        # We strip out the 'Security Blocks' that cause the black/blank screen
        excluded_headers = [
            'content-encoding', 'content-length', 'transfer-encoding', 'connection',
            'x-frame-options', 'content-security-policy', 'strict-transport-security'
        ]
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]

        return Response(resp.content, resp.status_code, headers)
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
