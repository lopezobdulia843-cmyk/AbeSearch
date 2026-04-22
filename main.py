from flask import Flask, request, Response, render_template_string
import requests
from bs4 import BeautifulSoup # We use this to 'read' the website
from urllib.parse import urljoin, urlparse
import os

app = Flask(__name__)

# ... (Keep your HOME_HTML from before here) ...

@app.route('/view')
def proxy():
    target_url = request.args.get('url')
    if not target_url: return "No URL", 400
    if not target_url.startswith('http'): target_url = 'https://' + target_url

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(target_url, headers=headers, timeout=10)
        
        # If it's a website (HTML), we need to fix the links
        if "text/html" in resp.headers.get("Content-Type", ""):
            soup = BeautifulSoup(resp.content, 'html.parser')
            
            # This is the "Magic": it finds every link and forces it through AbeSearch
            for tag in soup.find_all(['a', 'form', 'link', 'script', 'img']):
                attr = 'href' if tag.name in ['a', 'link'] else 'src'
                if tag.name == 'form': attr = 'action'
                
                if tag.has_attr(attr):
                    old_url = tag[attr]
                    # Make the link absolute (complete)
                    full_url = urljoin(target_url, old_url)
                    # Redirect the link back through your proxy
                    tag[attr] = f"/view?url={full_url}"

            content = soup.prettify()
        else:
            # If it's an image or something else, just pass it through
            content = resp.content

        # Clean up security headers so the site loads
        excluded = ['content-encoding', 'content-length', 'transfer-encoding', 'connection', 'x-frame-options', 'content-security-policy']
        headers = [(n, v) for (n, v) in resp.raw.headers.items() if n.lower() not in excluded]

        return Response(content, resp.status_code, headers)
    except Exception as e:
        return f"Proxy Error: {e}", 500
