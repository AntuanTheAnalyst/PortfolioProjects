from pypdf import PdfReader
from gtts import gTTS

reader = PdfReader("sample_audiobook_test.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

# print(text)

tts = gTTS(text=text, lang="en")

tts.save("audio.mp3")