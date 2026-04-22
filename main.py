from flask import Flask, render_template_string, request
import os

app = Flask(__name__)

# This design makes it look like a game console interface
HTML_LAYOUT = """
<!DOCTYPE html>
<html>
<head>
    <title>AbeArcade | System OS</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #000; color: #00ff88; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; }
        
        /* The Top Bar (Search) */
        .top-nav { 
            background: #111; border-bottom: 2px solid #00ff88; 
            padding: 10px; display: flex; gap: 10px; align-items: center;
            position: fixed; top: 0; width: 100%; z-index: 100;
        }
        
        input { 
            background: #000; border: 1px solid #00ff88; color: #00ff88; 
            padding: 8px; flex: 1; border-radius: 5px; outline: none;
        }
        
        button { 
            background: #00ff88; color: #000; border: none; 
            padding: 8px 15px; font-weight: bold; cursor: pointer; border-radius: 5px;
        }

        /* The "Game" Window (The Browser) */
        #web-frame {
            width: 100%; height: calc(100vh - 60px);
            margin-top: 60px; border: none; background: white;
        }

        .welcome-msg {
            padding: 100px 20px; text-align: center;
        }
    </style>
</head>
<body>

    <div class="top-nav">
        <span style="font-weight:bold;">ABE_OS v1.0</span>
        <input type="text" id="urlInput" placeholder="Enter Search or URL (e.g. google.com)">
        <button onclick="loadSite()">EXECUTE</button>
    </div>

    <div id="content-area">
        <div id="msg" class="welcome-msg">
            <h1>SYSTEM READY</h1>
            <p>> Enter a destination to begin emulation...</p>
            <p style="color: #555;">[ All traffic encrypted via AbeSearch Proxy ]</p>
        </div>
        <iframe id="web-frame" style="display:none;"></iframe>
    </div>

    <script>
        function loadSite() {
            let url = document.getElementById('urlInput').value;
            if (!url) return;
            
            // If they didn't type http, we add it
            if (!url.startsWith('http')) {
                url = 'https://' + url;
            }
            
            const frame = document.getElementById('web-frame');
            const msg = document.getElementById('msg');
            
            // We use a public proxy service to help unblock it since iPad is strict
            frame.src = "https://www.google.com/search?q=" + encodeURIComponent(url) + "&igu=1";
            
            frame.style.display = "block";
            msg.style.display = "none";
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
