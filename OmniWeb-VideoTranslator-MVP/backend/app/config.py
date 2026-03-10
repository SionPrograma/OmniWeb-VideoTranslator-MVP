import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "OmniWeb VideoTranslator MVP"
    DEBUG: bool = True
    
    # Base paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    OUTPUT_DIR: Path = BASE_DIR / "outputs"
    TEMP_DIR: Path = BASE_DIR / "temp"
    
    # Integration URLs
    LIBRETRANSLATE_URL: str = "http://localhost:5000"
    
    # Model Names
    WHISPER_MODEL: str = "base"
    COQUI_TTS_MODEL: str = "tts_models/multilingual/multi-dataset/xtts_v2"
    
    # Sub-directories for outputs
    AUDIO_OUTPUT: Path = OUTPUT_DIR / "audio"
    SUBTITLE_OUTPUT: Path = OUTPUT_DIR / "subtitles"
    TRANSCRIPT_OUTPUT: Path = OUTPUT_DIR / "transcripts"
    TRANSLATION_OUTPUT: Path = OUTPUT_DIR / "translations"
    MERGED_OUTPUT: Path = OUTPUT_DIR / "merged"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def create_directories(self):
        """Ensure all required directories exist."""
        directories = [
            self.OUTPUT_DIR,
            self.TEMP_DIR,
            self.AUDIO_OUTPUT,
            self.SUBTITLE_OUTPUT,
            self.TRANSCRIPT_OUTPUT,
            self.TRANSLATION_OUTPUT,
            self.MERGED_OUTPUT
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

settings = Settings()
settings.create_directories()
