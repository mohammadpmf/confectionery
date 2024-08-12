from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('process_sandbox/', views.payment_process_sandbox, name='payment_process_sandbox'),
    path('callback_sandbox/', views.payment_callback_sandbox, name='payment_callback_sandbox'),
]