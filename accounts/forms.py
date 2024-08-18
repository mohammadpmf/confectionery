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
        fields = ('email', 'password')

    def clean_password(self):
        data:str = self.cleaned_data["password"]
        if len(data)<8:
            raise ValidationError(_("Password must be at least 8 characters"))
        if data.isalpha():
            raise ValidationError(_("Password must have at least one digit"))
        if data.isdigit():
            raise ValidationError(_("Password can not be only a number"))
        return data


class ChangeUserProfileInWebsiteForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'nat_code', 'gender', 'phone_number']
    # GENDER_CHOICES =(
    #     ('', _('')),
    #     ('f', _('Female')),
    #     ('m', _('Male')),
    # )

    # first_name = forms.CharField(label=_('First Name'), max_length=255, required=False)
    # last_name = forms.CharField(label=_('Last Name'), max_length=255, required=False)
    # nat_code = forms.CharField(label=_('National Code'), min_length=10, max_length=10, required=False)
    # gender = forms.ChoiceField(label=_('Gender'), choices=GENDER_CHOICES, required=False)
    # phone_number = forms.CharField(label=_('Phone Number'), min_length=11, max_length=14, required=False)
    profile_picture = forms.ImageField(label=_('Profile Picture'), required=False)
    remove_profile_picture = forms.BooleanField(label=_('Remove Profile Picture'), required=False)


class ChangeUsersUsernameInWebsiteForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username']


class ChangeUsersEmailAddressInWebsiteForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']

    username = forms.CharField(label=_('Username'), disabled=True, min_length=1, max_length=255)


class ChangeUsersOTPNumberInWebsiteForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'phone_number']

    username = forms.CharField(label=_('Username'), disabled=True, min_length=1, max_length=255)
    phone_number = forms.CharField(label=_('Old Phone Number'), disabled=True)
    otp_phone_number = forms.CharField(label=_('OTP Phone Number'), min_length=11, max_length=11, error_messages={
        'required' : _('Enter phone number!'),
        'min_value' : _("Phone number should be exactly 11 digits to get verification code"),
        'max_value' : _("Phone number should be exactly 11 digits to get verification code"),
    })
