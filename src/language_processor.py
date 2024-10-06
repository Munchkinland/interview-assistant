from deep_translator import GoogleTranslator

class LanguageProcessor:
  def __init__(self):
      self.es_to_en = GoogleTranslator(source='es', target='en')
      self.en_to_es = GoogleTranslator(source='en', target='es')

  def translate(self, text, target_language):
      try:
          if target_language.startswith('es'):
              return self.en_to_es.translate(text)
          else:
              return self.es_to_en.translate(text)
      except Exception as e:
          print(f"Error en la traducción: {e}")
          return text