from django.db import models
from django.conf import settings


class Workflow(models.Model):
    SCHEDULE_CHOICES = [('daily', 'Diário'), ('once', 'Uma vez')]
    PROVIDER_CHOICES = [('gmail', 'Gmail')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workflows')
    name = models.CharField(max_length=200)
    trigger_time = models.TimeField()
    schedule_type = models.CharField(max_length=20, choices=SCHEDULE_CHOICES, default='daily')
    email_provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='gmail')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    class Meta:
        db_table = 'workflows'


class WorkflowRun(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('running', 'Executando'),
        ('success', 'Sucesso'),
        ('error', 'Erro'),
    ]

    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='runs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    result_summary = models.TextField(blank=True)
    logs = models.TextField(blank=True)
    executed_at = models.DateTimeField(auto_now_add=True)
    duration_ms = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Run #{self.id} — {self.workflow.name} [{self.status}]"

    class Meta:
        db_table = 'workflow_runs'
        ordering = ['-executed_at']
