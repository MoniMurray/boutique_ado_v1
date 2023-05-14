import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from products.models import Product
from django_countries.fields import CountryField

# when a user checks out we first use the information they put into the 
# payment form (Order) to create an order instance and then we'll iterate 
# through the items in the shopping bag creating an order line item for 
# each one, attaching it to the order and updating the delivery cost, 
# order total and grand total along the way.

class Order(models.Model):
    """ To Create and track Orders for anyone who makes a purchase """

    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False) 
    country = CountryField(blank_label='Country *', null=False, blank=False)
    post_code = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        """ This is a private model only, as prepended with _, 
        to Generate a random, unique order number using UUID,
        which will be a random strig of 32 characters"""

        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """ Override the original save method to set the order number 
        if it hasn't been set already """

        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)
    
    def update_total(self):
        """ A method to update the total by using the Aggregate() function
        and the Sum() function accross all the line item total fields
        for all line items on this order"""

        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE/100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """ A line item will be like an individual shopping bag item,
    relating to a specific order, and referencing the Product itself """

    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True) #XS, S, M, L, XL
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)

    def save(self, *args, **kwargs):
        """ Multiply the product price by the quantity for each lineitem
        to get the line item total """

        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'


