# audio_capture.py
import pyaudio
import wave

class AudioCapture:
    def __init__(self, chunk=1024, format=pyaudio.paInt16, channels=1, rate=16000):
        self.chunk = chunk
        self.format = format
        self.channels = channels
        self.rate = rate
        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = None
        self.frames = []

    def start_recording(self):
        """Inicia la grabación de audio."""
        self.frames = []  # Reinicia los frames
        self.stream = self.pyaudio_instance.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        print("Grabando... Presiona Ctrl+C para detener.")

    def record_audio(self):
        """Graba audio hasta que se detenga manualmente."""
        try:
            while True:
                data = self.stream.read(self.chunk)
                self.frames.append(data)
        except KeyboardInterrupt:
            print("Grabación detenida.")

    def stop_recording(self):
        """Detiene la grabación y cierra el stream."""
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio_instance.terminate()
        return b''.join(self.frames)  # Retorna todos los datos de audio grabados
