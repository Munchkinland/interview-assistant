# transcriber.py
from vosk import Model, KaldiRecognizer
import json

class Transcriber:
    def __init__(self, model_path):
        self.model = Model(model_path)  # Cargar el modelo de Vosk
        self.recognizer = KaldiRecognizer(self.model, 16000)  # Inicializar el reconocedor

    def transcribe_audio(self, audio_data):
        """
        Transcribe el audio dado utilizando el modelo de Vosk.
        :param audio_data: Datos de audio en formato WAV.
        :return: Texto transcrito.
        """
        if self.recognizer.AcceptWaveform(audio_data):
            result = self.recognizer.Result()
            return json.loads(result)['text']
        else:
            return None
