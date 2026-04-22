from flask import Flask, request, redirect, Response
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>AbeSearch is Live</h1><p>Go to /view?url=https://wikipedia.org to test!</p>"

@app.route('/view')
def proxy():
    url = request.args.get('url')
    headers = {'User-Agent': 'Mozilla/5.0'}
    # This fetches the site and tells it to 'unlock'
    resp = requests.get(url, headers=headers)
    proxy_resp = Response(resp.content, resp.status_code)
    # This strips the security blocks
    excluded = ['x-frame-options', 'content-security-policy']
    for k, v in resp.headers.items():
        if k.lower() not in excluded: proxy_resp.headers[k] = v
    return proxy_resp

if __name__ == '__main__':
    # This part lets Render talk to your code
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)