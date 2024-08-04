from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('category/<category>/', views.CategoryList.as_view(), name='categories'),
    path('product/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('my_favorites/', views.FavoriteList.as_view(), name='my_favorites'),
]
