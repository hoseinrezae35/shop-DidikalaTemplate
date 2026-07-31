from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .cart import CartSession


@receiver(user_logged_in)
def merge_cart_after_login(sender, request, user, **kwargs):

    cart = CartSession(request.session)

    cart.merge_session_cart_in_db(user)

    cart.sync_cart_items_from_db(user)