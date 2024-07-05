from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    inventory = models.IntegerField()
    unit_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self) -> str:
        return self.title


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Address(models.Model):
    city = models.CharField(max_length=255)
    postal_code = models.IntegerField()
    full_address = models.TextField()

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='addresses')

    def __str__(self) -> str:
        return f"{self.customer} --- city: {self.city} --- address: {self.full_address[:30]}"


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='carts')

    def __str__(self) -> str:
        return f"{self.customer} - {self.created_at}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='carts')

    quantity = models.PositiveIntegerField()


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = {
        PAYMENT_STATUS_PENDING: 'Pending',
        PAYMENT_STATUS_COMPLETE: 'Complete',
        PAYMENT_STATUS_FAILED: 'Failed'
    }
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name='orders')

    def __str__(self) -> str:
        return f"{self.customer} - {self.created_at} - {self.payment_status}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='orders')
    quantity = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()


class Review(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self) -> str:
        return f"{self.product} - {self.customer} - {self.title}"
