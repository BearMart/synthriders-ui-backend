import json
import base64
from pathlib import Path

def build_beatmap_meta_bin(
    track_data_path: str,
    cover_image_path: str,
    output_path: str,
    song_name: str,
    artist_name: str,
    difficulty: str = "Master",
    beatmapper: str = "AutoSynth"
):
    with open(track_data_path, "r", encoding="utf-8") as f:
        note_data = json.load(f)

    if cover_image_path:
        with open(cover_image_path, "rb") as img:
            cover_bytes = base64.b64encode(img.read()).decode("utf-8")
        cover_image_name = Path(cover_image_path).name
    else:
        cover_bytes = ""
        cover_image_name = ""

    meta = {
        "Name": song_name,
        "Author": artist_name,
        "Artwork": cover_image_name,
        "ArtworkBytes": cover_bytes,
        "Notes": {difficulty: note_data["notes"]},  # ✅ FIXED HERE
        "Lights": {difficulty: []},
        "Squares": {difficulty: []},
        "Triangles": {difficulty: []},
        "DrumSamples": None,
        "FilePath": "",
        "IsAdminOnly": False,
        "EditorVersion": 3,
        "Beatmapper": beatmapper,
        "MusicOffset": 0.0,
        "BPM": note_data.get("bpm", 120),
        "SongPreviewStartTime": 0.0,
        "SongPreviewEndTime": 15.0
    }

    binary_data = json.dumps(meta, indent=2).encode("utf-8-sig")
    with open(output_path, "wb") as f:
        f.write(binary_data)
