from celery import shared_task
from .models import Reservation
from datetime import datetime

@shared_task
def delete_expired_reservations():
    print("Task was run!!!")
    now = datetime.now()
    expired_reservations = Reservation.objects.filter(timeout__lte=now) # Less then or equal
    print(f"Expired Reservations: {expired_reservations}")
    count = expired_reservations.delete()
    return f"{count[0]} reservations deleted."
