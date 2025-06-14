from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('orders/', views.order_list, name='order_list'), 
]
