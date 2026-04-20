import json
from google.genai import types as genai_types
from core.services.gemini_client import get_client, GeminiModels

SYSTEM_PROMPT = """
Você é um agente de automação visual. Analise a imagem da tela e responda APENAS com JSON válido, sem texto extra.

Estrutura obrigatória:
{
  "description": "descrição curta do que está na tela",
  "elements": [
    {"type": "button|input|link|text|image", "label": "texto do elemento", "position": "topo|centro|rodapé|esquerda|direita"}
  ],
  "suggested_action": {
    "type": "click|type|scroll|open_url|press_key|done",
    "description": "o que fazer e por quê",
    ... campos extras dependendo do tipo:
    - click: "x": int, "y": int
    - type: "text": str
    - scroll: "amount": int (positivo = baixo)
    - open_url: "url": str
    - press_key: "key": str (ex: "RETURN", "TAB")
    - done: "summary": str
  }
}
"""


class VisionService:
    def analyze_ui(self, image_bytes: bytes, instruction: str) -> dict:
        if not image_bytes:
            return self._stub('Nenhuma imagem capturada.')
        try:
            return self._call_gemini(image_bytes, instruction)
        except Exception as e:
            return self._stub(error=str(e))

    def _call_gemini(self, image_bytes: bytes, instruction: str) -> dict:
        client = get_client()
        prompt = f"{SYSTEM_PROMPT}\n\nInstrução do usuário: {instruction}"

        response = client.models.generate_content(
            model=GeminiModels.VISION,
            contents=[
                genai_types.Part.from_bytes(data=image_bytes, mime_type='image/png'),
                prompt,
            ],
        )

        raw = response.text.strip()

        if raw.startswith('```'):
            raw = raw.split('```')[1]
            if raw.startswith('json'):
                raw = raw[4:]

        return json.loads(raw)

    def _stub(self, error: str = '') -> dict:
        msg = f'Erro Gemini Vision: {error}' if error else 'Gemini não configurado.'
        return {
            'description': 'Stub — Gemini Vision não ativo',
            'elements': [],
            'suggested_action': {'type': 'done', 'summary': msg},
        }
