from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    """
    Give Store owners/superusers the ability to add, update and delete products

    """
    class Meta:
        """
        This inner metaclass will define the Model and the fields
        we want to include
        """

        model = Product
        fields = '__all__'

        def __init__(self, *args, **kwargs):

            # override the init() to make changes to some fields

            super().__init__(*args, **kwargs)
            categories = Category.objects.all()
            friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

            # now that we have the friendly names, update the category 
            # field on the form to display those to the user to choose 
            # from instead ofusing the id.

            self.fields['category'].choices = friendly_names
            for field_name, filed in self.fields.items():
                field.widget.attrs['class'] = 'border-black rounded-0'
