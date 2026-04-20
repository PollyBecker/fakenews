import json
from core.services.gemini_client import get_client, GeminiModels

PLANNER_PROMPT = """
Você é o cérebro de um agente de automação. Dado o objetivo e o estado atual da UI,
decida qual é a PRÓXIMA ação a executar.

Responda APENAS com JSON válido, sem texto extra. Escolha um dos tipos:

- Navegar: {"type": "open_url", "url": "https://..."}
- Clicar:  {"type": "click", "x": int, "y": int, "description": "o que clicou"}
- Digitar: {"type": "type", "text": "texto a digitar"}
- Tecla:   {"type": "press_key", "key": "RETURN|TAB|ESCAPE|..."}
- Rolar:   {"type": "scroll", "amount": int}
- Concluir:{"type": "done", "summary": "resumo do que foi feito"}

Regras:
- Se o objetivo ainda não foi atingido, escolha uma ação concreta.
- Se a UI já mostra o resultado esperado, use "done" com um resumo útil.
- Não repita ações que já foram executadas sem necessidade.
"""


class Planner:
    def decide(self, goal: str, ui_state: dict, history: list = None) -> dict:
        try:
            return self._decide_with_gemini(goal, ui_state, history or [])
        except Exception:
            return self._decide_from_ui_state(ui_state)

    def _decide_with_gemini(self, goal: str, ui_state: dict, history: list) -> dict:
        client = get_client()

        history_str = ''
        if history:
            last = history[-3:]
            history_str = f"\n\nAções já executadas:\n{json.dumps(last, ensure_ascii=False)}"

        prompt = (
            f"{PLANNER_PROMPT}"
            f"\n\nObjetivo: {goal}"
            f"\n\nEstado atual da UI:\n{json.dumps(ui_state, ensure_ascii=False)}"
            f"{history_str}"
        )

        response = client.models.generate_content(
            model=GeminiModels.PLANNER,
            contents=prompt,
        )

        raw = response.text.strip()
        if raw.startswith('```'):
            raw = raw.split('```')[1]
            if raw.startswith('json'):
                raw = raw[4:]

        return json.loads(raw)

    def _decide_from_ui_state(self, ui_state: dict) -> dict:
        suggested = ui_state.get('suggested_action', {})
        if suggested:
            return suggested
        return {'type': 'done', 'summary': 'Nenhuma ação (planner sem Gemini).'}
