from django.shortcuts import get_object_or_404, redirect, render
from .models import Dish, Order
from django.contrib.auth.decorators import login_required
def home(request):
    return render(request, 'home.html') 

@login_required
def order_list(request):
    if request.user.is_staff:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})

def dish_list(request):
    dishes = Dish.objects.all()
    return render(request, 'dishes.html', {'dishes': dishes})

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'order_detail.html', {'order': order})

def select_dishes(request):
    dishes = Dish.objects.all()

    if request.method == 'POST':
        selected_ids = request.POST.getlist('dishes')
        if selected_ids:
            order = Order.objects.create(user=request.user)
            order.dish.set(Dish.objects.filter(id__in=selected_ids))
            order.save()
            return redirect('order_list')

    return render(request, 'select_dishes.html', {'dishes': dishes})