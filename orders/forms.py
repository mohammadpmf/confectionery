from django import forms
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from string import punctuation

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
    phone_number = forms.CharField(label=_('Phone Number'), min_length=11, max_length=11, error_messages={
        'required' : _('Enter phone number!'),
        'min_value' : _("Phone number should be exactly 11 digits in Iran"),
        'max_value' : _("Phone number should be exactly 11 digits in Iran"),
    })

    def clean_phone_number(self):
        data:str = self.cleaned_data["phone_number"]
        if data.isalpha():
            raise ValidationError(_("Phone number must only contain digits (not alphabet characters!)"))
        if data.startswith("09"):
            for char in data[2:]:
                if char in punctuation:
                    raise ValidationError(_("Phone number must only contain digits (not punctuations!)"))
                if char not in '0123456789':
                    raise ValidationError(_("Please enter all digits number carefully and only in english keyboard!"))
        else:
            raise ValidationError(_("Phone numbers start with 09 in Iran!"))
        return data
    
    