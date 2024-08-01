from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('nat_code', 'gender', 'phone_number')
        # fields = ['username', 'email', 'phone_number', 'first_name', 'last_name', 'email', 'nat_code', 'gender', 'phone_number', 'username']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = UserChangeForm.Meta.fields
        # fields = ('username', 'email', 'phone_number')


class ChangeUserInfoAfterRegisterationForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')

    def clean_password(self):
        data:str = self.cleaned_data["password"]
        if len(data)<8:
            raise ValidationError(_("Password must be at least 8 characters"))
        if data.isalpha():
            raise ValidationError(_("Password must have at least one digit"))
        if data.isdigit():
            raise ValidationError(_("Password can not be only a number"))
        return data
