from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class CustomClearableFileInput(ClearableFileInput):
    """
    Our custom file inherits the built-in django file
    """

    # override the clear checkbox label
    clear_checkbox_label = _('Remove')
    # give the following variables our own custom values
    initial_text = _('Current Image')
    input_text = _('')
    template_name = 'products/custom_widget_templates/custom_clearable_file_input.html'
