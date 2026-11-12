from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, MenuItem, Table, Booking, CartItem, Order, OrderItem

class UserSerializer(serializers.ModelSerializer):
    class Meta: model = User; fields = ["id", "username", "email"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta: model = User; fields = ["username", "email", "password"]
    def create(self, validated_data): return User.objects.create_user(**validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta: model = Category; fields = ["id", "name"]

class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    class Meta: model = MenuItem; fields = ["id", "title", "description", "price", "category", "category_name", "featured"]

class TableSerializer(serializers.ModelSerializer):
    class Meta: model = Table; fields = ["id", "number", "capacity"]

class BookingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    class Meta: model = Booking; fields = ["id", "user", "username", "table", "date", "time", "guests", "status", "created_at"]; read_only_fields = ["user", "status"]
    def validate_guests(self, value):
        if not 1 <= value <= 20: raise serializers.ValidationError("Guests must be between 1 and 20.")
        return value

class CartItemSerializer(serializers.ModelSerializer):
    menu_item_detail = MenuItemSerializer(source="menu_item", read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta: model = CartItem; fields = ["id", "menu_item", "menu_item_detail", "quantity", "total"]; read_only_fields = ["user"]

class OrderItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="menu_item.title", read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta: model = OrderItem; fields = ["id", "menu_item", "title", "quantity", "unit_price", "total"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta: model = Order; fields = ["id", "user", "status", "items", "total", "created_at"]; read_only_fields = ["user", "status"]
