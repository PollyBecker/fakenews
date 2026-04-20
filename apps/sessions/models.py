from django.db import models
from django.conf import settings
from django.utils import timezone


class RealtimeSession(models.Model):
    STATUS_CHOICES = [('active', 'Ativa'), ('closed', 'Encerrada')]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='realtime_sessions',
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity_at = models.DateTimeField(default=timezone.now)

    def touch(self):
        self.last_activity_at = timezone.now()
        self.save(update_fields=['last_activity_at'])

    def close(self):
        self.status = 'closed'
        self.save(update_fields=['status'])

    def __str__(self):
        return f"Sessão #{self.id} — {self.user.username} [{self.status}]"

    class Meta:
        db_table = 'realtime_sessions'
        ordering = ['-started_at']
