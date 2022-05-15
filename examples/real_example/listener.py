import numpy
import speech_recognition
import librosa
import os
from pydub import AudioSegment
# import datetime
import recognizer


class Listener:
    def __init__(self, speech_to_text_module: recognizer.Recognizer):
        self.recognizer = speech_recognition.Recognizer()
        self.recognizer.pause_threshold = 2
        self.recognizer.non_speaking_duration = 1
        self.microphone = speech_recognition.Microphone()
        self.speech_to_text_module = speech_to_text_module

    def __anything_to_wav(self, path: str):
        extension = path.split(".")[-1]
        audio = None
        if extension == "mp3":
            audio = AudioSegment.from_mp3(path)
        elif extension == "opus":
            audio = AudioSegment.from_ogg(path)
        audio.export(".temp.wav", format="wav")
        return self.listen_file(".temp.wav")

    def listen_file(self, path: str):
        if path.split(".")[-1] == "wav":
            audio = librosa.load(path, sr=16_000)[0]
            return self.__recognize(audio)
        else:
            return self.__anything_to_wav(path)

    def listen_microphone(self):
        with self.microphone as source:
            # self.recognizer.adjust_for_ambient_noise(source)
            print("Запись начата")
            raw_data = self.recognizer.listen(source)

            with open(f".temp.wav", "wb") as file:
                file.write(raw_data.get_wav_data())

            # with open(f"Записи/{str(datetime.datetime.now())[:19].replace(':', '-')}.wav", "wb") as file:
            #     file.write(raw_data.get_wav_data())

            print("Запись приостановлена")
            output = self.listen_file(".temp.wav")
            os.remove(".temp.wav")
            return output

    def __recognize(self, file: numpy.ndarray):
        return self.speech_to_text_module.recognize(file)
