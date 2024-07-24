from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model


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