from django.contrib import admin
from productos.models import *

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'direccion', 'email', 'telefono')
    list_filter = ('nombre',)
    search_fields = ('nombre',)

@admin.register(UnidadMedida)
class UnidadMedidaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'precio', 'proveedor', 'um',)

@admin.register(Stock)
class stockAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'fecha_modificacion', 'en_uso',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono', 'email',)

@admin.register(EstadoPago)
class EstadoPagoAdmin(admin.ModelAdmin):
    list_display = ('estado',)

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha', 'total', 'estado_pago',)

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('venta', 'producto', 'cantidad', 'precio_costo', 'porcentaje_ganancia', 'precio_venta')

@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ('metodo',)

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('venta', 'fecha', 'monto', 'metodo_pago',)

@admin.register(Devolucion)
class DevolucionAdmin(admin.ModelAdmin):
    list_display = ('venta', 'producto', 'cantidad', 'fecha',)
