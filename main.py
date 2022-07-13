import speech_recognition as sr
import pyttsx3

from bs4 import BeautifulSoup
import requests

# Initialize the recognizer
r = sr.Recognizer()


def GetWeather():
    print("hi")
    url = "https://weather.com/en-GB/weather/today/l/50.93,0.13?par=google&temp=c"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    title = (soup.find("h2", {"class": "Card--cardHeading--3et4e"})).text
    weatherTable = soup.findAll("li", {"class": "Column--column--2bRa6"})
    data = ["In the"]
    for i in range(0, 3):
        time = (weatherTable[i].find(
            "span", {"class": "Ellipsis--ellipsis--lfjoB"})).text
        temperatureValue = weatherTable[i].find(
            "span", {"data-testid": "TemperatureValue"}).text
        precipitationChance = weatherTable[i].find(
            "span", {"class": "Column--precip--2H5Iw"}).text
        if precipitationChance != "--":
            data.append(time)
            data.append(temperatureValue)
            data.append(precipitationChance)
    return data


commands = {'weather': GetWeather()}


def SpeakText(command):

    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


while(1):
    try:
        # use the microphone as source for input.
        with sr.Microphone() as source2:

            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)
            SpeakText("beep")
            # listens for the user's input
            audio2 = r.listen(source2)

            # Using google to recognize audio
            speech = r.recognize_google(audio2)
            speech = speech.lower()

            for i in commands.keys():
                if i == speech:
                    response = commands.get(i)
                    print(response)
                else:
                    print("command not understood add the command")

            SpeakText(response)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occured")
