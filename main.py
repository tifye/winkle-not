from cgitb import text
import speech_recognition
import pyttsx3
from textblob import TextBlob
from stefan_variations import stefan_variations

recognizer = speech_recognition.Recognizer()
speech_engine = pyttsx3.init()
texts = []

# Function that checks if string contains a list of words
def contains_list(string, words):
  for word in words:
    if contains(string, word):
      return True
  return False

# Function that checks if string contains a word
def contains(string, word):
  return string.find(word) != -1

def speak(text):
    speech_engine.say(text)
    speech_engine.runAndWait()

def recognize_speech_from_mic(recognizer, microphone):
  recognizer.adjust_for_ambient_noise(microphone, duration=0.05)
  audio = recognizer.listen(microphone)
  text = recognizer.recognize_google(audio)
  text = text.lower()
  return text

def text_sentiment(text):
  blob = TextBlob(text)
  sentiment = blob.sentiment.polarity
  return sentiment

def process_sentiment(text):
  sentiment = text_sentiment(text)
  print(f"Sentiment: {sentiment}")
  if sentiment > 0.2:
    speak("Stop that")
  elif sentiment < -0.02:
    speak("Continue")
  else:
    speak("You said something neutral")

def handle_text(text):
  global texts
  texts.append(text)
  if len(texts) > 3:
    texts.pop(0)
  return '. '.join(texts)

def main():
  global recognizer
  while True:
    try:
      with speech_recognition.Microphone() as mic:
        text = recognize_speech_from_mic(recognizer, mic)

        print(f"Recognized: {text}")
        # speak(text)
        full_context = handle_text(text)
        if contains_list(full_context, stefan_variations):
          process_sentiment(full_context)
        
    except speech_recognition.UnknownValueError as e:
      print(e)
      recognizer = speech_recognition.Recognizer()
      continue
  
if __name__ == "__main__":
  main()