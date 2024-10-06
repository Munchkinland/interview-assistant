from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Button, Select, TextArea
from speech_recognition_handler import SpeechRecognizer
from text_generation import TextGenerator
from language_processor import LanguageProcessor
import os

class SpeechRecognitionWorker:
  def __init__(self, recognizer, language):
      self.recognizer = recognizer
      self.language = language

  def recognize(self):
      return self.recognizer.recognize_speech(self.language)

class InterviewAssistantApp(App):
  CSS = """
  #main {
      layout: grid;
      grid-size: 2;
      grid-gutter: 1 2;
      padding: 1;
  }
  TextArea {
      height: 5;
  }
  Button {
      width: 100%;
  }
  """

  def __init__(self):
      super().__init__()
      self.speech_recognizer = SpeechRecognizer()
      self.text_generator = TextGenerator()
      self.language_processor = LanguageProcessor()

      resume_path = os.path.join("interview-assistant", "resources", "resume.txt")
      try:
          with open(resume_path, "r", encoding="utf-8") as f:
              self.resume = f.read()
      except FileNotFoundError:
          print(f"No se encontró el archivo de currículum en la ruta: {resume_path}")
          self.resume = ""

  def compose(self) -> ComposeResult:
      yield Header()
      yield Container(
          Select([(lang, lang) for lang in ["Español", "English"]], id="language"),
          TextArea(placeholder="Pregunta del entrevistador / Interviewer's question", id="interviewer_question"),
          Button("Escuchar pregunta / Listen to question", id="listen_button"),
          TextArea(placeholder="Respuesta generada / Generated answer", id="generated_answer"),
          Button("Generar respuesta / Generate answer", id="generate_button"),
          TextArea(placeholder="Tu respuesta / Your answer", id="interviewee_answer"),
          Button("Escuchar tu respuesta / Listen to your answer", id="listen_answer_button"),
          id="main"
      )
      yield Footer()

  def on_button_pressed(self, event: Button.Pressed) -> None:
      if event.button.id == "listen_button":
          self.listen_question()
      elif event.button.id == "generate_button":
          self.generate_answer()
      elif event.button.id == "listen_answer_button":
          self.listen_answer()

  def listen_question(self):
      language_code = self.get_language_code()
      worker = SpeechRecognitionWorker(self.speech_recognizer, language_code)
      text = worker.recognize()
      self.query_one("#interviewer_question").value = text

  def listen_answer(self):
      language_code = self.get_language_code()
      worker = SpeechRecognitionWorker(self.speech_recognizer, language_code)
      text = worker.recognize()
      self.query_one("#interviewee_answer").value = text

  def generate_answer(self):
      question = self.query_one("#interviewer_question").value
      context = "Entrevista de trabajo" if self.query_one("#language").value == "Español" else "Job interview"
      language = 'es' if self.query_one("#language").value == "Español" else 'en'
      
      response = self.text_generator.generate_response(question, context, self.resume, language)
      self.query_one("#generated_answer").value = response

  def get_language_code(self):
      return "es-ES" if self.query_one("#language").value == "Español" else "en-US"

if __name__ == "__main__":
  app = InterviewAssistantApp()
  app.run()

# Created/Modified files during execution:
# None