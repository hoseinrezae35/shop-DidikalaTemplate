from django.urls import path

from . import views


app_name = "dashboard"


urlpatterns = [
    path("costumer/", views.DashboardView.as_view(),name="index"),
    path("costumer/address", views.DashboardUserAddressView.as_view(),name="costumer-address"),
]
