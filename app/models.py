from distutils.command.upload import upload
from email.policy import default
from tkinter import CASCADE
from django.shortcuts import reverse
from django.db import models
from django.forms import BooleanField, IntegerField, PasswordInput
from django.conf import settings
# Create your models here.


class TipoUsuario(models.Model):
    tipo_usuario = models.CharField(max_length=20)

    def __str__(self):
        return self.tipo_usuario

    class Meta:
        db_table = 'tipo_usuario'


class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=40)
    apellido_usuario = models.CharField(max_length=40)
    username = models.CharField(max_length=20)
    contraseña_usuario = models.CharField(max_length=30)
    correo_usuario = models.CharField(max_length=100)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'usuario'


class TipoProducto(models.Model):
    tipo_producto = models.CharField(max_length=40)

    def __str__(self):
        return self.tipo_producto
    
    class Meta:
        db_table = 'tipo_producto'
    

class Producto(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=40)
    precio = models.IntegerField()
    stock = models.IntegerField(default=1)
    precio_descuento = models.IntegerField(blank=True, null=True)
    descripcion = models.TextField()
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="productosimg", null=True)
    fecha_ingreso = models.DateField()
    slug = models.SlugField()

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("tienda", kwargs={
            'slug': self.slug
        })

    def get_agregar_carrito_url(self):
        return reverse("agregar_carrito", kwargs={
            'slug': self.slug
        })
    
    def get_borrar_carrito_url(self):
        return reverse("borrar_carrito", kwargs={
            'slug': self.slug
        })



    class Meta:
        db_table = 'producto'


class Carrito(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Producto, on_delete = models.CASCADE)
    cantidad = models.IntegerField(default=1)
    compra = models.BooleanField(default = False)



    def __str__(self):
        return f"{self.cantidad} de {self.item.nombre}"

    def get_precio_total_producto(self):
        return self.cantidad * self.item.precio

    def get_precio_descuento_total_producto(self):
        return self.cantidad * self.item.precio_descuento

    def get_monto_descuento(self):
        return self.get_precio_total_producto() - self.get_precio_descuento_total_producto()

    def get_precio_final(self):
        if self.item.precio_descuento:
            return self.get_precio_descuento_total_producto
        return self.get_precio_total_producto()


    class Meta:
        db_table = 'carrito'


class Orden(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(Carrito)
    fecha = models.DateTimeField(auto_now_add = True)
    fecha_compra = models.DateTimeField()
    compra = models.BooleanField(default = False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for orden_item in self.items.all():
            total += orden_item.get_precio_final()
        return total


    class Meta:
        db_table = 'orden'
    
    
class Subscripcion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sub = models.BooleanField(default = False)

    def __str__(self):
        return self.user.username


# python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser