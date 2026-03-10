from TTS.api import TTS
from pathlib import Path
from ..config import settings
import torch

class TTSGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = None

    def get_tts(self):
        if self.tts is None:
            self.tts = TTS(settings.COQUI_TTS_MODEL).to(self.device)
        return self.tts

    def generate(self, text: str, output_path: Path, speaker_wav: Path = None, language: str = "en"):
        tts = self.get_tts()
        if speaker_wav and speaker_wav.exists():
            tts.tts_to_file(text=text, speaker_wav=str(speaker_wav), language=language, file_path=str(output_path))
        else:
            # use a default speaker if no voice clone requested
            tts.tts_to_file(text=text, speaker=tts.speakers[0] if tts.speakers else None, language=language, file_path=str(output_path))
        return output_path
