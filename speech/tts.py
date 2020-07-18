import pyttsx3

class speak:
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self, words):
        self.engine.say(words)
        self.engine.runAndWait()
