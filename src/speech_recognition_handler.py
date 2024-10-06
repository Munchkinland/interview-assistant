import speech_recognition as sr

class SpeechRecognizer:
  def __init__(self):
      self.recognizer = sr.Recognizer()

  def recognize_speech(self, language='es-ES'):
      with sr.Microphone() as source:
          print("Escuchando...")
          audio = self.recognizer.listen(source)
      
      try:
          if language.startswith('es'):
              text = self.recognizer.recognize_google(audio, language='es-ES')
          else:
              text = self.recognizer.recognize_google(audio, language='en-US')
          return text
      except sr.UnknownValueError:
          return "No se pudo entender el audio" if language.startswith('es') else "Could not understand audio"
      except sr.RequestError:
          return "No se pudo obtener resultados del servicio de reconocimiento de voz" if language.startswith('es') else "Could not obtain results from speech recognition service"