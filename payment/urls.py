from django.urls import path

from . import views

app_name = 'payment'


urlpatterns = [
    path('process_sandbox/', views.payment_process_sandbox, name='payment_process_sandbox'),
    path('callback_sandbox/', views.payment_callback_sandbox, name='payment_callback_sandbox'),
]


########################### az_iranian_bank_gateways ###########################
# نصبش کردم. اما درست کار نمیکرد کامنت کردم. کدهاش رو حذف نکردم.
# urlpatterns = [
#     path('process_sandbox/', views.go_to_gateway_view, name='payment_process_sandbox'),
#     path('callback_sandbox/', views.callback_gateway_view, name='payment_callback_sandbox'),
# ]
