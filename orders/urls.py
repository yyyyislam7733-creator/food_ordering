from django.urls import path
from . import views

urlpatterns = [
    path(
    'checkout/',
    views.checkout,
    name='checkout'
),
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),

    path('login/', views.user_login, name='login'),

    path('logout/', views.user_logout, name='logout'),

    path('cart/', views.cart, name='cart'),

    path(
        'add-to-cart/<int:food_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'remove-from-cart/<int:food_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'decrease-quantity/<int:food_id>/',
        views.decrease_quantity,
        name='decrease_quantity'
    ),

    path(
        'place-order/',
        views.place_order,
        name='place_order'
    ),

    path(
        'my-orders/',
        views.my_orders,
        name='my_orders'
    ),
]