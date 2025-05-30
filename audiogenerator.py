import requests
import os
from genderdetection import detect_gender

# === CONFIG ===
API_KEY = "sk_0fb792af8e166b088748b97aa2ff09d719e9bad0b21c0e5c"
SCRIPT_FILE = "script.txt"

# Your custom ElevenLabs voice IDs
voice_map = {
    "male": "wlpQBRhZtedzcMp28hF1",
    "female": "o0fLOvUpjMRqfWyUgiuB"
}

# === Emotion-based Voice Settings ===
emotion_settings = {
    "neutral": {"stability": 0.7, "similarity_boost": 0.75},
    "happy": {"stability": 0.4, "similarity_boost": 0.85},
    "sad": {"stability": 0.3, "similarity_boost": 0.8},
    "angry": {"stability": 0.2, "similarity_boost": 0.9},
    "fear": {"stability": 0.35, "similarity_boost": 0.75},
    "surprise": {"stability": 0.3, "similarity_boost": 0.7},
    "disgust": {"stability": 0.25, "similarity_boost": 0.85}
}

# Default emotion for now (can connect NLP later)
EMOTION = "sad"

# === Audio Generation Function ===
def generate_audio(text, output_filename, voice_id, emotion="neutral"):
    settings = emotion_settings.get(emotion, emotion_settings["neutral"])

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": API_KEY
    }

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": settings["stability"],
            "similarity_boost": settings["similarity_boost"]
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        # 🛠️ Ensure output folder exists
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)

        with open(output_filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Saved: {output_filename}")
    else:
        print(f"❌ Error ({response.status_code}): {response.text}")

# === Process Each Line in script.txt ===
def process_script(script_path):
    with open(script_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines, 1):
        if ":" not in line:
            continue

        speaker, dialogue = map(str.strip, line.split(":", 1))
        gender, source = detect_gender(speaker)

        print(f"🔍 Speaker: {speaker} ➜ Gender: {gender} (via {source})")

        voice_id = voice_map.get(gender)
        if not voice_id:
            print(f"⚠️ No voice ID for gender '{gender}' (speaker: {speaker}), skipping.")
            continue

        output_file = f"static/audio/line_{i}_{speaker}.mp3"
        generate_audio(dialogue, output_file, voice_id, EMOTION)

# === Run It ===
if __name__ == "__main__":
    process_script(SCRIPT_FILE)
