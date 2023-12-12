from fastapi import APIRouter, Depends

from src.auth.base_config import current_user
from src.tasks.tasks import send_email_dashboard_report

router = APIRouter(prefix='/report')


@router.get('/dashboard')
def get_dashboard_report(user=Depends(current_user)):
    send_email_dashboard_report.delay(user.username)
    return {
        'status': 200,
        'data': 'Email is sended',
        'details': None,
    }
