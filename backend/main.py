from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import uvicorn
import os
from backend.audio_utils import analyze_audio
from backend.map_generator import generate_map

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
