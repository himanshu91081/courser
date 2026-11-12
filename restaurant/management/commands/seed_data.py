from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from restaurant.models import Category, MenuItem, Table

class Command(BaseCommand):
    help = "Create demo users, roles, categories, menu items, and tables."
    def handle(self, *args, **kwargs):
        manager, _ = Group.objects.get_or_create(name="Manager")
        crew, _ = Group.objects.get_or_create(name="Delivery crew")
        customer_group, _ = Group.objects.get_or_create(name="Customer")
        for username, group in [("manager", manager), ("delivery", crew), ("customer", customer_group)]:
            user, created = User.objects.get_or_create(username=username, defaults={"email": f"{username}@littlelemon.local"})
            if created: user.set_password("LittleLemon123!"); user.save()
            user.groups.add(group)
        for name in ["Starters", "Mains", "Desserts", "Drinks"]: Category.objects.get_or_create(name=name)
        mains = Category.objects.get(name="Mains"); starters = Category.objects.get(name="Starters")
        for title, price, category in [("Greek Salad", 12, starters), ("Bruschetta", 9, starters), ("Lamb Chops", 25, mains), ("Grilled Fish", 22, mains)]:
            MenuItem.objects.get_or_create(title=title, defaults={"price": price, "category": category, "description": f"Fresh Little Lemon {title.lower()}."})
        for number, capacity in [(1, 2), (2, 4), (3, 6), (4, 8)]: Table.objects.get_or_create(number=number, defaults={"capacity": capacity})
        self.stdout.write(self.style.SUCCESS("Demo data created. Password for demo users: LittleLemon123!"))
