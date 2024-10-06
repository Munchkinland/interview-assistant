import os
from vosk import Model, KaldiRecognizer
import pyaudio

class Transcriber:
  def __init__(self, model_path):
      # Usa una ruta absoluta para el modelo
      absolute_model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', model_path))
      
      if not os.path.exists(absolute_model_path):
          print(f"El modelo no se encuentra en la ruta: {absolute_model_path}")
          raise FileNotFoundError(f"No se pudo encontrar el modelo en {absolute_model_path}")
      
      self.model = Model(absolute_model_path)
      self.recognizer = KaldiRecognizer(self.model, 16000)
      
      self.mic = pyaudio.PyAudio()
      self.stream = self.mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
      self.stream.start_stream()

  def listen(self):
      while True:
          data = self.stream.read(4096)
          if len(data) == 0:
              break
          if self.recognizer.AcceptWaveform(data):
              result = self.recognizer.Result()
              return result

  def stop(self):
      self.stream.stop_stream()
      self.stream.close()
      self.mic.terminate()