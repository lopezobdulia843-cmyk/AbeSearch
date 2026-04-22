from flask import Flask, render_template_string
import os

app = Flask(__name__)

# This loads a professional-grade emulator interface
EMULATOR_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Abe-Station | Emulator</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <style>
        body { margin: 0; background: #000; color: #00ff88; font-family: 'Courier New', monospace; overflow: hidden; height: 100vh; display: flex; flex-direction: column; }
        #header { padding: 10px; background: #111; border-bottom: 2px solid #00ff88; text-align: center; font-weight: bold; }
        #emulator-container { flex: 1; width: 100%; position: relative; background: #000; }
        canvas { width: 100%; height: 100%; cursor: inherit; }
        .instructions { position: absolute; bottom: 20px; width: 100%; text-align: center; color: #555; pointer-events: none; }
    </style>
</head>
<body>
    <div id="header">ABE-STATION v2.0 | SYSTEM READY</div>
    
    <div id="emulator-container">
        <iframe src="https://neptunajs.com/embed.html" style="width:100%; height:100%; border:none;"></iframe>
    </div>

    <div class="instructions">Tap the 'Load ROM' button inside the emulator to select a game from your iPad</div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(EMULATOR_PAGE)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
