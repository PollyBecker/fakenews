import logging
from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(name='tasks.scheduler.scan_due_workflows')
def scan_due_workflows():
    from apps.workflows.models import Workflow
    from tasks.runner import run_workflow

    now = timezone.localtime(timezone.now())
    current_time = now.time().replace(second=0, microsecond=0)

    due = Workflow.objects.filter(
        is_active=True,
        trigger_time__hour=current_time.hour,
        trigger_time__minute=current_time.minute,
    )

    count = 0
    for workflow in due:
        run_workflow.delay(workflow.id)
        count += 1
        logger.info(f'Enfileirado workflow #{workflow.id} — {workflow.name}')

    return f'{count} workflow(s) enfileirado(s)'
