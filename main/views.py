from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Order

def home(request):
    return render(request, 'home.html') 

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders.html', {'orders': orders})
