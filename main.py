#use this to actiate the virtual enviorment
        #source venv/bin/activate


import pyttsx3 

def Speak(text):
    rate = 100
    engine = pyttsx3.init()
    voices = engine.getProptery('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', rate+50)
    engine.say(text)
    engine.runandwait()
    


Speak("hello world")
Speak("shit")