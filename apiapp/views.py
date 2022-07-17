from django.shortcuts import render
from app.models import *
from rest_framework import viewsets
from .serializers import *

# Create your views here.
#SE ENCARGA DE HACER EL QUERY A LA BD
# Y MUESTRA EL QUERY REQUERIDO

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class TipoProductoViewSet(viewsets.ModelViewSet):
    queryset = TipoProducto.objects.all()
    serializer_class = TipoProductoSerializer