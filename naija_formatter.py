"""Custom formatter for Naija TTS dataset"""
import os
from typing import List

def naija_formatter(root_path: str, meta_file: str, **kwargs) -> List[List]:
    """
    Custom formatter for Naija TTS dataset.
    
    Format: audio_path|text|speaker|language
    
    Args:
        root_path: Root path of the dataset
        meta_file: Metadata file path
        
    Returns:
        List of [text, audio_path, speaker_name, language] items
    """
    txt_file = os.path.join(root_path, meta_file)
    print(f"DEBUG: naija_formatter called with root_path={root_path}, meta_file={meta_file}")
    print(f"DEBUG: expected txt_file={txt_file}")
    items = []
    
    if not os.path.exists(txt_file):
        print(f"ERROR: Metadata file not found: {txt_file}")
        return []
    
    with open(txt_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            parts = line.split("|")
            if len(parts) < 4:
                continue
                
            audio_path = parts[0]
            text = parts[1]
            speaker = parts[2]
            language = parts[3]
            
            # Make audio path absolute
            audio_file = os.path.join(root_path, audio_path)
            
            # Return format: dictionary
            items.append({
                "text": text,
                "audio_file": audio_file,
                "speaker_name": speaker,
                "language": language,
                "root_path": root_path
            })
    
    return items
