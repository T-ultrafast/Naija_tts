from TTS.config import load_config
try:
    config = load_config("naija_xtts_config.yaml")
    print(f"Config loaded. Type: {type(config)}")
    print(f"Model: {config.model}")
except Exception as e:
    print(f"Error loading config: {e}")
