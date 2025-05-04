from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.nombre
        
    def get_absolute_url(self):
        return reverse('productos:proveedor_detail', args=[str(self.id)])

class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nombre
        
    def get_absolute_url(self):
        return reverse('productos:unidadmedida_detail', args=[str(self.id)])

class Marca(models.Model):
    nombre = models.CharField(max_length=100)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nombre
        
    def get_absolute_url(self):
        return reverse('productos:marca_detail', args=[str(self.id)])

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=250)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True, help_text='Imagen del producto')

    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, null=True, blank=True)
    um = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.nombre
        
    def get_absolute_url(self):
        return reverse('productos:producto_detail', args=[str(self.id)])

class Stock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.FloatField()
    fecha_modificacion = models.DateTimeField(auto_now=True)
    en_uso = models.BooleanField(default=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.producto} - {self.cantidad}'
        
    def get_absolute_url(self):
        return reverse('productos:stock_detail', args=[str(self.id)])
    
    @classmethod
    def actualizar_stock(cls, producto_id, cantidad, es_venta=False):
        """Actualiza el stock de un producto.
        
        Args:
            producto_id: ID del producto a actualizar
            cantidad: Cantidad a agregar (positivo) o restar (negativo)
            es_venta: Si es True, la cantidad se resta; si es False, se suma
        
        Returns:
            Stock: Instancia del stock actualizado
        """
        # Si es una venta, convertimos la cantidad a negativo para restar
        if es_venta:
            cantidad = -abs(cantidad)
        
        try:
            # Intentamos obtener el stock activo del producto
            stock = cls.objects.filter(producto_id=producto_id, en_uso=True).first()
            
            if stock:
                # Si existe stock, actualizamos la cantidad
                stock.cantidad += float(cantidad)
                stock.save()
            else:
                # Si no existe stock, creamos uno nuevo (solo para agregar, no para ventas)
                if not es_venta or float(cantidad) > 0:
                    producto = Producto.objects.get(id=producto_id)
                    stock = cls.objects.create(
                        producto=producto,
                        cantidad=float(cantidad),
                        en_uso=True
                    )
                else:
                    # No hay stock para vender
                    raise ValueError(f"No hay stock disponible para el producto ID: {producto_id}")
            
            return stock
        except Exception as e:
            # Capturamos cualquier error y lo propagamos
            raise ValueError(f"Error al actualizar stock: {str(e)}")

class Zona(models.Model):
    nombre = models.CharField(max_length=100)
    localidades = models.TextField(blank=True, null=True, help_text="Ingrese las localidades separadas por comas")
    
    def __str__(self) -> str:
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('productos:zona_detail', args=[str(self.id)])


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    zona = models.ForeignKey(Zona, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.nombre
        
    def get_absolute_url(self):
        return reverse('productos:cliente_detail', args=[str(self.id)])

class EstadoPago(models.Model):
    estado = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.estado
        
    def get_absolute_url(self):
        return reverse('productos:estadopago_detail', args=[str(self.id)])

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado_pago = models.ForeignKey(EstadoPago, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo_pendiente = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f'{self.cliente} - {self.fecha} - {self.total}'
        
    def get_absolute_url(self):
        return reverse('productos:venta_detail', args=[str(self.id)])
    
    def actualizar_saldo(self):
        """Actualiza el saldo pendiente basado en el total y el monto pagado"""
        self.saldo_pendiente = self.total - self.monto_pagado
        if self.saldo_pendiente <= 0:
            # Si el saldo es cero o negativo, cambiamos el estado a pagado completo
            estado_completo = EstadoPago.objects.get(estado='Completo')
            self.estado_pago = estado_completo
            self.saldo_pendiente = 0  # Aseguramos que no quede negativo
        elif self.monto_pagado > 0:
            # Si hay algún pago pero aún hay saldo, es pago parcial
            estado_parcial = EstadoPago.objects.get(estado='Parcial')
            self.estado_pago = estado_parcial
        else:
            # Si no hay pagos, es deuda total
            estado_debe = EstadoPago.objects.get(estado='Debe Total')
            self.estado_pago = estado_debe
        self.save()

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    # Nuevos campos para el cálculo de precios con ganancia
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    porcentaje_ganancia = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f'{self.producto} - {self.cantidad} - {self.precio_venta}'
        
    def get_absolute_url(self):
        return reverse('productos:detalleventa_detail', args=[str(self.id)])

class MetodoPago(models.Model):
    metodo = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.metodo
        
    def get_absolute_url(self):
        return reverse('productos:metodopago_detail', args=[str(self.id)])

class Pago(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.venta} - {self.fecha} - {self.monto}'
        
    def get_absolute_url(self):
        return reverse('productos:pago_detail', args=[str(self.id)])

class Devolucion(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    volver_al_stock = models.BooleanField(default=True, help_text='Indica si el producto devuelto debe volver al stock')
    motivo = models.TextField(blank=True, null=True, help_text='Motivo de la devolución')

    def __str__(self) -> str:
        return f'{self.producto} - {self.cantidad} - {self.fecha}'
        
    def get_absolute_url(self):
        return reverse('productos:devolucion_detail', args=[str(self.id)])


class Catalogo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    codigo_acceso = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
            # Asegurarse de que el slug sea único
            original_slug = self.slug
            contador = 1
            while Catalogo.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{contador}"
                contador += 1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('productos:catalogo_detail', args=[str(self.id)])
    
    def get_public_url(self):
        return reverse('productos:catalogo_publico', args=[str(self.codigo_acceso)])


class ProductoCatalogo(models.Model):
    catalogo = models.ForeignKey(Catalogo, on_delete=models.CASCADE, related_name='productos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    porcentaje_ganancia = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    destacado = models.BooleanField(default=False)
    orden = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['orden', 'producto__nombre']
        unique_together = ('catalogo', 'producto')
    
    def save(self, *args, **kwargs):
        # Calcular el precio final basado en el precio del producto y el porcentaje de ganancia
        precio_base = self.producto.precio
        ganancia = precio_base * (self.porcentaje_ganancia / 100)
        self.precio_final = precio_base + ganancia
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.producto.nombre} en {self.catalogo.nombre}"
    
    def get_absolute_url(self):
        return reverse('productos:producto_catalogo_detail', args=[str(self.id)])
