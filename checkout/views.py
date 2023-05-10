from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from .forms import Orderform 
from bag.contexts import bag_contents

import stripe 

# Create your views here.
def checkout(request):
    """ Get the shopping bag from the session; 
    if there's nothing in the bag return a simple error message
    and redirect back to the products page; 
    create an instance of Orderform, which will be empty for now, 
    and then create the template, the context containing the Orderform,
    and finally render it all out. """

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})
    # if nothing in the bag
    if not bag:
        messages.error(request, "There is nothing in your bag at the moment")
        return redirect(reverse('products'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)

    # set the secret key on Stripe
    stripe.api_key = stripe_secret_key

    # create the paymentIntent
    intent = stripe.PaymentIntent.create(
        amount = stripe_total,
        currency = settings.STRIPE_CURRENCY,
    )
    
    order_form = Orderform()

    if not stripe_public_key:
        messages.warning(request, f'Stripe public key is missing. \Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)
    
