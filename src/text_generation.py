import os
from dotenv import load_dotenv
import openai
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

class TextGenerator:
  def __init__(self):
      # Cargar variables de entorno
      load_dotenv()
      
      # Configurar OpenAI API
      openai.api_key = os.getenv('OPENAI_API_KEY')
      
      if not openai.api_key:
          raise ValueError("No se encontró la clave de API de OpenAI en el archivo .env")

      self.models = {
          "es": "PlanTL-GOB-ES/gpt2-base-bne",
          "en": "gpt2"
      }
      self.generators = {}
      for lang, model_name in self.models.items():
          tokenizer = AutoTokenizer.from_pretrained(model_name)
          model = AutoModelForCausalLM.from_pretrained(model_name)
          self.generators[lang] = pipeline('text-generation', model=model, tokenizer=tokenizer)

  def generate_response(self, prompt, context, resume, language='es'):
      if language == 'es':
          system_message = "Eres un asistente de entrevistas útil y profesional. Utiliza el contexto y el currículum proporcionados para generar respuestas apropiadas."
          user_message = f"Contexto: {context}\nCurriculum: {resume}\nPregunta: {prompt}\n\nGenera una respuesta apropiada en español:"
      else:
          system_message = "You are a helpful and professional interview assistant. Use the provided context and resume to generate appropriate responses."
          user_message = f"Context: {context}\nResume: {resume}\nQuestion: {prompt}\n\nGenerate an appropriate answer in English:"

      try:
          response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=[
                  {"role": "system", "content": system_message},
                  {"role": "user", "content": user_message}
              ],
              max_tokens=150,
              n=1,
              stop=None,
              temperature=0.7,
          )
          return response.choices[0].message['content'].strip()
      except Exception as e:
          print(f"Error al usar GPT-3.5 Turbo: {e}")
          # Fallback al modelo local si GPT-3.5 Turbo falla
          generator = self.generators.get(language[:2], self.generators['es'])
          response = generator(user_message, max_length=150, num_return_sequences=1)
          return response[0]['generated_text'].strip()