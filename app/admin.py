from django.contrib import admin
from.models import *
# Register your models here.


class ProductoAdmin(admin.ModelAdmin):
    list_display = ['codigo','nombre','precio','descripcion','tipo', 'imagen', 'fecha_ingreso']
    search_fields = ['codigo']   #PARA BUSCAR ITEMS POR SU CODIGO
    list_per_page = 5    #PARA DECIDIR CUANTOS ITEMS SE MUESTRAN POR PAGINA


class UserAdmin(admin.ModelAdmin):
    list_display = ['nombre_usuario','apellido_usuario','username','contraseña_usuario','correo_usuario','tipo_usuario']
    search_fields = ['nombre_usuario']   #PARA BUSCAR ITEMS POR SU CODIGO
    list_per_page = 5    #PARA DECIDIR CUANTOS ITEMS SE MUESTRAN POR PAGINA

class CarritoAdmin(admin.ModelAdmin):
    list_display = ['id','item_id','user', 'cantidad']
    list_per_page = 5    #PARA DECIDIR CUANTOS ITEMS SE MUESTRAN POR PAGINA

admin.site.register(TipoProducto)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(Carrito,CarritoAdmin)
admin.site.register(Usuario,UserAdmin)
admin.site.register(TipoUsuario)
admin.site.register(Orden)
admin.site.register(Subscripcion)