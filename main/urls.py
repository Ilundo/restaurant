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
    path('cart/increase/<int:dish_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:dish_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-form/', views.order_form_view, name='order_form'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.category_dishes, name='category_dishes'),
]