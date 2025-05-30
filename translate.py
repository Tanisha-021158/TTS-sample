from translatepy import Translator

translator = Translator()

def marathi_to_english(text):
    translation = translator.translate(text, "English")
    return translation.result
marathi_line = "तू कुठे चालला आहेस?"
english_line = marathi_to_english(marathi_line)
print("English:", english_line)
# Output: Where are you going?
