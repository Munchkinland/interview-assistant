import os
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from speech_recognition_handler import SpeechRecognizer
from text_generation import TextGenerator
from language_processor import LanguageProcessor
from resume_processor import ResumeProcessor
from transcriber import Transcriber  # Asegúrate de que esta clase esté correctamente implementada

class InterviewAssistantGUI(BoxLayout):
  def __init__(self, **kwargs):
      super().__init__(**kwargs)
      self.orientation = 'vertical'
      self.speech_recognizer = SpeechRecognizer()
      self.text_generator = TextGenerator()
      self.language_processor = LanguageProcessor()
      self.resume = ""
      self.job_description = ""  # Nueva variable para almacenar la descripción del trabajo
      self.is_listening = False

      # Language selection
      self.language_spinner = Spinner(
          text='Español',
          values=('Español', 'English'),
          size_hint=(1, None),
          height=50
      )
      self.add_widget(self.language_spinner)

      # Resume upload button
      self.upload_resume_button = Button(
          text='Subir currículum / Upload resume',
          size_hint=(1, None),
          height=50
      )
      self.upload_resume_button.bind(on_press=self.show_load_resume)
      self.add_widget(self.upload_resume_button)

      # Job description input
      self.job_description_input = TextInput(
          hint_text='Descripción del puesto / Job Description',
          multiline=True,
          size_hint=(1, None),
          height=150
      )
      self.add_widget(self.job_description_input)

      # Button to upload job description
      self.upload_job_description_button = Button(
          text='Cargar descripción del puesto / Upload Job Description',
          size_hint=(1, None),
          height=50
      )
      self.upload_job_description_button.bind(on_press=self.show_load_job_description)
      self.add_widget(self.upload_job_description_button)

      # Interviewer's question
      self.interviewer_question = TextInput(
          hint_text='Pregunta del entrevistador / Interviewer\'s question',
          multiline=True,
          size_hint=(1, None),
          height=100
      )
      self.add_widget(self.interviewer_question)

      # Listen to question button
      self.listen_button = Button(
          text='Escuchar pregunta / Listen to question',
          size_hint=(1, None),
          height=50
      )
      self.listen_button.bind(on_press=self.toggle_listening_question)
      self.add_widget(self.listen_button)

      # Generated answer
      self.generated_answer = TextInput(
          hint_text='Respuesta generada / Generated answer',
          multiline=True,
          size_hint=(1, None),
          height=150
      )
      self.add_widget(self.generated_answer)

      # Generate answer button
      self.generate_button = Button(
          text='Generar respuesta / Generate answer',
          size_hint=(1, None),
          height=50
      )
      self.generate_button.bind(on_press=self.generate_answer)
      self.add_widget(self.generate_button)

      # Interviewee's answer
      self.interviewee_answer = TextInput(
          hint_text='Tu respuesta / Your answer',
          multiline=True,
          size_hint=(1, None),
          height=100
      )
      self.add_widget(self.interviewee_answer)

      # Listen to answer button
      self.listen_answer_button = Button(
          text='Escuchar tu respuesta / Listen to your answer',
          size_hint=(1, None),
          height=50
      )
      self.listen_answer_button.bind(on_press=self.toggle_listening_answer)
      self.add_widget(self.listen_answer_button)

  def show_load_job_description(self, instance):
      content = BoxLayout(orientation='vertical')
      self.file_chooser = FileChooserListView()
      content.add_widget(self.file_chooser)

      load_button = Button(text='Cargar', size_hint_y=None, height=50)
      load_button.bind(on_press=self.load_job_description)
      content.add_widget(load_button)

      self._popup = Popup(title="Cargar descripción del puesto", content=content, size_hint=(0.9, 0.9))
      self._popup.open()

  def load_job_description(self, instance):
      try:
          selected_file = self.file_chooser.selection[0]
          with open(selected_file, 'r', encoding='utf-8') as file:
              self.job_description = file.read()
          self.job_description_input.text = self.job_description
          print(f"Descripción del puesto cargada desde: {selected_file}")
          self._popup.dismiss()
          self.show_success_popup("Descripción del puesto cargada exitosamente")
      except Exception as e:
          print(f"Error al cargar la descripción del puesto: {str(e)}")
          self.show_error_popup(f"Error al cargar la descripción del puesto: {str(e)}")

  def show_load_resume(self, instance):
      content = BoxLayout(orientation='vertical')
      self.file_chooser = FileChooserListView()
      content.add_widget(self.file_chooser)

      load_button = Button(text='Cargar', size_hint_y=None, height=50)
      load_button.bind(on_press=self.load_resume)
      content.add_widget(load_button)

      self._popup = Popup(title="Cargar currículum", content=content, size_hint=(0.9, 0.9))
      self._popup.open()

  def load_resume(self, instance):
      try:
          selected_file = self.file_chooser.selection[0]
          self.resume = ResumeProcessor.process_resume(selected_file)
          self.text_generator.process_resume(self.resume)
          print(f"Currículum cargado y procesado desde: {selected_file}")
          self._popup.dismiss()
          self.show_success_popup("Currículum cargado exitosamente")
      except Exception as e:
          print(f"Error al cargar el currículum: {str(e)}")
          self.show_error_popup(f"Error al cargar el currículum: {str(e)}")

  def show_success_popup(self, message):
      content = Label(text=message)
      popup = Popup(title="Éxito", content=content, size_hint=(None, None), size=(400, 200))
      popup.open()

  def show_error_popup(self, message):
      content = Label(text=message)
      popup = Popup(title="Error", content=content, size_hint=(None, None), size=(400, 200))
      popup.open()

  def get_language_codes(self):
      return ("es", "es-ES") if self.language_spinner.text == "Español" else ("en", "en-US")

  def toggle_listening_question(self, instance):
      if not self.is_listening:
          self.start_listening(self.listen_button, self.interviewer_question, role="question")
      else:
          self.stop_listening(self.listen_button, role="question")

  def toggle_listening_answer(self, instance):
      if not self.is_listening:
          self.start_listening(self.listen_answer_button, self.interviewee_answer, role="answer")
      else:
          self.stop_listening(self.listen_answer_button, role="answer")

  def start_listening(self, button, text_input, role):
      self.is_listening = True
      button.text = "Detener escucha / Stop listening"
      language_code, _ = self.get_language_codes()

      # Inicializar el transcriber en un hilo separado
      self.transcriber = Transcriber(language=language_code)
      thread = threading.Thread(target=self.transcriber.listen_continuously, args=(self.update_transcription, role))
      thread.daemon = True
      thread.start()

  def stop_listening(self, button, role):
      self.is_listening = False
      button.text = "Escuchar pregunta / Listen to question" if role == "question" else "Escuchar tu respuesta / Listen to your answer"
      if self.transcriber:
          self.transcriber.stop()
          self.transcriber = None

  def update_transcription(self, text, role):
      def _update_text(dt):
          if role == "question":
              self.interviewer_question.text += text + " "
          elif role == "answer":
              self.interviewee_answer.text += text + " "
      Clock.schedule_once(_update_text)

  def generate_answer(self, instance):
      if not self.resume:
          self.show_error_popup("Por favor, cargue un currículum primero.")
          return

      question = self.interviewer_question.text
      context = "Entrevista de trabajo" if self.language_spinner.text == "Español" else "Job interview"
      _, gen_code = self.get_language_codes()

      # Aquí puedes usar la descripción del trabajo en la generación de respuestas
      job_description = self.job_description_input.text

      try:
          response = self.text_generator.generate_response(question, context, self.resume, job_description, gen_code)
          self.generated_answer.text = response
      except Exception as e:
          print(f"Error al generar la respuesta: {str(e)}")
          self.show_error_popup(f"Error al generar la respuesta: {str(e)}")

class InterviewAssistantApp(App):
  def build(self):
      return InterviewAssistantGUI()

if __name__ == '__main__':
  InterviewAssistantApp().run()