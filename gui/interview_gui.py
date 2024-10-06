# gui/interview_gui.py
import tkinter as tk
from tkinter import scrolledtext
from audio_capture import AudioCapture
from transcriber import Transcriber
from response_generator import ResponseGenerator
import threading

class InterviewGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Interview Assistant")
        
        # Inicializa los componentes
        self.audio_capture = AudioCapture()
        self.transcriber = Transcriber("models/vosk-model-small-en-us")  # Ruta al modelo de Vosk
        self.response_generator = ResponseGenerator("gpt-neo-1.3B")  # Modelo generativo
        
        # Configuración de la interfaz
        self.start_button = tk.Button(master, text="Iniciar Grabación", command=self.start_recording)
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(master, text="Detener Grabación", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)
        
        self.transcription_label = tk.Label(master, text="Transcripción:")
        self.transcription_label.pack(pady=5)
        
        self.transcription_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=10)
        self.transcription_text.pack(pady=5)
        
        self.response_label = tk.Label(master, text="Respuesta Generada:")
        self.response_label.pack(pady=5)
        
        self.response_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=10)
        self.response_text.pack(pady=5)

    def start_recording(self):
        self.transcription_text.delete(1.0, tk.END)  # Limpiar texto previo
        self.response_text.delete(1.0, tk.END)  # Limpiar texto previo
        self.start_button.config(state=tk.DISABLED)  # Desactivar botón de inicio
        self.stop_button.config(state=tk.NORMAL)  # Activar botón de detener
        
        # Iniciar grabación en un hilo separado para no bloquear la GUI
        self.recording_thread = threading.Thread(target=self.record_audio)
        self.recording_thread.start()

    def stop_recording(self):
        self.audio_capture.stop_recording()
        self.start_button.config(state=tk.NORMAL)  # Activar botón de inicio
        self.stop_button.config(state=tk.DISABLED)  # Desactivar botón de detener

    def record_audio(self):
        self.audio_capture.start_recording()  # Iniciar grabación
        self.audio_capture.record_audio()  # Grabar audio continuamente
        
        # Después de detener la grabación, procesa el audio
        audio_data = self.audio_capture.stop_recording()
        transcription = self.transcriber.transcribe_audio(audio_data)
        self.transcription_text.insert(tk.END, transcription + "\n")  # Mostrar transcripción

        # Generar respuesta basada en la transcripción
        if transcription:
            response = self.response_generator.generate_response(transcription)
            self.response_text.insert(tk.END, response + "\n")  # Mostrar respuesta generada

if __name__ == "__main__":
    root = tk.Tk()
    app = InterviewGUI(root)
    root.mainloop()
