from flask import Flask, render_template_string
import os

app = Flask(__name__)

# This is a full-screen Emulator setup
EMULATOR_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AbeSearch | Emulator</title>
    <style>
        body { background: #000; color: #00ff88; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; overflow: hidden; }
        #game { width: 100%; height: 80vh; max-width: 800px; border: 2px solid #00ff88; box-shadow: 0 0 20px #00ff88; }
        .controls { margin-top: 20px; text-align: center; background: #111; padding: 15px; border-radius: 10px; }
        h1 { margin-top: 0; text-shadow: 0 0 5px #00ff88; }
    </style>
</head>
<body>
    <h1>AbeSearch Arcade</h1>
    <div id="game">
        <div id="game-container"></div>
    </div>
    
    <div class="controls">
        <p><b>Controls:</b> Arrows = Move | Z = A | X = B | Enter = Start | Shift = Select</p>
        <p>Drag and Drop any <b>.nes</b> file into this window to play!</p>
    </div>

    <script src="https://cdn.jsdelivr.net/gh/ethanaobrien/emulatorjs@latest/dist/emulator.js"></script>
    <script>
        EmuJS.init({
            container: '#game-container',
            system: 'nes',
            # You can add a link to a ROM file here later!
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(EMULATOR_HTML)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
