from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from deep_translator import GoogleTranslator

# Load model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained("emotion-model")
tokenizer = AutoTokenizer.from_pretrained("emotion-model")

# Emotion ID to label mapping
id2label = {
    0: "sadness",
    1: "joy",
    2: "love",
    3: "anger",
    4: "fear",
    5: "surprise"
}

# Predict emotion from English text
def predict_emotion(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model(**inputs)
    predicted_label_id = torch.argmax(outputs.logits).item()
    predicted_label = id2label[predicted_label_id]
    return predicted_label_id, predicted_label

# Translate dialogue (Marathi to English)
def translate_marathi_to_english(text):
    return GoogleTranslator(source='auto', target='en').translate(text)

# Process the script and return list of results
def process_script_emotions(script_path):
    results = []

    with open(script_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        if ":" in line:
            name, dialogue = line.strip().split(":", 1)
            dialogue = dialogue.strip()
            if dialogue:
                translated = translate_marathi_to_english(dialogue)
                emotion_id, emotion_label = predict_emotion(translated)

                results.append({
                    "speaker": name.strip(),
                    "original_dialogue": dialogue,
                    "translated_dialogue": translated,
                    "emotion_id": emotion_id,
                    "emotion_label": emotion_label
                })

    return results
