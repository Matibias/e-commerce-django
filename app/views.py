from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import requests
from .models import *
from django.contrib.auth.models import Group
from django.conf import settings
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin


# CRUD PRODUCTO.

def agregarproducto(request):

    data = {
        'form' : ProductoForm()
    }
    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,'Producto guardado correctamente!')
            #data['mensaje'] = 'Producto guardado correctamente!'

            data['form'] = formulario
    return render(request, "app/productos/agregar_producto.html", data)

def listarproducto(request):

    productosAll = Producto.objects.all()
    datos = {
        'listaProductos' : productosAll
    }
    return render(request, "app/productos/listarproducto.html", datos)

def modificarProducto(request, id):

    productoAux = Producto.objects.get(codigo=id)
    data = {
        'form' : ProductoForm(instance=productoAux)
    }
    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES,instance=productoAux)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,'Producto modificado correctamente!')
            #data['mensaje'] = 'Producto modificado correctamente!'
            data['form'] = formulario

    return render(request, "app/productos/modificarProducto.html", data)

def eliminarproducto(request, id):
    productoAux = Producto.objects.get(codigo=id)
    productoAux.delete()
    
    return redirect(to="listarproducto")


# CRUD USUARIO.

def agregarusuario(request):

    data = {
        'form' : UsuarioForm()
    }
    if request.method == 'POST':
        formulario = UsuarioForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,'Usuario creado exitosamente!')
            #data['mensaje'] = 'Producto guardado correctamente!'
            data['form'] = formulario
    return render(request, "app/usuarios/agregar_usuario.html", data)

def listarusuario(request):

    productosAll = Usuario.objects.all()
    datos = {
        'listaUsuario' : productosAll
    }
    return render(request, "app/usuarios/listar_usuario.html", datos)

def modificarusuario(request, id):

    usuarioAux = Usuario.objects.get(id=id)
    data = {
        'form' : UsuarioForm(instance=usuarioAux)
    }
    if request.method == 'POST':
        formulario = UsuarioForm(request.POST, files=request.FILES,instance=usuarioAux)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,'Usuario modificado correctamente!')
            #data['mensaje'] = 'Producto modificado correctamente!'
            data['form'] = formulario

    return render(request, "app/usuarios/modificar_usuario.html", data)

def eliminarusuario(request, id):
    usuarioAux = Usuario.objects.get(id=id)
    usuarioAux.delete()
    
    return redirect(to="listarusuario")


#VISTAS TIENDA

class HomeView(ListView):
    model = Producto
    template_name = 'app/index.html'

class TiendaDetailView(DetailView):
    model = Producto
    template_name = 'app/tienda.html'

 
class CarritoDetailView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            orden = Orden.objects.get(user=self.request.user, compra=False)
            context = {
                'object': orden
            }
            return render(self.request, 'app/carrito.html', context)
        except ObjectDoesNotExist:
            #messages.warning(self.request, "You do not have an active order")
            return redirect("/")

class CompraCarritoView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        #form
        try:
            orden = Orden.objects.get(user=self.request.user, compra=False)
            context = {
                'object': orden
            }
            return render(self.request, 'app/compra.html', context)
        except ObjectDoesNotExist:
            #messages.warning(self.request, "You do not have an active order")
            return redirect("/")
        


def registro_usuarios(request):
    data = {
        'form' : RegistroUsuarioForm()
    }
    if request.method == 'POST':
        formulario = RegistroUsuarioForm(data=request.POST)
        if formulario.is_valid():
            user = formulario.save()
            group = Group.objects.get(name='cliente')
            user.groups.add(group)
            #user = authenticate(username=formulario.cleaned_data["username"],password=formulario.cleaned_data["password1"])
            #login(request,user)
            messages.success(request,'Registrado correctamente!')
            return redirect(to="login")
        data["form"] = formulario
    return render(request, "registration/registro.html", data)

class FundacionView(View):
    def get(self, *args, **kwargs):
        subscri = Subscripcion.objects.get_or_create(
        user=self.request.user,
        sub=False
        )
        subscri.save()
        context = {
                'object': subscri
            }
        return render(self.request, "app/fundacion.html", context)

class HistorialView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            orden = Orden.objects.filter(user=self.request.user, compra=True)

            context = {
                'object': orden
            }
            return render(self.request, "app/historial.html", context)
        except ObjectDoesNotExist:
            #messages.warning(self.request, "You do not have an active order")
            return redirect("/")
    

def login(request):
    return render(request, "app/login.html")
    
