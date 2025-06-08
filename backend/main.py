from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
from pathlib import Path
import tempfile
import zipfile

from backend.audio_utils import analyze_audio
from backend.map_generator import generate_map
from backend.beatmap_compiler import build_beatmap_meta_bin  # ✅ Add this import

app = FastAPI()

@app.post("/upload/")
async def upload_audio(file: UploadFile = File(...)):
    file_location = f"temp_audio/{file.filename}"
    os.makedirs("temp_audio", exist_ok=True)
    with open(file_location, "wb") as f:
        f.write(await file.read())

    bpm, beat_times = analyze_audio(file_location)
    map_data = generate_map(bpm, beat_times)

    output_path = file_location.replace(".mp3", "_map.json")
    with open(output_path, "w") as f:
        f.write(map_data)

    return FileResponse(output_path, filename=os.path.basename(output_path))


@app.post("/package/", summary="Package Synth", description="Returns a zipped .synth file")
async def package_synth(mp3: UploadFile = File(...), json: UploadFile = File(...), cover: UploadFile = File(None)):
    temp_dir = Path(tempfile.mkdtemp())
    base_name = mp3.filename.rsplit('.', 1)[0].replace(" ", "_")
    synth_dir = temp_dir / f"{base_name}_CustomMap"
    synth_dir.mkdir()

    # Save .ogg
    ogg_path = synth_dir / f"{base_name}.ogg"
    with open(ogg_path, "wb") as f:
        f.write(await mp3.read())

    # Save map JSON
    json_data = await json.read()
    track_path = synth_dir / "track.data.json"
    with open(track_path, "wb") as f:
        f.write(json_data)

    # Optional cover image
    cover_path = None
    if cover:
        cover_path = synth_dir / "cover.jpg"
        with open(cover_path, "wb") as f:
            f.write(await cover.read())

    # ✅ Compile beatmap.meta.bin
    song_name = base_name.replace("_", " ")
    artist_name = "Uploaded via SynthRiderz AI"
    meta_bin_path = synth_dir / "beatmap.meta.bin"
    meta_bin = build_beatmap_meta_bin(
        track_json_path=str(track_path),
        cover_image_path=str(cover_path) if cover else "",
        output_path=str(meta_bin_path),
        song_name=song_name,
        artist_name=artist_name
    )
    with open(meta_bin_path, "w", encoding="utf-8-sig") as f:
        f.write(meta_bin)

    # Add required meta file
    meta_path = synth_dir / "synthriderz.meta.json"
    meta_path.write_text('{"version":1,"environment":"DefaultEnvironment"}')

    # Create .synth ZIP
    synth_file = temp_dir / f"{base_name}.synth"
    with zipfile.ZipFile(synth_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in synth_dir.iterdir():
            zipf.write(file, arcname=file.name)

    return FileResponse(synth_file, media_type="application/octet-stream", filename=synth_file.name)
