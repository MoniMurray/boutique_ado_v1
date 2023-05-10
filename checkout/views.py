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

    bag = request.session.get('bag', {})
    # if nothing in the bag
    if not bag:
        messages.error(request, "There is nothing in your bag at the moment")
        return redirect(reverse('products'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)
    
    order_form = Orderform()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51N6Bl9HhC95fjDsPaMeQbc8E9RcMqt7CEaHoIV0ZNCHeb3kMjUyRWGh8cQJgCo21HzBPN7iIoQkgqU5KJmVj27Vq003qUJJuft',
        'client_secret': 'test client secret',
    }
    return render(request, template, context)
    
