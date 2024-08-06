from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('category/<category>/', views.CategoryList.as_view(), name='categories'),
    path('product/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('my_favorites/', views.FavoriteList.as_view(), name='my_favorites'),
    path('all_products/', views.ProductList.as_view(), name='all_products'),
    path('about_us/', views.AboutUs.as_view(), name='about_us'),
    path('contact_us/', views.ContactUs.as_view(), name='contact_us'),
]
