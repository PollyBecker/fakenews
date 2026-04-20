from google.genai import types as genai_types
from core.services.gemini_client import get_client, GeminiModels


class TTSService:
    VOICES = {
        'feminino': 'Aoede',
        'masculino': 'Puck',
        'neutro': 'Charon',
    }

    def speak(self, text: str, voice: str = 'feminino') -> bytes:
        client = get_client()
        voice_name = self.VOICES.get(voice, self.VOICES['feminino'])

        response = client.models.generate_content(
            model=GeminiModels.TTS,
            contents=text,
            config=genai_types.GenerateContentConfig(
                response_modalities=['AUDIO'],
                speech_config=genai_types.SpeechConfig(
                    voice_config=genai_types.VoiceConfig(
                        prebuilt_voice_config=genai_types.PrebuiltVoiceConfig(
                            voice_name=voice_name,
                        )
                    )
                ),
            ),
        )

        audio_part = response.candidates[0].content.parts[0]
        return audio_part.inline_data.data

    def speak_to_wav(self, text: str, voice: str = 'feminino') -> bytes:
        import wave, io

        raw_audio = self.speak(text, voice)

        # Gemini TTS retorna PCM 24kHz mono 16-bit
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)
            wf.writeframes(raw_audio)

        return buf.getvalue()
