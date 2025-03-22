from elevenlabs import ElevenLabs

# Set up the ElevenLabs client
client = ElevenLabs(api_key="sk_9ba17a6aa5e25a6e4b3763954f9f84668abe2ed78f6b121c")  # Replace with your actual API key

# Define the text and custom voice ID
voice_id = "o0fLOvUpjMRqfWyUgiuB"  # Replace with your generated "Indian Woman" voice ID
text = "नमस्ते, मैं आपकी सहायता के लिए यहाँ हूँ। आप मुझसे किसी भी विषय पर बात कर सकते हैं।"

# Generate speech as a generator
audio_stream = client.text_to_speech.convert(
    voice_id=voice_id,
    text=text
)

# Save the generated speech as an MP3 file
with open("output.mp3", "wb") as f:
    for chunk in audio_stream:
        f.write(chunk)

print("Speech saved as output.mp3 ✅")
