from celery import shared_task
from .models import Reservation
from datetime import datetime

@shared_task
def delete_expired_reservations():
    now = datetime.now()
    expired_reservations = Reservation.objects.filter(timeout__lt=now)
    count = expired_reservations.delete()
    return f"{count[0]} reservations deleted."
