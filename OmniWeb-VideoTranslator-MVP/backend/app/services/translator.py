import requests
from ..config import settings

class Translator:
    def __init__(self):
        self.url = f"{settings.LIBRETRANSLATE_URL}/translate"

    def translate(self, text: str, target_lang: str) -> str:
        try:
            response = requests.post(self.url, json={
                "q": text,
                "source": "auto",
                "target": target_lang,
                "format": "text"
            })
            response.raise_for_status()
            return response.json()["translatedText"]
        except Exception as e:
            print(f"Translation error: {e}")
            # Fallback for MVP if LibreTranslate is not running
            return f"[Translated to {target_lang}] {text}"
