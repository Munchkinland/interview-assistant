import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from speech_recognition_handler import SpeechRecognizer
from text_generation import TextGenerator
from language_processor import LanguageProcessor

class InterviewAssistantGUI(BoxLayout):
  def __init__(self, **kwargs):
      super().__init__(**kwargs)
      self.orientation = 'vertical'
      self.speech_recognizer = SpeechRecognizer()
      self.text_generator = TextGenerator()
      self.language_processor = LanguageProcessor()
      self.resume = self.load_resume()

      self.language_spinner = Spinner(text='Español', values=('Español', 'English'))
      self.add_widget(self.language_spinner)

      self.interviewer_question = TextInput(hint_text='Pregunta del entrevistador / Interviewer\'s question', multiline=True)
      self.add_widget(self.interviewer_question)

      self.listen_button = Button(text='Escuchar pregunta / Listen to question')
      self.listen_button.bind(on_press=self.start_listening_question)
      self.add_widget(self.listen_button)

      self.generated_answer = TextInput(hint_text='Respuesta generada / Generated answer', multiline=True)
      self.add_widget(self.generated_answer)

      self.generate_button = Button(text='Generar respuesta / Generate answer')
      self.generate_button.bind(on_press=self.generate_answer)
      self.add_widget(self.generate_button)

      self.interviewee_answer = TextInput(hint_text='Tu respuesta / Your answer', multiline=True)
      self.add_widget(self.interviewee_answer)

      self.listen_answer_button = Button(text='Escuchar tu respuesta / Listen to your answer')
      self.listen_answer_button.bind(on_press=self.start_listening_answer)
      self.add_widget(self.listen_answer_button)

  def load_resume(self):
      resume_path = os.path.join("interview-assistant", "resources", "resume.txt")
      try:
          with open(resume_path, "r", encoding="utf-8") as f:
              return f.read()
      except FileNotFoundError:
          print(f"No se encontró el archivo de currículum en la ruta: {resume_path}")
          return ""

  def get_language_codes(self):
      return ("es-ES", "es") if self.language_spinner.text == "Español" else ("en-US", "en")

  def start_listening_question(self, instance):
      self.start_listening(self.listen_button, self.interviewer_question)

  def start_listening_answer(self, instance):
      self.start_listening(self.listen_answer_button, self.interviewee_answer)

  def start_listening(self, button, text_input):
      button.disabled = True
      button.text = "Escuchando... / Listening..."
      
      speech_code, _ = self.get_language_codes()
      Clock.schedule_once(lambda dt: self.perform_speech_recognition(speech_code, button, text_input), 0.1)

  def perform_speech_recognition(self, speech_code, button, text_input):
      text = self.speech_recognizer.recognize_speech(speech_code)
      text_input.text = text
      button.disabled = False
      button.text = "Escuchar pregunta / Listen to question" if button == self.listen_button else "Escuchar tu respuesta / Listen to your answer"

  def generate_answer(self, instance):
      question = self.interviewer_question.text
      context = "Entrevista de trabajo" if self.language_spinner.text == "Español" else "Job interview"
      _, gen_code = self.get_language_codes()
      
      response = self.text_generator.generate_response(question, context, self.resume, gen_code)
      self.generated_answer.text = response

class InterviewAssistantApp(App):
  def build(self):
      return InterviewAssistantGUI()

if __name__ == '__main__':
  InterviewAssistantApp().run()