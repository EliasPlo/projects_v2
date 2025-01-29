import sounddevice as sd
import numpy as np
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia

# Alustetaan puhesynteesi
engine = pyttsx3.init()

# Asetetaan äänen nopeus ja äänenvoimakkuus
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# Funktio puheen tunnistukseen
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Kuuntelen...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language='fi-FI')
        print(f"Kuulin: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("En kuullut mitään selkeää.")
        return ""
    except sr.RequestError:
        print("Verkkovirhe, yritä myöhemmin.")
        return ""

# Funktio puheenvastaukselle
def speak(text):
    print(f"Vastaan: {text}")
    engine.say(text)
    engine.runAndWait()

# Funktio ajan kertomiseen
def tell_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    return f"Nykyinen aika on {current_time}"

# Funktio Wikipedia-haulle
def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=1, lang='fi')
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return "Tuli monta tulosta, tarkenna hakua."
    except wikipedia.exceptions.HTTPTimeoutError:
        return "Wikipediassa on tällä hetkellä ongelmia."

# Pääsilmukka, jossa avustaja kuuntelee ja reagoi
def main():
    speak("Hei, kuinka voin auttaa?")
    
    while True:
        query = recognize_speech()
        
        if 'aika' in query:
            current_time = tell_time()
            speak(current_time)
        
        elif 'wikipedia' in query:
            speak("Mitä haluaisit tietää Wikipediasta?")
            query = recognize_speech()
            answer = search_wikipedia(query)
            speak(answer)
        
        elif 'lopeta' in query or 'kiitos' in query:
            speak("Kiitos, että käytit avustajaa. Hei hei!")
            break
        
        else:
            speak("En ymmärtänyt, voisitko toistaa?")
        
if __name__ == "__main__":
    main()
