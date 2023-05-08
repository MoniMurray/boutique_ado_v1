from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

    # to override the ready method by importin our signals module,
    #now every time a lineitem is saved or deleted our custom Update_total() 
    #model method will be called, updating the order totals automatically
    def ready(self):
        import checkout.signals
