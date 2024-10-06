# main.py
from audio_capture import AudioCapture
from transcriber import Transcriber
from response_generator import ResponseGenerator

class InterviewAssistant:
    def __init__(self):
        self.audio_capture = AudioCapture()
        self.transcriber = Transcriber("models/vosk-model-small-en-us")  # Ruta al modelo de Vosk
        self.response_generator = ResponseGenerator("gpt-neo-1.3B")  # Modelo generativo

    def start_interview(self):
        self.audio_capture.start_recording()  # Inicia la grabación

        # Graba audio continuamente hasta que se interrumpa manualmente
        self.audio_capture.record_audio()
        
        # Detiene la grabación y obtiene los datos
        audio_data = self.audio_capture.stop_recording()

        # Transcribe el audio grabado
        transcription = self.transcriber.transcribe_audio(audio_data)
        print(f"Transcription: {transcription}")

        # Generar respuesta basada en la transcripción
        if transcription:
            response = self.response_generator.generate_response(transcription)
            print(f"Generated Response: {response}")

if __name__ == "__main__":
    assistant = InterviewAssistant()
    assistant.start_interview()  # Inicia la entrevista
