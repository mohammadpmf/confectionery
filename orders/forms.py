from django import forms
from django.utils.translation import gettext as _

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone_number', 'address', 'order_notes']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'order_notes': forms.Textarea(attrs={'rows': 5, 'placeholder': _("Please Enter any further notes if you have some. Otherwise leave theis field empty.")}),
        }
    
    change_name = forms.BooleanField(label=_("Also change first_name and last_name of my account."), required=False)
