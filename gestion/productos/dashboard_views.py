from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum, Q
from .models import Producto, Cliente, Venta, Stock

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'productos/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Si el usuario es staff o superuser, puede ver todos los datos
        if user.is_staff or user.is_superuser:
            # Estadísticas generales
            context['total_productos'] = Producto.objects.count()
            context['total_clientes'] = Cliente.objects.count()
            context['total_ventas'] = Venta.objects.count()
            
            # Productos más vendidos
            context['productos_mas_vendidos'] = Producto.objects.annotate(
                total_vendido=Sum('detalleventa__cantidad')
            ).order_by('-total_vendido')[:5]
            
            # Clientes con más compras
            context['clientes_top'] = Cliente.objects.annotate(
                total_compras=Count('venta')
            ).order_by('-total_compras')[:5]
            
            # Ventas recientes
            context['ventas_recientes'] = Venta.objects.all().order_by('-fecha')[:10]
            
            # Productos con bajo stock
            context['productos_bajo_stock'] = Stock.objects.filter(cantidad__lt=10).order_by('cantidad')[:5]
        else:
            # Estadísticas filtradas por usuario
            context['total_productos'] = Producto.objects.filter(Q(usuario=user) | Q(usuario__isnull=True)).count()
            context['total_clientes'] = Cliente.objects.filter(Q(usuario=user) | Q(usuario__isnull=True)).count()
            context['total_ventas'] = Venta.objects.filter(Q(usuario=user) | Q(usuario__isnull=True)).count()
            
            # Productos más vendidos (solo del usuario)
            context['productos_mas_vendidos'] = Producto.objects.filter(
                Q(usuario=user) | Q(usuario__isnull=True)
            ).annotate(
                total_vendido=Sum('detalleventa__cantidad', 
                                  filter=Q(detalleventa__venta__usuario=user) | Q(detalleventa__venta__usuario__isnull=True))
            ).order_by('-total_vendido')[:5]
            
            # Clientes con más compras (solo del usuario)
            context['clientes_top'] = Cliente.objects.filter(
                Q(usuario=user) | Q(usuario__isnull=True)
            ).annotate(
                total_compras=Count('venta', 
                                   filter=Q(venta__usuario=user) | Q(venta__usuario__isnull=True))
            ).order_by('-total_compras')[:5]
            
            # Ventas recientes (solo del usuario)
            context['ventas_recientes'] = Venta.objects.filter(
                Q(usuario=user) | Q(usuario__isnull=True)
            ).order_by('-fecha')[:10]
            
            # Productos con bajo stock (solo del usuario)
            context['productos_bajo_stock'] = Stock.objects.filter(
                Q(usuario=user) | Q(usuario__isnull=True),
                cantidad__lt=10
            ).order_by('cantidad')[:5]
        
        # Contar elementos asociados al usuario
        context['ventas_count'] = Venta.objects.filter(usuario=user).count()
        context['productos_count'] = Producto.objects.filter(usuario=user).count()
        context['clientes_count'] = Cliente.objects.filter(usuario=user).count()
        context['stock_count'] = Stock.objects.filter(usuario=user).count()
        
        # Obtener las últimas 5 ventas del usuario
        context['ultimas_ventas'] = Venta.objects.filter(usuario=user).order_by('-fecha')[:5]
        
        # Obtener productos con stock bajo (menos de 10 unidades)
        context['stock_bajo'] = Stock.objects.filter(
            usuario=user, 
            en_uso=True, 
            cantidad__lt=10
        ).order_by('cantidad')[:5]
        
        return context
