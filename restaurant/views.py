from django.contrib.auth.models import Group, User
from django.db import transaction
from django.db.models import Q
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Category, MenuItem, Table, Booking, CartItem, Order, OrderItem
from .permissions import IsManager, IsManagerOrReadOnly, IsManagerOrDeliveryCrew, in_group
from .serializers import *

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all(); serializer_class = RegisterSerializer; permission_classes = [AllowAny]

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.select_related("category").all(); serializer_class = MenuItemSerializer; permission_classes = [IsManagerOrReadOnly]
    def get_queryset(self):
        qs = super().get_queryset(); params = self.request.query_params
        if params.get("category"): qs = qs.filter(category_id=params["category"]) if params["category"].isdigit() else qs.filter(category__name__iexact=params["category"])
        if params.get("featured") in ("true", "false"): qs = qs.filter(featured=params["featured"] == "true")
        if params.get("search"): qs = qs.filter(Q(title__icontains=params["search"]) | Q(description__icontains=params["search"]))
        ordering = params.get("ordering", "title"); return qs.order_by(ordering if ordering.lstrip("-") in ("title", "price") else "title")

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all(); serializer_class = CategorySerializer; permission_classes = [IsManagerOrReadOnly]

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all(); serializer_class = TableSerializer; permission_classes = [IsManager]

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer; permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Booking.objects.all() if in_group(self.request.user, "Manager") else Booking.objects.filter(user=self.request.user)
    def perform_create(self, serializer): serializer.save(user=self.request.user)
    def perform_update(self, serializer):
        if not in_group(self.request.user, "Manager") and serializer.instance.user_id != self.request.user.id: self.permission_denied(self.request)
        serializer.save()

class CartView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer; permission_classes = [IsAuthenticated]
    def get_queryset(self): return CartItem.objects.filter(user=self.request.user).select_related("menu_item", "menu_item__category")
    def perform_create(self, serializer): serializer.save(user=self.request.user)

class CartDeleteView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer; permission_classes = [IsAuthenticated]
    def get_queryset(self): return CartItem.objects.filter(user=self.request.user)

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer; permission_classes = [IsAuthenticated]
    def get_queryset(self):
        qs = Order.objects.prefetch_related("items__menu_item")
        return qs if in_group(self.request.user, "Manager") or in_group(self.request.user, "Delivery crew") else qs.filter(user=self.request.user)
    @action(detail=False, methods=["post"])
    @transaction.atomic
    def checkout(self, request):
        cart = list(CartItem.objects.filter(user=request.user).select_related("menu_item"))
        if not cart: return Response({"detail": "Cart is empty."}, status=400)
        order = Order.objects.create(user=request.user)
        OrderItem.objects.bulk_create([OrderItem(order=order, menu_item=i.menu_item, quantity=i.quantity, unit_price=i.menu_item.price) for i in cart])
        CartItem.objects.filter(user=request.user).delete()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    @action(detail=True, methods=["patch"], permission_classes=[IsManagerOrDeliveryCrew])
    def status(self, request, pk=None):
        order = self.get_object(); new_status = request.data.get("status")
        if new_status not in dict(Order.STATUS_CHOICES): return Response({"detail": "Invalid status."}, status=400)
        order.status = new_status; order.save(update_fields=["status"]); return Response(self.get_serializer(order).data)
