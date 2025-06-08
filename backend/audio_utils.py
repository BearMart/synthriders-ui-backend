import librosa

def analyze_audio(file_path):
    try:
        y, sr = librosa.load(file_path)
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beats, sr=sr).tolist()
        return round(float(tempo)), beat_times
    except Exception as e:
        print("⚠️ Error in analyze_audio:", str(e))
        raise
