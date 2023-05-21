from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """ display the OrderLineItem model fields within the same page displaying the Order model fields"""

    model = OrderLineItem
    readonly_fields = ('lineitem_total',)

class OrderAdmin(admin.ModelAdmin):
    """ Set up the Admin view of the fields in Order model """

    inlines = (OrderLineItemAdminInline,)

    # these will all be calculated by our model methods so we don't want anyone to change them
    readonly_fields = (
        'order_number',
        'date',
        'delivery_cost',
        'order_total',
        'grand_total',
        'original_bag',
        'stripe_pid',
    )

    # not 'strictly' necessary to do the following, but if you want your fields in a specific order you should do this
    fields = (
        'order_number',
        'date',
        'user_profile',
        'full_name',
        'email',
        'phone_number',
        'country',
        'post_code',
        'town_or_city',
        'street_address1',
        'street_address2',
        'county',
        'delivery_cost',
        'order_total',
        'grand_total',
        'original_bag',
        'stripe_pid',
    )

    list_display = (
        'order_number',
        'date',
        'full_name',
        'order_total',
        'delivery_cost',
        'grand_total',
    )

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)