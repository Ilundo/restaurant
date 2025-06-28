from django.contrib import messages
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

def home(request):
    dishes = Dish.objects.filter(availability=True)  
    return render(request, 'home.html', {'dishes': dishes})

def dish_list(request):
    dishes = Dish.objects.all()
    return render(request, 'dishes.html', {'dishes': dishes})

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'order_detail.html', {'order': order})

def dish_detail(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    return render(request, 'dish_detail.html', {'dish': dish})


def cart_view(request):
    return render(request, 'cart.html')
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for dish_id, quantity in cart.items():
        dish = Dish.objects.get(id=dish_id)
        subtotal = dish.price * quantity
        total += subtotal
        items.append({
            'dish': dish,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'cart.html', {'items': items, 'total': total})

def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart = request.session.get('cart', {})

    if str(dish_id) in cart:
        cart[str(dish_id)] += 1
    else:
        cart[str(dish_id)] = 1

    request.session['cart'] = cart
    return redirect('home')


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

@login_required
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.user == order.user or request.user.is_superuser:
        order.delete()
        messages.success(request, "Замовлення видалено.")
    else:
        messages.error(request, "Ви не маєте прав на видалення цього замовлення.")

    return redirect('order_list')