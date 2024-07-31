from django.urls import path

from . import views


urlpatterns = [
    path('accounts/login_with_phone_number/', views.LoginWithPhoneNumber.as_view(), name='login_with_phone_number'),
]
