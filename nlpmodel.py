from tensorflow.keras.models import load_model
import joblib
import numpy as np

# Load the model
model = load_model("emotion_model.h5")

# Load the tokenizer and label encoder
tokenizer = joblib.load("tokenizer.jb")
label_encoder = joblib.load("label_encoder.jb")

# Example input
text = ["I am so happy today!"]

# Preprocess the text (same as training)
max_length = 100  # Must match your training setup
sequence = tokenizer.texts_to_sequences(text)

from tensorflow.keras.preprocessing.sequence import pad_sequences
padded_sequence = pad_sequences(sequence, maxlen=max_length, padding="post")

# Make prediction
prediction = model.predict(padded_sequence)
predicted_label = np.argmax(prediction, axis=1)
decoded_label = label_encoder.inverse_transform(predicted_label)

print("Predicted Emotion:", decoded_label[0])
