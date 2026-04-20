import os
from google import genai
from google.genai import types as genai_types


def get_client() -> genai.Client:
    http_options = genai_types.HttpOptions(timeout=10)

    use_vertex = os.getenv('USE_VERTEX_AI', 'false').lower() == 'true'

    if use_vertex:
        project = os.getenv('GOOGLE_CLOUD_PROJECT', '')
        location = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')
        return genai.Client(vertexai=True, project=project, location=location,
                            http_options=http_options)

    api_key = os.getenv('GEMINI_API_KEY', '')
    return genai.Client(api_key=api_key, http_options=http_options)


class GeminiModels:
    VISION = 'gemini-2.0-flash-lite'
    PLANNER = 'gemini-2.0-flash-lite'
    NLU = 'gemini-2.0-flash'
    STT = 'gemini-2.0-flash-lite'
    TTS = 'gemini-2.5-flash-preview-tts'
