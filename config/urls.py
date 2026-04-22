import json
import os
import urllib.request
import urllib.error
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def demo_view(request):
    return render(request, 'demo.html')


CHECK_PROMPT = """Voce e um verificador de noticias para idosos. Classifique a noticia a seguir.

Noticia: "{noticia}"

Responda APENAS com JSON valido neste formato (sem markdown, sem texto extra):
{{"verdict": "fake" | "true", "explanation": "explicacao curta e gentil para idosos, em no maximo 3 frases, citando fontes ou desmentidos quando possivel"}}

Use verdict "fake" para noticias falsas, enganosas ou sem comprovacao.
Use verdict "true" para noticias verificadas em fontes oficiais."""


@csrf_exempt
def check_news_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    try:
        body = json.loads(request.body or b'{}')
    except Exception:
        body = {}

    noticia = (body.get('noticia') or '').strip()
    if not noticia:
        return JsonResponse({'error': 'noticia vazia'}, status=400)

    prompt = CHECK_PROMPT.format(noticia=noticia)
    api_key = os.getenv('GEMINI_API_KEY', '')

    last_error = None
    for model in ['gemini-flash-latest', 'gemini-2.5-flash', 'gemini-2.5-pro']:
        try:
            url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}'
            payload = json.dumps({
                'contents': [{'parts': [{'text': prompt}]}],
                'generationConfig': {'temperature': 0.2, 'responseMimeType': 'application/json'},
            }).encode('utf-8')
            req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = json.loads(resp.read().decode('utf-8'))

            text = ''
            for part in body.get('candidates', [{}])[0].get('content', {}).get('parts', []):
                text += part.get('text', '')
            text = text.strip()
            if text.startswith('```'):
                text = text.split('```')[1]
                if text.startswith('json'):
                    text = text[4:]
                text = text.strip().rstrip('`').strip()

            data = json.loads(text)
            verdict = 'fake' if data.get('verdict') == 'fake' else 'true'
            explanation = data.get('explanation') or 'Sem explicacao disponivel.'
            return JsonResponse({'verdict': verdict, 'explanation': explanation, 'model': model})
        except Exception as e:
            last_error = e
            continue

    return JsonResponse({
        'verdict': 'fake',
        'explanation': f'Nao foi possivel consultar o verificador agora. Detalhe tecnico: {last_error}',
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo/', demo_view),
    path('', demo_view),
    path('api/check-news/', check_news_view),
    path('api/auth/', include('apps.users.urls')),
    path('api/workflows/', include('apps.workflows.urls')),
    path('api/sessions/', include('apps.sessions.urls')),
]
