import json
import random

def generate_map(bpm, beat_times):
    notes = []
    for time in beat_times:
        note = {
            "time": round(time, 3),
            "position": [random.randint(-5, 5), random.randint(-2, 2)],
            "type": random.choice(["note", "hold", "tap"])
        }
        notes.append(note)

    map_data = {
        "bpm": bpm,
        "notes": notes
    }

    return json.dumps(map_data, indent=2)