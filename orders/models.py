from django.db import models
from django.contrib.auth.models import User


class Food(models.Model):

    CATEGORY_CHOICES = [
        ('Pizza', 'Pizza'),
        ('Burger', 'Burger'),
        ('Chicken', 'Chicken'),
        ('Chinese', 'Chinese'),
        ('Dessert', 'Dessert'),
        ('Drinks', 'Drinks'),
    ]

    name = models.CharField(max_length=100)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='Burger'
    )

    image = models.ImageField(
        upload_to='food/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Order(models.Model):

    customer_name = models.CharField(
    max_length=100,
    default=''
    )

    phone = models.CharField(
    max_length=15,
    default=''
    )

    delivery_address = models.TextField(
    default=''
    )
    customer_name = models.CharField(
    max_length=100
    )

    phone = models.CharField(
    max_length=15
    )

    delivery_address = models.TextField()

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    ordered_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=50,
        default='Pending'
    )
   

    def __str__(self):
        return f"{self.customer.username} - {self.food.name}"