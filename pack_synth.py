import os
import json
import shutil
import zipfile
import subprocess
from pathlib import Path

# 📝 Song Info
song_title = "Shiver"
artist_name = "John Summit & Hayla"
difficulty = "Hard"
environment = "DefaultEnvironment"

# 🎯 Input file names
input_map = "generated_map.json"
input_song = "Shiver.mp3"
cover_image = "cover.jpg"  # optional

# 📁 Folder & File Structure
folder_name = f"{song_title.replace(' ', '_')}_CustomMap"
ogg_name = f"{song_title}.ogg"
map_name = "track.data.json"
meta_name = "synthriderz.meta.json"
synth_file = f"{song_title}.synth"

# 📂 Output Directory
output_dir = Path("output") / folder_name
output_dir.mkdir(parents=True, exist_ok=True)

# ✅ 1. Copy Map File
shutil.copy(input_map, output_dir / map_name)

# ✅ 2. Create Metadata File
meta = {
    "songName": song_title,
    "authorName": artist_name,
    "songFilename": ogg_name,
    "trackFilename": map_name,
    "coverImageFilename": cover_image if os.path.exists(cover_image) else "",
    "difficulty": difficulty,
    "environmentName": environment,
    "customData": {}
}
with open(output_dir / meta_name, "w") as f:
    json.dump(meta, f, indent=4)

# ✅ 3. Convert MP3 → OGG
ogg_path = output_dir / ogg_name
subprocess.run(["ffmpeg", "-i", input_song, "-y", str(ogg_path)])

# ✅ 4. Copy Cover Image (if exists)
if os.path.exists(cover_image):
    shutil.copy(cover_image, output_dir / cover_image)

# ✅ 5. Zip to .synth
synth_zip = output_dir.with_suffix(".synth")
with zipfile.ZipFile(synth_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file in output_dir.iterdir():
        zipf.write(file, arcname=file.name)

# ✅ 6. Copy to Synth Riders CustomSongs folder
custom_songs = Path.home() / "Documents" / "SynthRiders" / "CustomSongs"
custom_songs.mkdir(parents=True, exist_ok=True)
shutil.copy(synth_zip, custom_songs / synth_zip.name)

print(f"✅ Packaged and copied to: {custom_songs / synth_zip.name}")