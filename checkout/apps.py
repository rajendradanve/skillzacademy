"""
imported signal from checkout class
"""

from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    """
    Checkout Config Class
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

    def ready(self):
        import checkout.signals
