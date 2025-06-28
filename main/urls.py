from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('orders/', views.order_list, name='order_list'),
    path('dishes/<int:pk>/', views.dish_detail, name='dish_detail'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/select/', views.select_dishes, name='select_dishes'),
    path('orders/<int:pk>/delete/', views.delete_order, name='delete_order'),
    path('add_to_cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
]