import json
from core.services.gemini_client import get_client, GeminiModels

NLU_PROMPT = """
Você é um assistente que extrai parâmetros de automação a partir de linguagem natural.

Dado o texto do usuário, extraia os campos abaixo e retorne APENAS JSON válido, sem texto extra:

{
  "name": "nome descritivo da automação",
  "trigger_time": "HH:MM",
  "schedule_type": "daily" | "once",
  "email_provider": "gmail" | null,
  "missing": ["lista de campos que não foram mencionados e precisam ser perguntados"]
}

Regras:
- Se o usuário não mencionar horário, coloque null em trigger_time e adicione "trigger_time" em missing.
- schedule_type padrão é "daily" se mencionar "todo dia", "toda manhã" etc.
- Se mencionar "uma vez" ou data específica, use "once".
- email_provider: use "gmail" se mencionar Gmail, Google, email, caixa de entrada.
- Se um campo não puder ser inferido, adicione ao array "missing".
"""


class WorkflowBuilder:
    REQUIRED_SLOTS = ['name', 'trigger_time', 'schedule_type', 'email_provider']

    def __init__(self):
        self._slots = {}

    def parse_natural_language(self, text: str) -> dict:
        try:
            return self._extract_with_gemini(text)
        except Exception:
            return {'missing': self.REQUIRED_SLOTS, 'raw': text}

    def _extract_with_gemini(self, text: str) -> dict:
        client = get_client()
        prompt = f"{NLU_PROMPT}\n\nTexto do usuário: \"{text}\""

        response = client.models.generate_content(
            model=GeminiModels.NLU,
            contents=prompt,
        )

        raw = response.text.strip()
        if raw.startswith('```'):
            raw = raw.split('```')[1]
            if raw.startswith('json'):
                raw = raw[4:]

        result = json.loads(raw)

        for slot in self.REQUIRED_SLOTS:
            value = result.get(slot)
            if value is not None:
                self._slots[slot] = value

        return result

    def fill(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.REQUIRED_SLOTS:
                self._slots[key] = value

    def missing_slots(self) -> list:
        return [s for s in self.REQUIRED_SLOTS if s not in self._slots]

    def is_complete(self) -> bool:
        return len(self.missing_slots()) == 0

    def build(self) -> dict:
        if not self.is_complete():
            raise ValueError(f'Slots faltando: {self.missing_slots()}')
        return {**self._slots}
