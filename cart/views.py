from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View, TemplateView

from shop.models import Product
from .cart import CartSession


class AddToCartView(View):

    def post(self, request, *args, **kwargs):

        product_id = request.POST.get("product_id")

        if not product_id:
            return JsonResponse({
                "success": False,
                "message": "محصول نامعتبر است."
            }, status=400)

        product = get_object_or_404(
            Product,
            pk=product_id,
            is_available=True
        )

        cart = CartSession(request.session)
        cart.add_product(product.id)

        if request.user.is_authenticated:
            cart.sync_session_cart_to_db(request.user)

        return JsonResponse({
            "success": True,
            "message": "محصول با موفقیت به سبد خرید اضافه شد.",
            "total_quantity": cart.get_total_quantity(),
            "cart_total": cart.get_total_payment_amount(),
        })


class UpdateCartView(View):

    def post(self, request):

        product_id = request.POST.get("product_id")
        action = request.POST.get("action")

        if not product_id or action not in ["increase", "decrease"]:
            return JsonResponse({
                "success": False,
                "message": "درخواست نامعتبر است."
            }, status=400)

        product = get_object_or_404(
            Product,
            pk=product_id,
            is_available=True
        )

        cart = CartSession(request.session)

        cart_item = next(
            (
                item for item in cart.get_cart_dict()["items"]
                if item["product_id"] == product.id
            ),
            None
        )

        if cart_item is None:
            return JsonResponse({
                "success": False,
                "message": "محصول در سبد خرید وجود ندارد."
            }, status=404)

        quantity = cart_item["quantity"]

        if action == "increase":

            quantity += 1

        else:
            quantity -= 1

        if quantity <= 0:

            cart.remove_product(product.id)

            if request.user.is_authenticated:
                cart.sync_session_cart_to_db(request.user)

            return JsonResponse({

                "success": True,

                "deleted": True,

                "product_id": product.id,

                "cart_count": cart.get_total_quantity(),

                "cart_total": cart.get_total_payment_amount(),

                "message": "محصول از سبد خرید حذف شد."

            })

        cart.update_product_quantity(product.id, quantity)

        if request.user.is_authenticated:
            cart.sync_session_cart_to_db(request.user)

        return JsonResponse({

            "success": True,

            "deleted": False,

            "product_id": product.id,

            "quantity": quantity,

            "item_total": quantity * product.final_price,

            "cart_total": cart.get_total_payment_amount(),

            "cart_count": cart.get_total_quantity(),

        })


class SessionCartSummaryView(TemplateView):
    template_name = "cart/cart-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = CartSession(self.request.session)

        context["cart_items"] = cart.get_cart_item()
        context["cart_count"] = cart.get_total_quantity()
        context["total_payment_price"] = cart.get_total_payment_amount()

        return context
