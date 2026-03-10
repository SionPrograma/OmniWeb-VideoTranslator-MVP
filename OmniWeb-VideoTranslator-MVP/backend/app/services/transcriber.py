import whisper
from pathlib import Path
from ..config import settings

class Transcriber:
    def __init__(self):
        self.model = None

    def get_model(self):
        if self.model is None:
            self.model = whisper.load_model(settings.WHISPER_MODEL)
        return self.model

    def transcribe(self, audio_path: Path) -> dict:
        model = self.get_model()
        result = model.transcribe(str(audio_path), verbose=False)
        return result
