from rest_framework.permissions import BasePermission

def in_group(user, name):
    return user.is_authenticated and user.groups.filter(name=name).exists()

class IsManager(BasePermission):
    def has_permission(self, request, view): return in_group(request.user, "Manager")

class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view): return request.method in ("GET", "HEAD", "OPTIONS") or in_group(request.user, "Manager")

class IsManagerOrDeliveryCrew(BasePermission):
    def has_permission(self, request, view): return in_group(request.user, "Manager") or in_group(request.user, "Delivery crew")
