import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import RealtimeSession
from .serializers import RealtimeSessionSerializer
from core.agent.execution_loop import ExecutionLoop
from core.services.stt import STTService
from core.services.tts import TTSService


class StartSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        RealtimeSession.objects.filter(user=request.user, status='active').update(status='closed')
        session = RealtimeSession.objects.create(user=request.user)
        return Response(RealtimeSessionSerializer(session).data, status=status.HTTP_201_CREATED)


class SessionCommandView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, session_id):
        try:
            session = RealtimeSession.objects.get(id=session_id, user=request.user, status='active')
        except RealtimeSession.DoesNotExist:
            return Response(
                {'error': 'Sessão não encontrada ou inativa.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        command = request.data.get('command', '')
        session.touch()

        loop = ExecutionLoop()
        result = loop.run_once(command=command)
        return Response({'result': result})


class VoiceCommandView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, session_id):
        try:
            session = RealtimeSession.objects.get(id=session_id, user=request.user, status='active')
        except RealtimeSession.DoesNotExist:
            return Response(
                {'error': 'Sessão não encontrada ou inativa.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        audio_file = request.FILES.get('audio')
        if not audio_file:
            return Response({'error': 'Nenhum áudio enviado.'}, status=status.HTTP_400_BAD_REQUEST)

        session.touch()

        transcript = '[STT indisponível]'
        try:
            stt = STTService()
            mime_type = audio_file.content_type or 'audio/webm'
            transcript = stt.transcribe(audio_file.read(), mime_type=mime_type)
        except Exception as e:
            transcript = f'[Erro STT: {e}]'

        loop = ExecutionLoop()
        result = loop.run_once(command=transcript)

        summary = result.get('action', {}).get('summary', 'Comando executado.')
        audio_b64 = None
        try:
            tts = TTSService()
            audio_b64 = base64.b64encode(tts.speak_to_wav(summary)).decode('utf-8')
        except Exception:
            pass

        return Response({
            'transcript': transcript,
            'result': result,
            'audio_response': audio_b64,
        })


class CloseSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, session_id):
        try:
            session = RealtimeSession.objects.get(id=session_id, user=request.user)
            session.close()
        except RealtimeSession.DoesNotExist:
            return Response({'error': 'Sessão não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'status': 'closed'})
