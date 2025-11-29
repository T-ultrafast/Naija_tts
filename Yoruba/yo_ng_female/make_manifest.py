import pandas as pd

# 1. Read the TSV (2 columns: audio_id, text)
df = pd.read_csv("line_index.tsv", sep="\t", header=None, 
names=["audio_id", "text"])

# 2. Build full audio path relative to naija_tts root:
#    e.g. Yoruba/yo_ng_female/yof_06136_00616155826.wav
AUDIO_BASE = "Yoruba/yo_ng_female"
df["audio_path"] = AUDIO_BASE + "/" + df["audio_id"] + ".wav"

# 3. Add speaker + language columns
df["speaker"] = "yor_f_01"   # adjust later if you split by speaker
df["language"] = "yor"       # or "yo" if your config expects ISO 639-1

# 4. Reorder columns to match: audio_path|text|speaker|language
cols = ["audio_path", "text", "speaker", "language"]
manifest = df[cols]

# 5. Save as pipe-separated CSV with no header
manifest.to_csv("metadata.csv", sep="|", header=False, index=False)

