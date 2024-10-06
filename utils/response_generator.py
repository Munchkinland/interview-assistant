# response_generator.py
from transformers import pipeline

class ResponseGenerator:
    def __init__(self, model_name):
        self.generator = pipeline("text-generation", model=model_name)

    def generate_response(self, prompt):
        """
        Genera una respuesta basada en el prompt proporcionado.
        :param prompt: Pregunta o contexto para la generación de respuesta.
        :return: Respuesta generada.
        """
        response = self.generator(prompt, max_length=100)
        return response[0]['generated_text']
