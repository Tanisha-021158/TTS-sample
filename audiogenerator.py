import requests
import os
from genderdetection import detect_gender
from predict_emotion import process_script_emotions  

# === CONFIG ===
API_KEY = "sk_0afc7c625ab002429361719d94c9856a3987ad78b79a1c81"
SCRIPT_FILE = "script.txt"

# Your custom ElevenLabs voice IDs
voice_map = {
    "male": "ZSruKT7dxK3hKgfHUl0m",
    "female": "FQ4LU5boZVsszfqflq0t"
}

# === Emotion-based Voice Settings ===
emotion_settings = {
    "joy": {"stability": 0.4, "similarity_boost": 0.85},
    "sadness": {"stability": 0.3, "similarity_boost": 0.8},
    "anger": {"stability": 0.2, "similarity_boost": 0.9},
    "fear": {"stability": 0.35, "similarity_boost": 0.75},
    "surprise": {"stability": 0.3, "similarity_boost": 0.7},
    "love": {"stability": 0.4, "similarity_boost": 0.8},
    "neutral": {"stability": 0.7, "similarity_boost": 0.75},
    
}

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
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        with open(output_filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Saved: {output_filename}")
    else:
        print(f"❌ Error ({response.status_code}): {response.text}")

# === Process Script with Emotion Integration ===
def process_script(script_path):
    results = process_script_emotions(script_path)

    for i, result in enumerate(results, 1):
        speaker = result["speaker"]
        original = result["original_dialogue"]       # Marathi text
        translated = result["translated_dialogue"]   # English text
        emotion = result["emotion_label"]

        gender, source = detect_gender(speaker)
        print(f"\n🔊 Line {i}")
        print(f"👤 Speaker: {speaker} ➜ Gender: {gender} (via {source})")
        print(f"🗣️ Marathi: {original}")
        print(f"🌐 English: {translated}")
        print(f"🎭 Emotion: {emotion}")

        voice_id = voice_map.get(gender)
        if not voice_id:
            print(f"⚠️ No voice ID for gender '{gender}' (speaker: {speaker}), skipping.")
            continue

        output_file = f"static/audio/line_{i}_{speaker}.mp3"
        # Generate audio from Marathi text
        generate_audio(original, output_file, voice_id, emotion)

# === Run It ===
if __name__ == "__main__":
    process_script(SCRIPT_FILE)
