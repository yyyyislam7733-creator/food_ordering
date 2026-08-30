from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Food, Order


def home(request):
    foods = Food.objects.all()

    return render(
        request,
        'orders/home.html',
        {'foods': foods}
    )


def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return redirect('register')

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                'Username already exists.'
            )

            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            'Registration successful. Please login.'
        )

        return redirect('login')

    return render(
        request,
        'orders/register.html'
    )


def user_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        else:

            messages.error(
                request,
                'Invalid username or password.'
            )

            return redirect('login')

    return render(
        request,
        'orders/login.html'
    )


def user_logout(request):

    logout(request)

    return redirect('home')


def cart(request):

    cart = request.session.get('cart', {})

    foods = Food.objects.filter(
        id__in=cart.keys()
    )

    cart_items = []

    total = 0

    for food in foods:

        quantity = cart.get(
            str(food.id),
            cart.get(food.id, 1)
        )

        item_total = food.price * quantity

        total += item_total

        cart_items.append({
            'food': food,
            'quantity': quantity,
            'item_total': item_total
        })

    return render(
        request,
        'orders/cart.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )


def add_to_cart(request, food_id):

    cart = request.session.get('cart', {})

    food_id = str(food_id)

    if food_id in cart:

        cart[food_id] += 1

    else:

        cart[food_id] = 1

    request.session['cart'] = cart

    request.session.modified = True

    return redirect('cart')


def remove_from_cart(request, food_id):

    cart = request.session.get('cart', {})

    food_id = str(food_id)

    if food_id in cart:

        del cart[food_id]

    request.session['cart'] = cart

    request.session.modified = True

    return redirect('cart')


def decrease_quantity(request, food_id):

    cart = request.session.get('cart', {})

    food_id = str(food_id)

    if food_id in cart:

        cart[food_id] -= 1

        if cart[food_id] <= 0:

            del cart[food_id]

    request.session['cart'] = cart

    request.session.modified = True

    return redirect('cart')


def place_order(request):

    if not request.user.is_authenticated:

        return redirect('login')

    cart = request.session.get('cart', {})

    if not cart:

        return redirect('cart')

    for food_id, quantity in cart.items():

        try:

            food = Food.objects.get(
                id=food_id
            )

            total_price = food.price * quantity

            Order.objects.create(
                customer=request.user,
                food=food,
                quantity=quantity,
                total_price=total_price
            )

        except Food.DoesNotExist:

            continue

    request.session['cart'] = {}

    request.session.modified = True

    return redirect('home')
def my_orders(request):

    if not request.user.is_authenticated:
        return redirect('login')

    orders = Order.objects.filter(
        customer=request.user
    ).order_by('-ordered_at')

    return render(
        request,
        'orders/my_orders.html',
        {
            'orders': orders
        }
    )
def checkout(request):

    if not request.user.is_authenticated:
        return redirect('login')

    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    foods = Food.objects.filter(
        id__in=cart.keys()
    )

    cart_items = []
    total = 0

    for food in foods:

        quantity = cart.get(
            str(food.id),
            1
        )

        item_total = food.price * quantity

        total += item_total

        cart_items.append({
            'food': food,
            'quantity': quantity,
            'item_total': item_total
        })

    if request.method == 'POST':

        customer_name = request.POST.get(
            'customer_name'
        )

        phone = request.POST.get(
            'phone'
        )

        delivery_address = request.POST.get(
            'delivery_address'
        )

        if not customer_name or not phone or not delivery_address:

            messages.error(
                request,
                'Please fill all delivery details.'
            )

            return render(
                request,
                'orders/checkout.html',
                {
                    'cart_items': cart_items,
                    'total': total
                }
            )

        for food_id, quantity in cart.items():

            try:

                food = Food.objects.get(
                    id=food_id
                )

                total_price = food.price * quantity

                Order.objects.create(
                    customer=request.user,
                    food=food,
                    quantity=quantity,
                    total_price=total_price,
                    customer_name=customer_name,
                    phone=phone,
                    delivery_address=delivery_address
                )

            except Food.DoesNotExist:

                continue

        request.session['cart'] = {}
        request.session.modified = True

        messages.success(
            request,
            'Order placed successfully!'
        )

        return redirect('my_orders')

    return render(
        request,
        'orders/checkout.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )