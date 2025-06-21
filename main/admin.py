from django.contrib import admin
from .models import Category, Dish, Basket, Order

admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(Basket)
admin.site.register(Order)
