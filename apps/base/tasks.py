from celery import shared_task

from .utils.gs import GreekStudy


@shared_task
def get_user_id(email: str, password: str):
    if not email or not password:
        return "Email and password are required."
    gs = GreekStudy()
    gs.login(email=email, password=password)
    return gs.get_user_id()
