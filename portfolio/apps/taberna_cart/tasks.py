from celery import shared_task
from datetime import timedelta
from django.utils.timezone import now
from .models import Cart


@shared_task
def delete_old_carts():
    threshold_date = now() - timedelta(days=60)
    old_carts = Cart.objects.filter(date_added__lt=threshold_date)
    old_carts.delete()
