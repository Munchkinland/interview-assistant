import os
from textual.app import App
from textual.widgets import Button, Select, TextArea
from textual.reactive import Reactive
from speech_recognition_handler import SpeechRecognizer
from text_generation import TextGenerator
from language_processor import LanguageProcessor

class InterviewAssistantApp(App):
    language = Reactive("Español")

    def __init__(self):
        super().__init__()
        self.speech_recognizer = SpeechRecognizer()
        self.text_generator = TextGenerator()
        self.language_processor = LanguageProcessor()
        self.resume = self.load_resume()

    async def on_mount(self) -> None:
        await self.view.dock(Select(options=["Español", "English"], value=self.language), edge="top")
        await self.view.dock(TextArea(placeholder="Pregunta del entrevistador / Interviewer's question"), edge="top", size=5)
        await self.view.dock(Button("Escuchar pregunta / Listen to question", id="listen_question"), edge="top")
        await self.view.dock(TextArea(placeholder="Respuesta generada / Generated answer"), edge="top", size=5)
        await self.view.dock(Button("Generar respuesta / Generate answer", id="generate"), edge="top")
        await self.view.dock(TextArea(placeholder="Tu respuesta / Your answer"), edge="top", size=5)
        await self.view.dock(Button("Escuchar tu respuesta / Listen to your answer", id="listen_answer"), edge="top")

    def load_resume(self):
        resume_path = os.path.join("interview-assistant", "resources", "resume.txt")
        try:
            with open(resume_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"No se encontró el archivo de currículum en la ruta: {resume_path}")
            return ""

    def get_language_codes(self):
        return ("es-ES", "es") if self.language == "Español" else ("en-US", "en")

    async def handle_button_pressed(self, event):
        button_id = event.button.id
        if button_id in ["listen_question", "listen_answer"]:
            await self.start_listening(button_id)
        elif button_id == "generate":
            await self.generate_answer()

    async def start_listening(self, button_id):
        speech_code, _ = self.get_language_codes()
        text = self.speech_recognizer.recognize_speech(speech_code)
        text_area = self.view.query_one(f"TextArea:nth-child({2 if button_id == 'listen_question' else 6})")
        text_area.text = text

    async def generate_answer(self):
        question = self.view.query_one("TextArea:nth-child(2)").text
        context = "Entrevista de trabajo" if self.language == "Español" else "Job interview"
        _, gen_code = self.get_language_codes()
        response = self.text_generator.generate_response(question, context, self.resume, gen_code)
        self.view.query_one("TextArea:nth-child(4)").text = response

if __name__ == "__main__":
    InterviewAssistantApp().run()