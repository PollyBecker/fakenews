from google.genai import types as genai_types
from core.services.gemini_client import get_client, GeminiModels


class STTService:
    def transcribe(self, audio_bytes: bytes, mime_type: str = 'audio/wav') -> str:
        client = get_client()

        response = client.models.generate_content(
            model=GeminiModels.STT,
            contents=[
                genai_types.Part.from_bytes(data=audio_bytes, mime_type=mime_type),
                'Transcreva este áudio em português. Retorne apenas o texto, sem comentários adicionais.',
            ],
        )

        return response.text.strip()
