import re
import speech_recognition as sr
from os import path
from common_utils.logger import logger
import common_utils.api_utils


class SpeechObject:
    def __init__(self, sentence_from_google, type_='Google Assistant'):
        self.name = None
        if type_ is None or type_ is 'local':
            self.sentence = self.recognizer()
        else:
            self.sentence = sentence_from_google
        self.percentage = None
        self.turn_on_text_signal = "lights on"
        self.turn_off_text_signal = "lights off"
        self.lamp_number = 1

    @staticmethod
    def recognizer():
        r = sr.Recognizer()
        r.operation_timeout = 3
        r.non_speaking_duration = 0.5

        def listener(r):
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source)
            return audio

        audio = listener(r)

        with open(".//output//results.wav", "wb") as f:
            f.write(audio.get_wav_data())

        AUDIO_FILE = path.join(path.dirname(path.realpath(".//output/")), "results.wav")
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # read the entire audio file

        print("alo")

        try:
            the_sentence = r.recognize_google(audio)
            print("Google Speech Recognition thinks you said " + the_sentence)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return None
        return the_sentence

    def set_brightness_with_speech(self):
        sentence_ = self.sentence

        if sentence_:
            if re.search(r"(hundred.*?)", sentence_):
                self.sentence = sentence_.replace("hundred", "100")
            self.percentage = int(sentence_.split()[-1].split('%')[0])
        else:
            self.percentage = None
        return self.percentage

    def get_lamp_number(self):
        sentence_ = self.sentence
        if sentence_:
            if re.search(r"(number.*?\d.)", sentence_):
                self.lamp_number = int(sentence_.split()[-1])
                return self.lamp_number
        else:
            return self.lamp_number

    def turn_on_off_with_speech(self):
        sentence_ = self.sentence
        if sentence_:
            if re.search(r"(lights on.*?)", sentence_) or re.search(r"(on.*?)", sentence_):
                return self.turn_on_text_signal
            elif re.search(r"(lights off.*?)", sentence_) or re.search(r"(off.*?)", sentence_):
                return self.turn_off_text_signal
        else:
            return None
