import os
from vosk import Model, KaldiRecognizer
import pyaudio
import json

class Transcriber:
  def __init__(self, language='es'):
      # Actualizar la ruta base de los modelos
      base_model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models'))
      
      # Definir la ruta del modelo según el idioma
      if language.startswith('es'):
          model_path = os.path.join(base_model_path, 'es', 'vosk-model-small-es-0.42')  # Ruta actualizada para español
      else:
          model_path = os.path.join(base_model_path, 'en', 'vosk-model-small-en-us-0.15')  # Ruta actualizada para inglés

      # Verificar si el modelo existe
      if not os.path.exists(model_path):
          raise FileNotFoundError(f"No se pudo encontrar el modelo en {model_path}")

      # Inicializar el modelo y el reconocedor
      self.model = Model(model_path)
      self.recognizer = KaldiRecognizer(self.model, 16000)
      self.mic = pyaudio.PyAudio()
      self.stream = None
      self.listening = False

  def listen_continuously(self, callback, role):
      self.stream = self.mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
      self.stream.start_stream()
      self.listening = True

      while self.listening:
          data = self.stream.read(4096, exception_on_overflow=False)
          if self.recognizer.AcceptWaveform(data):
              result = self.recognizer.Result()
              result_dict = json.loads(result)
              text = result_dict.get("text", "")
              if text:
                  callback(text, role)
          else:
              partial = self.recognizer.PartialResult()
              # Manejar resultados parciales si es necesario

  def stop(self):
      self.listening = False
      if self.stream is not None:
          self.stream.stop_stream()
          self.stream.close()
      self.mic.terminate()