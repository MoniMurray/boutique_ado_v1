from django import forms
from .models import Order 

class Orderform(forms.ModelForm):

    class Meta:
        model = Order
        fields = (
            'full_name',
            'email',
            'phone_number',
            'street_address1',
            'street_address2',
            'town_or_city',
            'post_code',
            'country',
            'county',
            )

    def __init__(self, *args, **kwargs):

        """Add placeholders and classes, remove auto-generated labels, 
        and set autofocus on first field """

        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'street_address1': 'Street Address Line 1',
            'street_address2': 'Street Address Line 2',
            'town_or_city': 'Town or City',
            'post_code': 'Postal Code',
            'country': 'Country',
            'county': 'County',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False