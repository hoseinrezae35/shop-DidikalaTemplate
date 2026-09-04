from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("checkout/", views.OrderView.as_view(), name="checkout"),
    path("create-order/", views.CreateOrderView.as_view(), name="create-order"),
]
