from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <title>ABE-STATION OS</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <style>
        body, html { 
            margin: 0; padding: 0; width: 100%; height: 100%; 
            background: #000; overflow: hidden; font-family: -apple-system, sans-serif;
        }
        #console-container { 
            width: 100%; height: 100%; border: none; 
        }
        .status-bar {
            background: #111; color: #00ff88; font-size: 10px;
            padding: 5px 15px; border-bottom: 1px solid #222;
            display: flex; justify-content: space-between;
        }
    </style>
</head>
<body>
    <div class="status-bar">
        <span>SYSTEM_LOAD: OPTIMAL</span>
        <span>ABE-STATION v5.0</span>
    </div>
    <iframe id="console-container" src="https://afterplay.io"></iframe>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CONTENT)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
