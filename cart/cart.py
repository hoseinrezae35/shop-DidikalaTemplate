from shop.models import Product
from .models import CartModel, CartItemModel


class CartSession:

    def __init__(self, session):
        self.session = session
        self._cart = self.session.setdefault("cart", {"items": []})

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session["cart"] = {"items": []}
        self._cart = self.session["cart"]
        self.save()

    def get_cart_dict(self):
        return self._cart

    # -------------------------
    # Add Product
    # -------------------------
    def add_product(self, product_id):

        product_id = int(product_id)

        for item in self._cart["items"]:
            if item["product_id"] == product_id:
                item["quantity"] += 1
                self.save()
                return

        self._cart["items"].append({
            "product_id": product_id,
            "quantity": 1
        })

        self.save()

    # -------------------------
    # Update Quantity
    # -------------------------
    def update_product_quantity(self, product_id, quantity):

        product_id = int(product_id)
        quantity = int(quantity)

        if quantity <= 0:
            return self.remove_product(product_id)

        for item in self._cart["items"]:

            if item["product_id"] == product_id:
                item["quantity"] = quantity
                break

        self.save()

    # -------------------------
    # Remove Product
    # -------------------------
    def remove_product(self, product_id):

        product_id = int(product_id)

        self._cart["items"] = [
            item
            for item in self._cart["items"]
            if item["product_id"] != product_id
        ]

        self.save()

    # -------------------------
    # Total Quantity
    # -------------------------
    def get_total_quantity(self):

        return sum(
            item["quantity"]
            for item in self._cart["items"]
        )

    # -------------------------
    # Cart Items
    # -------------------------
    def get_cart_item(self):

        product_ids = [
            item["product_id"]
            for item in self._cart["items"]
        ]

        products = Product.objects.filter(
            id__in=product_ids,
            is_available=True
        )

        products = {
            product.id: product
            for product in products
        }

        items = []

        for item in self._cart["items"]:

            product = products.get(item["product_id"])

            if not product:
                continue

            items.append({

                "product_obj": product,

                "quantity": item["quantity"],

                "total_price": product.final_price * item["quantity"]

            })

        return items

    # -------------------------
    # Total Payment
    # -------------------------
    def get_total_payment_amount(self):

        return sum(
            item["total_price"]
            for item in self.get_cart_item()
        )

    # -------------------------
    # Merge Session -> Database
    # -------------------------
    def merge_session_cart_in_db(self, user):
        cart, _ = CartModel.objects.get_or_create(user=user)

        for item in self._cart["items"]:

            product = Product.objects.filter(
                id=item["product_id"],
                is_available=True
            ).first()

            if not product:
                continue

            cart_item, created = CartItemModel.objects.get_or_create(
                cart=cart,
                product=product
            )

            if created:
                cart_item.quantity = item["quantity"]
            else:
                cart_item.quantity += item["quantity"]

            cart_item.save()

    def sync_session_cart_to_db(self, user):

        cart, _ = CartModel.objects.get_or_create(user=user)

        session_products = []

        for item in self._cart["items"]:

            product = Product.objects.filter(
                id=item["product_id"],
                is_available=True
            ).first()

            if not product:
                continue

            session_products.append(product.id)

            cart_item, _ = CartItemModel.objects.get_or_create(
                cart=cart,
                product=product
            )

            cart_item.quantity = item["quantity"]
            cart_item.save()

        CartItemModel.objects.filter(
            cart=cart
        ).exclude(
            product_id__in=session_products
        ).delete()

    def sync_cart_items_from_db(self, user):

        cart = CartModel.objects.get(user=user)

        self.clear()

        for cart_item in cart.cart_items.select_related("product"):

            if not cart_item.product.is_available:
                continue

            self._cart["items"].append({
                "product_id": cart_item.product.id,
                "quantity": cart_item.quantity
            })

        self.save()
