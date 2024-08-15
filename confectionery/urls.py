from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('category/<category>/', views.CategoryList.as_view(), name='categories'),
    path('product/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('my_favorites/', views.FavoriteList.as_view(), name='my_favorites'),
    path('all_products/', views.ProductList.as_view(), name='all_products'),
    path('about_us/', views.AboutUs.as_view(), name='about_us'),
    path('about_me/', views.AboutMe.as_view(), name='about_me'),
    path('contact_us/', views.ContactUs.as_view(), name='contact_us'),
    path('chefs/', views.ChefList.as_view(), name='chefs'),
    path('my_orders/', views.MyOrdersList.as_view(), name='my_orders'),
    path('my_orders/<int:pk>/', views.MyOrdersDetail.as_view(), name='my_orders_detail'),
]
