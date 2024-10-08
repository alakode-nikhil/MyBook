from .models import Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        cart,_ = Cart.objects.get_or_create(user =request.user)
        cart_item_count = cart.cartitem_set.count()
        return {'cart_item_count':cart_item_count}
    
    return{'cart_item_count':0}

            