import time
import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name='tasks.runner.run_workflow')
def run_workflow(workflow_id: int):
    from apps.workflows.models import Workflow, WorkflowRun
    from core.agent.execution_loop import ExecutionLoop

    try:
        workflow = Workflow.objects.get(id=workflow_id)
    except Workflow.DoesNotExist:
        logger.error(f'Workflow #{workflow_id} não encontrado.')
        return

    run = WorkflowRun.objects.create(workflow=workflow, status='running')
    start = time.time()
    loop = None

    try:
        loop = ExecutionLoop(headless=True)
        goal = (
            f"Verificar emails importantes no {workflow.email_provider} "
            f"para o usuário {workflow.user.username}"
        )
        history = loop.run_goal(goal)

        duration = int((time.time() - start) * 1000)
        run.status = 'success'
        run.result_summary = _build_summary(history)
        run.logs = str(history)
        run.duration_ms = duration
        run.save()

        logger.info(f'Workflow #{workflow_id} concluído em {duration}ms')

    except Exception as e:
        run.status = 'error'
        run.logs = str(e)
        run.duration_ms = int((time.time() - start) * 1000)
        run.save()
        logger.exception(f'Erro no workflow #{workflow_id}')
        raise

    finally:
        if loop:
            loop.close()


def _build_summary(history: list) -> str:
    if not history:
        return 'Nenhuma ação executada.'
    last_action = history[-1].get('action', {})
    if last_action.get('type') == 'done':
        return last_action.get('summary', 'Tarefa concluída.')
    return f'{len(history)} ação(ões) executada(s).'
