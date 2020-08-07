import pyttsx3

class speak:
    def __init__(self, have_internet):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)

        #self.have_internet = have_internet
        self.have_internet = False

        #voices = self.engine.getProperty('voices')
        #for voice in voices:
        #    print(f"voices: {voice.id}")

    def configure(self, **kwargs):
        #rate, volume, voice
        if 'rate' in kwargs:
            try:
                self.engine.setProperty('rate', kwargs.get('rate'))
            except:
                self.engine.setProperty('rate', 125)
        elif 'volume' in kwargs:
            try:
                if kwargs.get('volume') > 0 and kwargs.get('volume') < 1.0:
                    self.engine.setProperty('volume', kwargs.get('volume'))
            except:
                pass
        elif 'voiceid' in kwargs:
            try:
                self.engine.setProperty('voice', kwargs.get('voiceid'))
            except:
                voices = self.engine.getProperty('voices')
                self.engine.setProperty('voice', voices[0].id)

    def speak(self, words, **kwargs):
        self.engine.say(words)
        self.engine.runAndWait()
