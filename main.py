from flask import Flask, render_template_string
import os

app = Flask(__name__)

# This is a much more stable version for iPad Safari
EMULATOR_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Abe-Station | OS</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { margin: 0; background: #000; color: #00ff88; font-family: monospace; height: 100vh; display: flex; flex-direction: column; }
        #header { padding: 15px; background: #111; border-bottom: 2px solid #00ff88; text-align: center; font-size: 1.2rem; }
        #emu-wrap { flex: 1; position: relative; }
        #emulator { width: 100%; height: 100%; border: none; }
        .footer { padding: 10px; font-size: 0.8rem; text-align: center; color: #555; }
    </style>
</head>
<body>
    <div id="header">ABE-STATION v2.5</div>
    
    <div id="emu-wrap">
        <iframe id="emulator" src="https://emulatorjs.org/embed/nes"></iframe>
    </div>

    <div class="footer">Tap the screen to start | Select a ROM from your iPad</div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(EMULATOR_PAGE)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
