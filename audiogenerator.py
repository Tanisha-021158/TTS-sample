import requests
import os
from genderdetection import detect_gender
from predict_emotion import process_script_emotions


# Emotion-specific ElevenLabs settings
emotion_settings = {
    "joy": {"stability": 0.35, "similarity_boost": 0.8, "style_exaggeration": 0.3, "speed": 1.05},
    "sadness": {"stability": 0.75, "similarity_boost": 0.75, "style_exaggeration": 0.1, "speed": 0.85},
    "anger": {"stability": 0.25, "similarity_boost": 0.85, "style_exaggeration": 0.4, "speed": 1.1},
    "fear": {"stability": 0.4, "similarity_boost": 0.7, "style_exaggeration": 0.2, "speed": 0.95},
    "surprise": {"stability": 0.3, "similarity_boost": 0.65, "style_exaggeration": 0.35, "speed": 1.1},
    "love": {"stability": 0.45, "similarity_boost": 0.8, "style_exaggeration": 0.25, "speed": 0.95},
    "neutral": {"stability": 0.8, "similarity_boost": 0.75, "style_exaggeration": 0.0, "speed": 1.0}
}


def generate_audio(text, output_filename, voice_id, emotion="neutral"):
    print(f"🔐 API key in use: {API_KEY}")

    settings = emotion_settings.get(emotion, emotion_settings["neutral"])

    # Optional: truncate if text too long for API
    if len(text) > 2000:
        print(f"⚠️ Truncating input text for safety: {text[:30]}...")
        text = text[:2000]

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
            "similarity_boost": settings["similarity_boost"],
            "style_exaggeration": settings["style_exaggeration"],
            "speed": settings["speed"]
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        with open(output_filename, "wb") as f:
            f.write(response.content)
        return output_filename
    else:
        print(f"❌ ElevenLabs API failed for line: '{text[:50]}...'")
        print(f"Status: {response.status_code} - {response.text}")
        return None


def process_script_content(script_file_path):
    results = process_script_emotions(script_file_path)
    processed_data = []

    for i, result in enumerate(results, 1):
        speaker = result["speaker"]
        original = result["original_dialogue"]
        translated = result["translated_dialogue"]
        emotion = result["emotion_label"]

        gender, _ = detect_gender(speaker)
        voice_id = voice_map.get(gender)

        if not voice_id:
            print(f"⚠️ Unknown gender or voice missing for speaker: {speaker}")
            continue

        audio_path = f"static/audio/line_{i}_{speaker}.mp3"
        audio_result = generate_audio(original, audio_path, voice_id, emotion)

        if not audio_result:
            print(f"⚠️ Failed to generate audio for line {i} ({speaker}): {original}")

        processed_data.append({
            "line_num": i,
            "speaker": speaker,
            "gender": gender,
            "original": original,
            "translated": translated,
            "emotion": emotion,
            "audio_path": audio_result  # May be None, and frontend will handle that
        })

    return processed_data


def regenerate_audio_with_overrides(line_num, speaker, original, gender, emotion):
    voice_id = voice_map.get(gender)
    if not voice_id:
        print(f"⚠️ Unknown gender for override: {speaker}, gender: {gender}")
        return None

    audio_path = f"static/audio/line_{line_num}_{speaker}_override.mp3"
    return generate_audio(original, audio_path, voice_id, emotion)
