from django import template
from app.models import *

register = template.Library()


#@register.filter
#def cart_item_count(user):
#    if user.is_authenticated:
#        qs = Orden.objects.filter(user=user, ordered=False)
#        if qs.exists():
#            return qs[0].items.count()
#    return 0

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        orden_activa = Orden.objects.filter(user=user, compra=False)
        if orden_activa.exists():
            qs = Carrito.objects.filter(user=user, compra=False)
            if qs.exists():
                count = 0
                for item in qs:
                    count += item.cantidad
                return count
        count = 0
        return count
    return 0