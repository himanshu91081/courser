from django.conf import settings
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name

class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="menu_items")
    featured = models.BooleanField(default=False)
    def __str__(self): return self.title

class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField()
    def __str__(self): return f"Table {self.number} ({self.capacity})"

class Booking(models.Model):
    STATUS_CHOICES = [("confirmed", "Confirmed"), ("cancelled", "Cancelled")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True, related_name="bookings")
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="confirmed")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["date", "time"]

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    class Meta:
        ordering = ["id"]
        constraints = [models.UniqueConstraint(fields=["user", "menu_item"], name="unique_cart_item")]
    @property
    def total(self): return self.menu_item.price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = [("pending", "Pending"), ("preparing", "Preparing"), ("out_for_delivery", "Out for delivery"), ("delivered", "Delivered")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created_at"]
    @property
    def total(self): return sum(item.total for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    @property
    def total(self): return self.unit_price * self.quantity
