import pyttsx3
import sys

def main():
    engine = pyttsx3.init()
    for arg in sys.argv[1:]:
        engine.say(arg)
    engine.runAndWait()


if __name__ == "__main__":
    main()