@login_required
def perfil(request):
    return render(request, "app/perfil.html")

def register(request):
    return render(request, "app/register.html")

def api_digimon(request):
    response = requests.get("https://digimon-api.vercel.app/api/digimon").json()

    data = {
        'listaDigimon' : response
    }
    return render(request, "app/apiqla.html", data)

def registrado(request):
    return render(request, "app/registrado.html")

class DetalleOrdenView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            orden = Orden.objects.filter(user=self.request.user, compra=True)[0]
            context = {
                'object': orden
            }
            return render(self.request, 'app/detalle_orden.html', context)
        except ObjectDoesNotExist:
            #messages.warning(self.request, "You do not have an active order")
            return redirect("/")

def seguimientovista(request):
    return render(request, "app/seguimientovista.html")


@login_required
def agregar_carrito(request, slug):
    item = get_object_or_404(Producto, slug=slug)
    orden_item, created = Carrito.objects.get_or_create(
        item=item,
        user=request.user,
        compra=False
        )
    orden_qs = Orden.objects.filter(user=request.user, compra=False)
    if orden_qs.exists():
        orden = orden_qs[0]
        # verificar si el item esta en la orden
        if orden.items.filter(item__slug=item.slug).exists():
            if item.stock <= 0:
                return redirect("carrito")
            else:
                orden_item.cantidad += 1
                orden_item.save()
                item.stock -= 1
                item.save()
                #messages.success(request, "Cantidad de producto actualizada exitosamente.")
                return redirect("carrito")
        else:
            if item.stock <= 0:
                return redirect("tienda", slug=slug)
            orden.items.add(orden_item)
            item.stock -= 1
            item.save()
            return redirect("carrito")
    else:
        fecha_compra = timezone.now()
        orden = Orden.objects.create(user=request.user, fecha_compra=fecha_compra)
        orden.items.add(orden_item)
        item.stock -= 1
        item.save()
        messages.success(request, "se creo")
        return redirect("tienda", slug=slug)

@login_required
def borrar_carrito(request, slug):
    item = get_object_or_404(Producto, slug=slug)
    orden_qs = Orden.objects.filter(user=request.user, compra=False)
    if orden_qs.exists():
        orden = orden_qs[0]
        # verificar si el item esta en la orden
        if orden.items.filter(item__slug=item.slug).exists():
            orden_item = Carrito.objects.filter(
            item=item,
            user=request.user,
            compra=False
            )[0]
            
            item.stock += orden_item.cantidad
            item.save()
            orden.items.remove(orden_item)
            orden_item.delete()
            #orden_qs.delete()
            #messages.info(request, "Producto eliminado del carrito.")
            return redirect("carrito")
        else:
            #messages.info(request, "Este producto no se encuentra en el carrito.")
            return redirect("tienda", slug=slug)
    else:
        #messages.info(request, "No hay orden activa.")
        return redirect("tienda", slug=slug)

@login_required
def remover_unidad_producto(request, slug):
    item = get_object_or_404(Producto, slug=slug)
    order_qs = Orden.objects.filter(
        user=request.user,
        compra=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = Carrito.objects.filter(
                item=item,
                user=request.user,
                compra=False
            )[0]
            if order_item.cantidad > 1:
                order_item.cantidad -= 1
                order_item.save()
                item.stock += 1
                item.save()
            else:
                order_item.delete()
                order.items.remove(order_item)
                item.stock += 1
                item.save()
            
            return redirect("carrito")
        else:
            
            return redirect("tienda", slug=slug)
    else:
        
        return redirect("tienda", slug=slug)

@login_required
def comprar_producto(request, slug):
    item = get_object_or_404(Producto, slug=slug)
    orden_qs = Orden.objects.filter(user=request.user, compra=False)
    if orden_qs.exists():

        #tomamos el primer objeto de la qs
        orden = orden_qs[0]

        # verificar si el item esta en la orden
        if orden.items.filter(item__slug=item.slug).exists():
            orden_item = Carrito.objects.filter(
            item=item,
            user=request.user,
            compra=False
            )[0]
            #orden.items.remove(orden_item)
            orden_item.compra=True
            orden_item.save()
            orden.compra=True
            orden.save()
            return redirect("index")
        else:
        
            return redirect("compra")
    else:
        
        return redirect("compra")

@permission_required('request.user.is_superuser')
def perfilcrud_users(request):
    return render(request, "app/perfilcrud_users.html")

@permission_required('request.user.is_superuser')
def perfilcrud_productos(request):
    return render(request, "app/perfilcrud_productos.html")