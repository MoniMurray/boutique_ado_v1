from django.http import HttpResponse 

class StripeWH_Handler:
    """
    Handle Stripe Webhooks
    """

    def __init__(self, request):
        """ the init class method is a setup method that is called every 
        time an instance of the class is created"""

        self.request = reques
    
    def handle_event(self, event):
        """ Handle a generic/unknown/unexpected webhook event """

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )