from django.urls import path

from . import views


urlpatterns = [
    path('accounts/madval_logout/', views.MadvalLogout.as_view(), name='madval_logout'),
    path('accounts/logout_confirm/', views.LogoutConfirm.as_view(), name='logout_confirm'),
    path('accounts/login_with_phone_number/', views.LoginWithPhoneNumber.as_view(), name='login_with_phone_number'),
    path('accounts/register_with_phone_number/', views.RegisterWithPhoneNumber.as_view(), name='register_with_phone_number'),
    path('accounts/change_profile/', views.ChangeProfile.as_view(), name='change_profile'),
    path('accounts/change_username/', views.ChangeUsername.as_view(), name='change_username'),
    path('accounts/change_email/', views.ChangeEmailAddress.as_view(), name='change_email'),
    path('accounts/change_otp_number/', views.ChangeOTPNumber.as_view(), name='change_otp_number'),
    path('accounts/change_otp_number/confirm/', views.ChangeOTPNumberConfirm.as_view(), name='verify_otp_phone_number_for_change'),
]
