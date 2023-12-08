# also import BackgroundTasks from fastapi
# if you process tasks with fastapi.BackgroundTasks
from fastapi import APIRouter, Depends

from src.auth.base_config import current_user
from src.tasks.tasks import send_email_dashboard_report


router = APIRouter(prefix='/report')


@router.get('/dashboard')
def get_dashboard_report(user=Depends(current_user)):
    # task is executed in synchronous mode
    # send_email_dashboard_report(user.username)

    # task is executed in the background fastapi in event loop or another thread
    # add background_tasks: BackgroundTasks as a param of func
    # background_tasks.add_task(send_email_dashboard_report, user.username)

    # task is executed by celery worker in extra process
    send_email_dashboard_report.delay(user.username)

    return {
        'status': 200,
        'data': 'Mail is sended',
        'details': None,
    }
