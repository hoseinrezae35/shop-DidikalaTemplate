from .cart import CartSession

def cart_session(request):
    cart = CartSession(request.session)
    return {
        "cart_count": cart.get_total_quantity()
    }
