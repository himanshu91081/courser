from django.contrib import admin
from .models import Category, MenuItem, Table, Booking, CartItem, Order, OrderItem
admin.site.register([Category, MenuItem, Table, Booking, CartItem, Order, OrderItem])
