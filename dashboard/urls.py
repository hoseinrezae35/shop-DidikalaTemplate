from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("costumer/", views.DashboardView.as_view(), name="index"),
    path("address-list/", views.AddressListView.as_view(), name="address-list"),
    path("addresses/<int:pk>/delete/", views.AddressDeleteView.as_view(), name="address-delete"),
    path("addresses/<int:pk>/edit/", views.AddressUpdateView.as_view(), name="address-edit"),
    path("profile-edit/", views.UserProfileUpdateView.as_view(), name="user-profile"),

]
