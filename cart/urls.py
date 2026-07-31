from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path('cart-list', views.SessionCartSummaryView.as_view(), name="cart_list"),
    path("add", views.AddToCartView.as_view(), name="add_to_cart"),
    path("update/",views.UpdateCartView.as_view(),name="update_cart"),
]
