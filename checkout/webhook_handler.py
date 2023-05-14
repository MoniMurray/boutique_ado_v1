from django.http import HttpResponse 

class StripeWH_Handler:
    """
    Handle Stripe Webhooks
    """

    def __init__(self, request):
        """ the init class method is a setup method that is called every 
        time an instance of the class is created"""

        self.request = request
    
    def handle_event(self, event):
        """ Handle a generic/unknown/unexpected webhook event """

        return HttpResponse(
            content=f'Unhandled Webhook received: {event["type"]}',
            status=200
        )
    
    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id 
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping 
        grand_total = round(stripe_charge.amount/100, 2)

        # replace any empty strings in the shipping_details with 'None'
        for field, value in shipping_details.address.items():
            if value == '':
                shipping_details.address[field] = None
        
        # On a user checking out, their form is submitted - check the 
        # database to see if the order exists already, if it does send a message
        # to that effect, if it does not then create it here in the webhook

        # start by assuming the order doesn't exist yet by setting the var to False
        order_exists = False
        try:
            order = Order.objects.get(
                full_name__iexact=shipping_details.name,
                email__iexact=shipping_details.email,
                phone_number__iexact=shipping_details.phone,
                country__iexact=shipping_details.country,
                post_code__iexact=shipping_details.postal_code,
                town_or_city__iexact=shipping_details.city,
                street_address1__iexact=shipping_details.line1,
                street_address2__iexact=shipping_details.line2,
                county__iexact=shipping_details.state,
                grand_total=grand_total,
            )
            # if the order is found, set the order_exists variable to True
            order_exists = True
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verfied order already in database', 
                status=200
            )
        except Order.DoesNotExist:
            # iterate through the bag items, but load the bag from json
            # version within the paymentIntent, instead of from the session
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=shipping_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.country,
                    post_code=shipping_details.postal_code,
                    town_or_city=shipping_details.city,
                    street_address1=shipping_details.line1,
                    street_address2=shipping_details.line2,
                    county=shipping_details.state,
                )
                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.get(id=item_id)
                    if isinstance[item_data, int]:
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].item():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: (e)',
                    status=500
                )
        print(intent)
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)