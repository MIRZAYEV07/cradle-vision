from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from src.app22 import get_current_active_superuser
from src.app22 import celery_app
from src.app22 import Message
from src.app22 import send_test_email

router = APIRouter()


@router.post(
    "/test-celery/",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
def test_celery(body: Message) -> Message:
    """
    Test Celery worker.
    """
    celery_app.send_task("app22.worker.test_celery", args=[body.message])
    return Message(message="Word received")


@router.post(
    "/test-email/",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
def test_email(email_to: EmailStr) -> Message:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return Message(message="Test email sent")
