from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

class TextGenerator:
  def __init__(self):
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
          full_prompt = f"Contexto: {context}\nCurriculum: {resume}\nPregunta: {prompt}\n\nGenera una respuesta apropiada en español:"
      else:
          full_prompt = f"Context: {context}\nResume: {resume}\nQuestion: {prompt}\n\nGenerate an appropriate answer in English:"
      
      generator = self.generators.get(language[:2], self.generators['es'])
      response = generator(full_prompt, max_length=150, num_return_sequences=1)

      return response[0]['generated_text'].strip()