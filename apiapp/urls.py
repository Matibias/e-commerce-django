from django.urls import path, include
from rest_framework import routers
from .views import *

#INDICA LA RUTA DE LLAMADO DEL API
router = routers.DefaultRouter()
router.register('producto', ProductoViewSet)
router.register('tipoproducto', TipoProductoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]