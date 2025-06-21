from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/select/', views.select_dishes, name='select_dishes'),
]