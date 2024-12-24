from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'taberna_orders'
    verbose_name = '07.Taberna: Orders'

    def ready(self):
        from . import signals
        signals.paypal_taberna_payment_received
