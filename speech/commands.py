import speech_recognition as sr


class Commands:
    source = sr.Microphone()

    def __init__(self):
        # Words that sphinx should listen closely for. 0-1 is the sensitivity
        # of the wake word.
        self.keywords = [("capture", 1),  # start the capture of data
                         ("save", 1)]     # save session

        self.result = [("left", 1),
                       ("right", 1),
                       ("short", 1),
                       ("long", 1),
                       ("make", 1)]

        r = sr.Recognizer()
        r.adjust_for_ambient_noise(self.source)
        r.listen_in_background(sr.Microphone(), self.callback)

    def callback(self, recognizer, audio):                          # this is called from the background thread
        try:
            speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=self.keywords)
            print(speech_as_text)

            # Look for your "Ok Google" keyword in speech_as_text
            if "capture" in speech_as_text:
                self.recognize_main()

        except sr.UnknownValueError:
            print("Oops! Didn't catch that")

        try:
            print("You said " + recognizer.recognize(audio))  # received audio data, now need to recognize it
        except LookupError:
            print("Oops! Didn't catch that")

    def recognize_main(self):
        print("Starting data capture...")
        # pair bluetooth
        # capture data
        # save data

