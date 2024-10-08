import os
from dotenv import load_dotenv
import openai
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import re

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

        self.processed_resume = ""
        self.keywords = []  # Para almacenar palabras clave
        self.skills = []    # Para almacenar habilidades

    def process_resume(self, resume_text):
        # Almacenar el texto del currículum
        self.processed_resume = resume_text
        
        # Extraer palabras clave y habilidades
        self.extract_keywords_and_skills(resume_text)

    def extract_keywords_and_skills(self, resume_text):
        # Ejemplo simple de extracción de palabras clave y habilidades
        # Puedes mejorar esta lógica según tus necesidades
        # Aquí se asume que las habilidades están en una lista separada por comas
        skills_pattern = r'Habilidades?:\s*([A-Za-z\s,]+)'
        skills_match = re.search(skills_pattern, resume_text, re.IGNORECASE)
        if skills_match:
            self.skills = [skill.strip() for skill in skills_match.group(1).split(',')]
        
        # Extraer palabras clave (puedes definir tus propias reglas)
        self.keywords = list(set(re.findall(r'\b\w+\b', resume_text)))  # Palabras únicas

    def generate_response(self, prompt, context, resume, job_description, language='es'):
        # Procesar el currículum si no se ha hecho previamente
        if not self.processed_resume:
            self.process_resume(resume)

        if language == 'es':
            system_message = "Eres un asistente de entrevistas útil y profesional. Utiliza el contexto, el currículum y la descripción del trabajo proporcionados para generar respuestas apropiadas."
            user_message = f"Contexto: {context}\nCurriculum: {self.processed_resume}\nDescripción del trabajo: {job_description}\nPregunta: {prompt}\n\nGenera una respuesta apropiada en español:"
        else:
            system_message = "You are a helpful and professional interview assistant. Use the provided context, resume, and job description to generate appropriate responses."
            user_message = f"Context: {context}\nResume: {self.processed_resume}\nJob Description: {job_description}\nQuestion: {prompt}\n\nGenerate an appropriate answer in English:"

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