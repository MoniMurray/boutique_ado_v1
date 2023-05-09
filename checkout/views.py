from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import Orderform 

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
    
    order_form = Orderform()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
    }
    return render(request, template, context)
    
