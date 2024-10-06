import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QComboBox, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from speech_recognition_handler import SpeechRecognizer
from text_generation import TextGenerator
from language_processor import LanguageProcessor

class SpeechRecognitionThread(QThread):
  textReady = pyqtSignal(str)

  def __init__(self, recognizer, language):
      super().__init__()
      self.recognizer = recognizer
      self.language = language

  def run(self):
      text = self.recognizer.recognize_speech(self.language)
      self.textReady.emit(text)

class InterviewAssistantGUI(QMainWindow):
  def __init__(self):
      super().__init__()
      self.setWindowTitle("Asistente de Entrevistas / Interview Assistant")
      self.setGeometry(100, 100, 800, 600)

      self.central_widget = QWidget()
      self.setCentralWidget(self.central_widget)
      self.layout = QVBoxLayout(self.central_widget)

      self.setup_ui()

      self.speech_recognizer = SpeechRecognizer()
      self.text_generator = TextGenerator()
      self.language_processor = LanguageProcessor()

      # Actualizar la ruta del currículum
      resume_path = os.path.join("interview-assistant", "resources", "resume.txt")
      try:
          with open(resume_path, "r", encoding="utf-8") as f:
              self.resume = f.read()
      except FileNotFoundError:
          print(f"No se encontró el archivo de currículum en la ruta: {resume_path}")
          self.resume = ""

  def setup_ui(self):
      # Configuración de idioma / Language configuration
      self.language_layout = QHBoxLayout()
      self.language_label = QLabel("Idioma / Language:")
      self.language_combo = QComboBox()
      self.language_combo.addItems(["Español", "English"])
      self.language_layout.addWidget(self.language_label)
      self.language_layout.addWidget(self.language_combo)
      self.layout.addLayout(self.language_layout)

      # Área de texto para la pregunta del entrevistador / Text area for interviewer's question
      self.interviewer_question = QTextEdit()
      self.interviewer_question.setPlaceholderText("Pregunta del entrevistador / Interviewer's question")
      self.layout.addWidget(self.interviewer_question)

      # Botón para iniciar reconocimiento de voz / Button to start speech recognition
      self.listen_button = QPushButton("Escuchar pregunta / Listen to question")
      self.listen_button.clicked.connect(self.start_listening)
      self.layout.addWidget(self.listen_button)

      # Área de texto para la respuesta generada / Text area for generated answer
      self.generated_answer = QTextEdit()
      self.generated_answer.setPlaceholderText("Respuesta generada / Generated answer")
      self.layout.addWidget(self.generated_answer)

      # Botón para generar respuesta / Button to generate answer
      self.generate_button = QPushButton("Generar respuesta / Generate answer")
      self.generate_button.clicked.connect(self.generate_answer)
      self.layout.addWidget(self.generate_button)

      # Área de texto para la respuesta del entrevistado / Text area for interviewee's answer
      self.interviewee_answer = QTextEdit()
      self.interviewee_answer.setPlaceholderText("Tu respuesta / Your answer")
      self.layout.addWidget(self.interviewee_answer)

      # Botón para escuchar la respuesta del entrevistado / Button to listen to interviewee's answer
      self.listen_answer_button = QPushButton("Escuchar tu respuesta / Listen to your answer")
      self.listen_answer_button.clicked.connect(self.start_listening_answer)
      self.layout.addWidget(self.listen_answer_button)

  def start_listening(self):
      self.listen_button.setEnabled(False)
      self.listen_button.setText("Escuchando... / Listening...")
      
      language_code = self.get_language_code()
      self.speech_thread_question = SpeechRecognitionThread(self.speech_recognizer, language_code)
      self.speech_thread_question.textReady.connect(self.on_speech_recognized)
      self.speech_thread_question.start()

  def start_listening_answer(self):
      self.listen_answer_button.setEnabled(False)
      self.listen_answer_button.setText("Escuchando... / Listening...")
      
      language_code = self.get_language_code()
      self.speech_thread_answer = SpeechRecognitionThread(self.speech_recognizer, language_code)
      self.speech_thread_answer.textReady.connect(self.on_answer_recognized)
      self.speech_thread_answer.start()

  def on_speech_recognized(self, text):
      self.interviewer_question.setPlainText(text)
      self.listen_button.setEnabled(True)
      self.listen_button.setText("Escuchar pregunta / Listen to question")

  def on_answer_recognized(self, text):
      self.interviewee_answer.setPlainText(text)
      self.listen_answer_button.setEnabled(True)
      self.listen_answer_button.setText("Escuchar tu respuesta / Listen to your answer")

  def generate_answer(self):
      question = self.interviewer_question.toPlainText()
      context = "Entrevista de trabajo" if self.language_combo.currentText() == "Español" else "Job interview"
      language = 'es' if self.language_combo.currentText() == "Español" else 'en'
      
      response = self.text_generator.generate_response(question, context, self.resume, language)
      self.generated_answer.setPlainText(response)

  def get_language_code(self):
      return "es-ES" if self.language_combo.currentText() == "Español" else "en-US"