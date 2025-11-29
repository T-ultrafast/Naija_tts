import os
import sys
from TTS.utils.synthesizer import Synthesizer
from naija_formatter import naija_formatter
import TTS.tts.datasets

# Register formatter
TTS.tts.datasets.naija = naija_formatter

# Paths
OUT_DIR = "out/naija_xtts_yor/naija_xtts_yor-November-29-2025_09+21AM-0000000"
MODEL_PATH = os.path.join(OUT_DIR, "checkpoint_2.pth")
CONFIG_PATH = os.path.join(OUT_DIR, "config.json")
OUTPUT_WAV = "output.wav"

def main():
    print(f"Loading model from {MODEL_PATH}...")
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model file not found at {MODEL_PATH}")
        return

    # Initialize Synthesizer
    synthesizer = Synthesizer(
        tts_checkpoint=MODEL_PATH,
        tts_config_path=CONFIG_PATH,
        tts_speakers_file=None,
        tts_languages_file=None,
        vocoder_checkpoint=None,
        vocoder_config=None,
        encoder_checkpoint=None,
        encoder_config=None,
        use_cuda=False,
    )

    text = "Bawo ni, ṣe dada ni?"
    print(f"Synthesizing text: '{text}'")
    
    # Synthesize
    wav = synthesizer.tts(text)
    
    # Save
    synthesizer.save_wav(wav, OUTPUT_WAV)
    print(f"Audio saved to {OUTPUT_WAV}")

if __name__ == "__main__":
    main()
