from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import RegisterView, MenuItemViewSet, CategoryViewSet, TableViewSet, BookingViewSet, CartView, CartDeleteView, OrderViewSet

router = DefaultRouter()
router.register("menu-items", MenuItemViewSet, basename="menu-item")
router.register("categories", CategoryViewSet, basename="category")
router.register("tables", TableViewSet, basename="table")
router.register("bookings", BookingViewSet, basename="booking")
router.register("orders", OrderViewSet, basename="order")
urlpatterns = [path("", include(router.urls)), path("auth/register/", RegisterView.as_view()), path("cart/", CartView.as_view()), path("cart/<int:pk>/", CartDeleteView.as_view())]
