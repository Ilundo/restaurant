from django.contrib import admin
from .models import Category, Dish, Order, Role, UserProfile

admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(Order)
admin.site.register(Role)
admin.site.register(UserProfile)