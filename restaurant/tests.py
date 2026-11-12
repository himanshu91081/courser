from datetime import date, time, timedelta
from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Category, MenuItem

class APIWorkflowTests(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user("customer", password="password123")
        self.manager = User.objects.create_user("manager", password="password123")
        Group.objects.create(name="Manager").user_set.add(self.manager)
        category = Category.objects.create(name="Mains")
        MenuItem.objects.create(title="Lamb Chops", price=25, category=category)
    def auth(self, user): self.client.force_authenticate(user=user)
    def test_customer_can_read_menu_but_cannot_write(self):
        self.auth(self.customer)
        self.assertEqual(self.client.get("/api/menu-items/").status_code, 200)
        self.assertEqual(self.client.post("/api/menu-items/", {"title": "Soup", "price": 8}).status_code, 403)
    def test_manager_can_create_menu_item(self):
        self.auth(self.manager)
        response = self.client.post("/api/menu-items/", {"title": "Soup", "price": "8.00"})
        self.assertEqual(response.status_code, 201)
    def test_customer_cart_checkout_clears_cart(self):
        self.auth(self.customer)
        item = MenuItem.objects.first()
        self.assertEqual(self.client.post("/api/cart/", {"menu_item": item.id, "quantity": 2}).status_code, 201)
        response = self.client.post("/api/orders/checkout/")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["total"], "50.00")
        self.assertEqual(self.client.get("/api/cart/").data["count"], 0)
    def test_customer_can_create_booking(self):
        self.auth(self.customer)
        response = self.client.post("/api/bookings/", {"date": str(date.today() + timedelta(days=1)), "time": "19:00", "guests": 2})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["username"], "customer")
