from django.db import models


class CartModel(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    def calculate_total_price(self):
        return sum(item.product.final_price * item.quantity for item in self.cart_items.all())


class CartItemModel(models.Model):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey('shop.Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_cart_product"
            )
        ]

    def __str__(self):
        return f"{self.product.name} - {self.cart.id}"
