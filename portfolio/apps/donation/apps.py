from django.apps import AppConfig


class DonationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'donation'
    verbose_name = '09.Donation'

    def ready(self):
        from . import signals
        signals.paypal_payment_received
