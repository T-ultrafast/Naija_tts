import os
import io
from flask import Flask, render_template, request, send_file, jsonify
from TTS.utils.synthesizer import Synthesizer
from naija_formatter import naija_formatter
import TTS.tts.datasets

# Register formatter
TTS.tts.datasets.naija = naija_formatter

app = Flask(__name__)

# Paths
OUT_DIR = "out/naija_xtts_yor/naija_xtts_yor-November-29-2025_09+21AM-0000000"
MODEL_PATH = os.path.join(OUT_DIR, "checkpoint_2.pth")
CONFIG_PATH = os.path.join(OUT_DIR, "config.json")

# Global synthesizer
synthesizer = None

def load_model():
    global synthesizer
    if synthesizer is None:
        print(f"Loading model from {MODEL_PATH}...")
        if not os.path.exists(MODEL_PATH):
            print(f"Error: Model file not found at {MODEL_PATH}")
            return False
        
        synthesizer = Synthesizer(
            tts_checkpoint=MODEL_PATH,
            tts_config_path=CONFIG_PATH,
            use_cuda=False,
        )
        print("Model loaded successfully!")
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/synthesize', methods=['POST'])
def synthesize():
    if not synthesizer:
        if not load_model():
            return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400

    print(f"Synthesizing: {text}")
    try:
        wav = synthesizer.tts(text)
        
        # Convert to bytes
        out = io.BytesIO()
        synthesizer.save_wav(wav, out)
        out.seek(0)
        
        return send_file(
            out,
            mimetype="audio/wav",
            as_attachment=False,
            download_name="output.wav"
        )
    except Exception as e:
        print(f"Error during synthesis: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    load_model()
    app.run(debug=True, port=5000)
