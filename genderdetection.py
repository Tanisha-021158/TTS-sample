import joblib
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

# === Load trained ML model ===
model = joblib.load('gender_predictor.pkl')

# === Manual gender map ===
gender_map = {
    "राम": "male",
    "शिवाजी": "male",
    "विनायक": "male",
    "अजय": "male",
    "सूरज": "male",
    "अमोल": "male",
    "सीता": "female",
    "राधा": "female",
    "सुनिता": "female",
    "अनिता": "female",
    "गीता": "female",
    "लता": "female"
}

# === Rule-Based Suffix Guess ===
def guess_gender_from_name(name):
    name = name.strip()
    if len(name) <= 2:
        return "unknown"

    female_suffixes = (
        "ा", "ी", "ता", "ना", "शा", "ला", "सा", "जा", "रा", "था", "बा", "मा", "दा", "खा", "पा"
    )
    male_suffixes = (
        "क", "द", "ल", "ज", "न", "श", "थ", "भ", "राव", "ेश", "ंत", "ीत", "नंद", "राज"
    )

    for suffix in female_suffixes:
        if name.endswith(suffix):
            return "female"
    for suffix in male_suffixes:
        if name.endswith(suffix):
            return "male"
    return "unknown"

# === Final Gender Detection (Manual + Suffix + ML) ===
def detect_gender(name):
    # 1️⃣ Manual map first
    if name in gender_map:
        return gender_map[name], "manual"
    
    # 2️⃣ Suffix guess fallback
    suffix_guess = guess_gender_from_name(name)
    if suffix_guess != "unknown":
        return suffix_guess, "suffix"
    
    # 3️⃣ ML model fallback
    english_name = transliterate(name, sanscript.DEVANAGARI, sanscript.ITRANS).lower()
    ml_prediction = model.predict([english_name])[0]
    ml_gender = "male" if ml_prediction == 0 else "female"
    return ml_gender, "ml"

# === Process script file for debugging/output ===
def process_script(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for idx, line in enumerate(lines, 1):
        line = line.strip()
        if ":" not in line:
            continue

        speaker, dialogue = map(str.strip, line.split(":", 1))

        # Detect gender with source
        final_gender, source = detect_gender(speaker)

        # Transliterate for display
        english_name = transliterate(speaker, sanscript.DEVANAGARI, sanscript.ITRANS).lower()

        # Print everything
        print(f"🔠 Transliteration: {speaker} ➜ {english_name}")
        print(f"🔹 Line {idx}")
        print(f"👤 Speaker: {speaker}")
        print(f"🗂️  Dialogue: {dialogue}")
        print(f"✅ Final Gender Used: {final_gender} (via {source})\n")

# === Run for testing (optional) ===
if __name__ == "__main__":
    process_script("script.txt")
