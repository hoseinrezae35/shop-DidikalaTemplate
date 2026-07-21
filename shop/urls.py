from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path('product-list/', views.ProductListView.as_view(), name="product-list"),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name="product-detail"),
    path('category-detail/<int:pk>/', views.CategoryDetailView.as_view(), name="category-detail"),

]
