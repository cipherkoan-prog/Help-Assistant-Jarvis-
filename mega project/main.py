import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
import time
from openai import OpenAI

recognizer=sr.Recognizer()
engine=pyttsx3.init()

rate = engine.getProperty('rate')
engine.setProperty('rate', 170)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

newsapi="194d3d27fdd04db0a869e7f3e59f8ff6"

def speak(text):
    print("Jarvis speaking:", text)
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    client = OpenAI(
    api_key="your_api_key_here"
    )

    response = client.responses.create(
    model="gpt-5-nano",
    massage=[{"role":"system","content":"You are a virtual assistant named Jarvis. You are helpful, creative, clever, and very friendly."},
             {"role":"user","content":command}
        ]  
        )

    return response.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link=musiclibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
        r = requests.get(url)
        data = r.json()

        articles = data["articles"]
    else:
        # let Open AI handel the erquest
        output=aiProcess(c)
        speak(output)


        speak("Here are the top headlines")
        time.sleep(1)

        for article in articles[:5]:
            title = article["title"]
            print(title)
            speak(title)
            time.sleep(0.5)



if __name__== "__main__":
    speak("Initializing jarvis.....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()

        print("recognizing...")
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=5)

            word = r.recognize_google(audio)
            print("Heard:", word)

            if "jarvis" in word.lower():
                speak("Yes")

                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                print("Command:", command)
                processCommand(command)

        except sr.UnknownValueError:
            print("Could not understand audio (UnknownValueError)")
        except sr.RequestError as e:
            print("Speech recognition request failed; check your internet connection. Error:", e)
        except Exception as e:
            print("Error:", e)
