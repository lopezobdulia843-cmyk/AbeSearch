from flask import Flask, request, Response, render_template_string
import requests
import os

app = Flask(__name__)

# The Arcade-style interface
HTML_LAYOUT = """
<!DOCTYPE html>
<html>
<head>
    <title>AbeSearch | OS</title>
    <style>
        body { background: #000; color: #00ff88; font-family: monospace; margin: 0; }
        .nav { background: #111; padding: 10px; display: flex; gap: 10px; border-bottom: 2px solid #00ff88; }
        input { flex: 1; background: #000; border: 1px solid #00ff88; color: #00ff88; padding: 10px; }
        button { background: #00ff88; border: none; padding: 10px 20px; cursor: pointer; font-weight: bold; }
        iframe { width: 100%; height: calc(100vh - 60px); border: none; background: white; }
    </style>
</head>
<body>
    <div class="nav">
        <input type="text" id="url" placeholder="Enter URL (e.g. https://wikipedia.org)">
        <button onclick="go()">EXECUTE</button>
    </div>
    <iframe id="view"></iframe>
    <script>
        function go() {
            let u = document.getElementById('url').value;
            if(!u.startsWith('http')) u = 'https://' + u;
            // This sends the request to our /proxy route
            document.getElementById('view').src = '/proxy?url=' + encodeURIComponent(u);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT)

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url: return "No URL", 400
    
    try:
        # Your server goes and gets the site
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        # We create a response and DELETE the security headers that block the iPad
        out = Response(res.content, res.status_code)
        
        # Strip out the "Don't show in frame" rules
        for k, v in res.headers.items():
            if k.lower() not in ['x-frame-options', 'content-security-policy', 'frame-options']:
                out.headers[k] = v
        return out
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
