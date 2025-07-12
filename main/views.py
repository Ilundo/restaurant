from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from .models import Dish, Order, Category
from .forms import OrderForm,DishForm




def home(request):
    dishes = Dish.objects.filter(availability=True)
    return render(request, 'home.html', {'dishes': dishes})




@login_required
def profile_view(request):
    return render(request, 'profile.html', {
        'user': request.user,
        'profile': request.user.userprofile,
    })


def dish_list(request):
    dishes = Dish.objects.all()
    return render(request, 'dishes.html', {'dishes': dishes})

def dish_detail(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    return render(request, 'dish_detail.html', {'dish': dish})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

def category_dishes(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    dishes = Dish.objects.filter(category=category, availability=True)
    return render(request, 'category_dishes.html', {'category': category, 'dishes': dishes})



def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for dish_id, quantity in cart.items():
        try:
            dish = Dish.objects.get(id=dish_id)
            subtotal = dish.price * quantity
            total += subtotal
            items.append({
                'dish': dish,
                'quantity': quantity,
                'subtotal': subtotal,
            })
        except Dish.DoesNotExist:
            continue

    return render(request, 'cart.html', {'items': items, 'total': total})


def add_to_cart(request, dish_id):
    cart = request.session.get('cart', {})
    cart[str(dish_id)] = cart.get(str(dish_id), 0) + 1
    request.session['cart'] = cart
    return redirect('home')


def increase_quantity(request, dish_id):
    cart = request.session.get('cart', {})
    if str(dish_id) in cart:
        cart[str(dish_id)] += 1
    request.session['cart'] = cart
    return redirect('cart')


def decrease_quantity(request, dish_id):
    cart = request.session.get('cart', {})
    if str(dish_id) in cart:
        cart[str(dish_id)] -= 1
        if cart[str(dish_id)] <= 0:
            del cart[str(dish_id)]
    request.session['cart'] = cart
    return redirect('cart')


@login_required
def checkout_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for dish_id, quantity in cart.items():
        dish = get_object_or_404(Dish, id=dish_id)
        subtotal = dish.price * quantity
        total += subtotal
        items.append({'dish': dish, 'quantity': quantity, 'subtotal': subtotal})

    return render(request, 'checkout.html', {'items': items, 'total': total})


@login_required
def order_form_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Кошик порожній.")
        return redirect('home')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(user=request.user)
            for dish_id, quantity in cart.items():
                dish = get_object_or_404(Dish, id=dish_id)
                for _ in range(quantity):
                    order.dish.add(dish)
            order.save()
            request.session['cart'] = {}
            messages.success(request, "Замовлення успішно створене!")
            return redirect('home')
    else:
        form = OrderForm()

    return render(request, 'order_form.html', {'form': form})


@login_required
def order_list(request):
    if request.user.is_staff:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'order_detail.html', {'order': order})


@login_required
def dish_create(request):
    if not request.user.userprofile.role.name == 'admin':
        raise PermissionDenied("У вас немає доступу до цієї сторінки")

    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Страва додана!")
            return redirect('home')
    else:
        form = DishForm()

    return render(request, 'dish_create.html', {'form': form})

@login_required
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.user == order.user or request.user.is_superuser:
        order.delete()
        messages.success(request, "Замовлення видалено.")
    else:
        messages.error(request, "Ви не маєте прав на видалення цього замовлення.")

    return redirect('order_list')


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
