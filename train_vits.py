import os
import sys
from TTS.config import load_config
from TTS.tts.models.vits import Vits
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.utils.audio import AudioProcessor
from trainer import Trainer, TrainerArgs
from TTS.tts.datasets import load_tts_samples
from naija_formatter import naija_formatter

def register_naija_formatter():
    """Register the custom naija formatter so TTS can find it by name."""
    import TTS.tts.datasets
    TTS.tts.datasets.naija = naija_formatter

def main():
    register_naija_formatter()
    # Load config
    config_path = "naija_xtts_config.yaml"
    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        sys.exit(1)
        
    config = load_config(config_path)
    print(f"DEBUG: config.optimizer = {config.optimizer}")
    print(f"DEBUG: type(config.optimizer) = {type(config.optimizer)}")

    
    # Initialize Audio Processor
    ap = AudioProcessor.init_from_config(config)
    
    # Initialize Tokenizer
    # Note: init_from_config returns (tokenizer, config) possibly modifying config
    tokenizer, config = TTSTokenizer.init_from_config(config)

    # Load samples
    train_samples, eval_samples = load_tts_samples(
        config.datasets,
        eval_split=True,
        eval_split_max_size=config.eval_split_max_size,
        eval_split_size=config.eval_split_size,
    )
    
    # Initialize Model
    model = Vits(config, ap, tokenizer, speaker_manager=None)
    
    # Initialize Trainer
    trainer = Trainer(
        TrainerArgs(),
        config,
        output_path=config.output_path,
        model=model,
        train_samples=train_samples,
        eval_samples=eval_samples,
    )
    
    # Start Training
    trainer.fit()

if __name__ == "__main__":
    main()
