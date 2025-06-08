import json
import base64
from pathlib import Path

def build_beatmap_meta_bin(
    track_json_path: str,
    cover_image_path: str,
    output_path: str,
    song_name: str,
    artist_name: str,
    difficulty: str = "Master",
    beatmapper: str = "AutoSynth"
):
    # Load note data from track.data.json
    with open(track_json_path, "r", encoding="utf-8") as f:
        note_data = json.load(f)

    # Load and encode cover image
    cover_image_name = Path(cover_image_path).name
    with open(cover_image_path, "rb") as img:
        cover_bytes = base64.b64encode(img.read()).decode("utf-8")

    # Build the meta structure
    meta = {
        "Name": song_name,
        "Author": artist_name,
        "Artwork": cover_image_name,
        "ArtworkBytes": cover_bytes,
        "Notes": {difficulty: note_data},
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

    # Write to beatmap.meta.bin (UTF-8 with BOM)
    with open(output_path, "w", encoding="utf-8-sig") as f:
        json.dump(meta, f, indent=2)

    print(f"✅ beatmap.meta.bin written to: {output_path}")
