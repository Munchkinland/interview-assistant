import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from speech_recognition_handler import SpeechRecognizer
from text_generation import TextGenerator
from language_processor import LanguageProcessor

class InterviewAssistantGUI(BoxLayout):
  def __init__(self, **kwargs):
      super().__init__(**kwargs)
      self.orientation = 'vertical'
      self.padding = 10
      self.spacing = 10

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

      self.setup_ui()

  def setup_ui(self):
      # Language selection
      language_layout = BoxLayout(size_hint_y=None, height=30)
      language_layout.add_widget(Label(text="Idioma / Language:"))
      self.language_spinner = Spinner(text='Español', values=('Español', 'English'))
      language_layout.add_widget(self.language_spinner)
      self.add_widget(language_layout)

      # Interviewer's question
      self.interviewer_question = TextInput(hint_text="Pregunta del entrevistador / Interviewer's question", multiline=True)
      self.add_widget(self.interviewer_question)

      # Listen button
      self.listen_button = Button(text="Escuchar pregunta / Listen to question", on_press=self.start_listening)
      self.add_widget(self.listen_button)

      # Generated answer
      self.generated_answer = TextInput(hint_text="Respuesta generada / Generated answer", multiline=True)
      self.add_widget(self.generated_answer)

      # Generate button
      self.generate_button = Button(text="Generar respuesta / Generate answer", on_press=self.generate_answer)
      self.add_widget(self.generate_button)

      # Interviewee's answer
      self.interviewee_answer = TextInput(hint_text="Tu respuesta / Your answer", multiline=True)
      self.add_widget(self.interviewee_answer)

      # Listen answer button
      self.listen_answer_button = Button(text="Escuchar tu respuesta / Listen to your answer", on_press=self.start_listening_answer)
      self.add_widget(self.listen_answer_button)

  def start_listening(self, instance):
      self.listen_button.disabled = True
      self.listen_button.text = "Escuchando... / Listening..."
      Clock.schedule_once(self.perform_listening, 0.1)

  def perform_listening(self, dt):
      language_code = self.get_language_code()
      text = self.speech_recognizer.recognize_speech(language_code)
      self.interviewer_question.text = text
      self.listen_button.disabled = False
      self.listen_button.text = "Escuchar pregunta / Listen to question"

  def start_listening_answer(self, instance):
      self.listen_answer_button.disabled = True
      self.listen_answer_button.text = "Escuchando... / Listening..."
      Clock.schedule_once(self.perform_listening_answer, 0.1)

  def perform_listening_answer(self, dt):
      language_code = self.get_language_code()
      text = self.speech_recognizer.recognize_speech(language_code)
      self.interviewee_answer.text = text
      self.listen_answer_button.disabled = False
      self.listen_answer_button.text = "Escuchar tu respuesta / Listen to your answer"

  def generate_answer(self, instance):
      question = self.interviewer_question.text
      context = "Entrevista de trabajo" if self.language_spinner.text == "Español" else "Job interview"
      language = 'es' if self.language_spinner.text == "Español" else 'en'
      
      response = self.text_generator.generate_response(question, context, self.resume, language)
      self.generated_answer.text = response

  def get_language_code(self):
      return "es-ES" if self.language_spinner.text == "Español" else "en-US"

class InterviewAssistantApp(App):
  def build(self):
      return InterviewAssistantGUI()

if __name__ == "__main__":
  InterviewAssistantApp().run()

# Created/Modified files during execution:
# None