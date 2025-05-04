from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Producto
import uuid
from django.utils.text import slugify

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
