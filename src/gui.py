import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QComboBox, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from speech_recognition_handler import SpeechRecognizer
from text_generation import TextGenerator
from language_processor import LanguageProcessor

class SpeechRecognitionThread(QThread):
    textReady = pyqtSignal(str)

    def __init__(self, recognizer, language_code):
        super().__init__()
        self.recognizer = recognizer
        self.language_code = language_code

    def run(self):
        text = self.recognizer.recognize_speech(self.language_code)
        self.textReady.emit(text)

class InterviewAssistantGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Asistente de Entrevistas / Interview Assistant")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.speech_recognizer = SpeechRecognizer()
        self.text_generator = TextGenerator()
        self.language_processor = LanguageProcessor()

        self.setup_ui()
        self.load_resume()

    def setup_ui(self):
        self.setup_language_selection()
        self.setup_interviewer_question()
        self.setup_generated_answer()
        self.setup_interviewee_answer()

    def setup_language_selection(self):
        self.language_layout = QHBoxLayout()
        self.language_label = QLabel("Idioma / Language:")
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Español", "English"])
        self.language_layout.addWidget(self.language_label)
        self.language_layout.addWidget(self.language_combo)
        self.layout.addLayout(self.language_layout)

    def setup_interviewer_question(self):
        self.interviewer_question = QTextEdit()
        self.interviewer_question.setPlaceholderText("Pregunta del entrevistador / Interviewer's question")
        self.layout.addWidget(self.interviewer_question)

        self.listen_button = QPushButton("Escuchar pregunta / Listen to question")
        self.listen_button.clicked.connect(self.start_listening_question)
        self.layout.addWidget(self.listen_button)

    def setup_generated_answer(self):
        self.generated_answer = QTextEdit()
        self.generated_answer.setPlaceholderText("Respuesta generada / Generated answer")
        self.layout.addWidget(self.generated_answer)

        self.generate_button = QPushButton("Generar respuesta / Generate answer")
        self.generate_button.clicked.connect(self.generate_answer)
        self.layout.addWidget(self.generate_button)

    def setup_interviewee_answer(self):
        self.interviewee_answer = QTextEdit()
        self.interviewee_answer.setPlaceholderText("Tu respuesta / Your answer")
        self.layout.addWidget(self.interviewee_answer)

        self.listen_answer_button = QPushButton("Escuchar tu respuesta / Listen to your answer")
        self.listen_answer_button.clicked.connect(self.start_listening_answer)
        self.layout.addWidget(self.listen_answer_button)

    def load_resume(self):
        resume_path = os.path.join("interview-assistant", "resources", "resume.txt")
        try:
            with open(resume_path, "r", encoding="utf-8") as f:
                self.resume = f.read()
        except FileNotFoundError:
            print(f"No se encontró el archivo de currículum en la ruta: {resume_path}")
            self.resume = ""

    def get_language_codes(self):
        if self.language_combo.currentText() == "Español":
            return "es-ES", "es"
        else:
            return "en-US", "en"

    def start_listening_question(self):
        self.start_listening(self.listen_button, self.interviewer_question)

    def start_listening_answer(self):
        self.start_listening(self.listen_answer_button, self.interviewee_answer)

    def start_listening(self, button, text_edit):
        button.setEnabled(False)
        button.setText("Escuchando... / Listening...")
        
        speech_code, _ = self.get_language_codes()
        speech_thread = SpeechRecognitionThread(self.speech_recognizer, speech_code)
        speech_thread.textReady.connect(lambda text: self.on_speech_recognized(text, button, text_edit))
        speech_thread.start()

    def on_speech_recognized(self, text, button, text_edit):
        text_edit.setPlainText(text)
        button.setEnabled(True)
        button.setText("Escuchar pregunta / Listen to question" if button == self.listen_button else "Escuchar tu respuesta / Listen to your answer")

    def generate_answer(self):
        question = self.interviewer_question.toPlainText()
        context = "Entrevista de trabajo" if self.language_combo.currentText() == "Español" else "Job interview"
        _, gen_code = self.get_language_codes()
        
        response = self.text_generator.generate_response(question, context, self.resume, gen_code)
        self.generated_answer.setPlainText(response)