import pyttsx3
import datetime
import wikipedia

# Alustetaan puhesynteesi
engine = pyttsx3.init()

# Asetetaan äänen nopeus ja äänenvoimakkuus
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

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
    except wikipedia.exceptions.PageError:
        return "Valitsemasi aihe ei löytynyt."

# Komentojen käsittely (manuaaliset komennot)
def handle_command(command):
    if 'aika' in command:
        current_time = tell_time()
        speak(current_time)
    
    elif 'wiki' in command:
        speak("Mitä haluaisit tietää Wikipediasta?")
        query = input("Syötä kysymys: ")
        answer = search_wikipedia(query)
        speak(answer)
    
    elif 'lopeta' in command or 'kiitos' in command:
        speak("Kiitos, että käytit avustajaa. Hei hei!")
        return False
    
    else:
        speak("En ymmärtänyt, voisitko toistaa?")
    
    return True

# Pääsilmukka ilman kuuntelua
def main():
    speak("Hei, kuinka voin auttaa?")
    
    while True:
        command = input("Syötä komento: ").lower()  # Käyttäjä syöttää komennon manuaalisesti
        if not handle_command(command):
            break

if __name__ == "__main__":
    main()
