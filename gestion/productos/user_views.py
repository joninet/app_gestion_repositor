from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

from .mixins import UserDataMixin
from .views import (
    IndexView, ProveedorListView, ProveedorDetailView, ProveedorCreateView, ProveedorUpdateView, ProveedorDeleteView,
    UnidadMedidaListView, UnidadMedidaDetailView, UnidadMedidaCreateView, UnidadMedidaUpdateView, UnidadMedidaDeleteView,
    MarcaListView, MarcaDetailView, MarcaCreateView, MarcaUpdateView, MarcaDeleteView,
    ProductoListView, ProductoDetailView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView,
    StockListView, StockDetailView, StockCreateView, StockUpdateView, StockDeleteView,
    ClienteListView, ClienteDetailView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView,
    EstadoPagoListView, EstadoPagoDetailView, EstadoPagoCreateView, EstadoPagoUpdateView, EstadoPagoDeleteView,
    VentaListView, VentaDetailView, VentaCreateView, VentaUpdateView, VentaDeleteView,
    DetalleVentaListView, DetalleVentaDetailView, DetalleVentaCreateView, DetalleVentaUpdateView, DetalleVentaDeleteView,
    MetodoPagoListView, MetodoPagoDetailView, MetodoPagoCreateView, MetodoPagoUpdateView, MetodoPagoDeleteView,
    PagoListView, PagoDetailView, PagoCreateView, PagoUpdateView, PagoDeleteView,
    DevolucionListView, DevolucionDetailView, DevolucionCreateView, DevolucionUpdateView, DevolucionDeleteView
)

# Vista de Inicio con autenticación
class UserIndexView(LoginRequiredMixin, IndexView):
    def get_context_data(self, **kwargs):
        # Primero obtenemos el contexto de la clase padre pero sin llamar a super().get_context_data
        # para evitar que se ejecute el código que calcula los counts
        context = super(IndexView, self).get_context_data(**kwargs)
        user = self.request.user
        
        # Si el usuario es staff o superuser, puede ver todos los datos como en la clase padre
        if user.is_staff or user.is_superuser:
            return super().get_context_data(**kwargs)
            
        # Filtrar datos por usuario antes de contar
        from .models import Producto, Cliente, Venta, Stock
        
        context['productos_count'] = Producto.objects.filter(usuario=user).count()
        context['clientes_count'] = Cliente.objects.filter(usuario=user).count()
        context['ventas_count'] = Venta.objects.filter(usuario=user).count()
        context['ultimas_ventas'] = Venta.objects.filter(usuario=user).order_by('-fecha')[:5]
        context['productos_bajo_stock'] = Stock.objects.filter(cantidad__lt=10, en_uso=True, producto__usuario=user).order_by('cantidad')[:5]
        
        return context

# Vistas para Proveedor con autenticación
class UserProveedorListView(UserDataMixin, ProveedorListView):
    pass

class UserProveedorDetailView(UserDataMixin, ProveedorDetailView):
    pass

class UserProveedorCreateView(UserDataMixin, ProveedorCreateView):
    pass

class UserProveedorUpdateView(UserDataMixin, ProveedorUpdateView):
    pass

class UserProveedorDeleteView(UserDataMixin, ProveedorDeleteView):
    pass

# Vistas para UnidadMedida con autenticación
class UserUnidadMedidaListView(UserDataMixin, UnidadMedidaListView):
    pass

class UserUnidadMedidaDetailView(UserDataMixin, UnidadMedidaDetailView):
    pass

class UserUnidadMedidaCreateView(UserDataMixin, UnidadMedidaCreateView):
    pass

class UserUnidadMedidaUpdateView(UserDataMixin, UnidadMedidaUpdateView):
    pass

class UserUnidadMedidaDeleteView(UserDataMixin, UnidadMedidaDeleteView):
    pass

# Vistas para Marca con autenticación
class UserMarcaListView(UserDataMixin, MarcaListView):
    pass

class UserMarcaDetailView(UserDataMixin, MarcaDetailView):
    pass

class UserMarcaCreateView(UserDataMixin, MarcaCreateView):
    pass

class UserMarcaUpdateView(UserDataMixin, MarcaUpdateView):
    pass

class UserMarcaDeleteView(UserDataMixin, MarcaDeleteView):
    pass

# Vistas para Producto con autenticación
class UserProductoListView(UserDataMixin, ProductoListView):
    pass

class UserProductoDetailView(UserDataMixin, ProductoDetailView):
    pass

class UserProductoCreateView(UserDataMixin, ProductoCreateView):
    pass

class UserProductoUpdateView(UserDataMixin, ProductoUpdateView):
    pass

class UserProductoDeleteView(UserDataMixin, ProductoDeleteView):
    pass

# Vistas para Stock con autenticación
class UserStockListView(UserDataMixin, StockListView):
    pass

class UserStockDetailView(UserDataMixin, StockDetailView):
    pass

class UserStockCreateView(UserDataMixin, StockCreateView):
    def form_valid(self, form):
        # Asignar el usuario actual al stock
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class UserStockUpdateView(UserDataMixin, StockUpdateView):
    pass

class UserStockDeleteView(UserDataMixin, StockDeleteView):
    pass

# Vistas para Cliente con autenticación
class UserClienteListView(UserDataMixin, ClienteListView):
    pass

class UserClienteDetailView(UserDataMixin, ClienteDetailView):
    pass

class UserClienteCreateView(UserDataMixin, ClienteCreateView):
    fields = ['nombre', 'direccion', 'telefono', 'email', 'zona']

class UserClienteUpdateView(UserDataMixin, ClienteUpdateView):
    fields = ['nombre', 'direccion', 'telefono', 'email', 'zona']

class UserClienteDeleteView(UserDataMixin, ClienteDeleteView):
    pass

# Vistas para EstadoPago con autenticación
class UserEstadoPagoListView(UserDataMixin, EstadoPagoListView):
    pass

class UserEstadoPagoDetailView(UserDataMixin, EstadoPagoDetailView):
    pass

class UserEstadoPagoCreateView(UserDataMixin, EstadoPagoCreateView):
    pass

class UserEstadoPagoUpdateView(UserDataMixin, EstadoPagoUpdateView):
    pass

class UserEstadoPagoDeleteView(UserDataMixin, EstadoPagoDeleteView):
    pass

# Vistas para Venta con autenticación
class UserVentaListView(UserDataMixin, VentaListView):
    pass

class UserVentaDetailView(UserDataMixin, VentaDetailView):
    pass

class UserVentaCreateView(VentaCreateView):
    # No heredamos de UserDataMixin porque VentaCreateView tiene un form_valid diferente
    # y heredamos directamente de View, no de CreateView
    
    def get(self, request, *args, **kwargs):
        # Verificar que el usuario esté autenticado
        if not request.user.is_authenticated:
            return redirect('productos:login')
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # Verificar que el usuario esté autenticado
        if not request.user.is_authenticated:
            return redirect('productos:login')
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, venta_form, detalle_formset):
        # Asignar el usuario actual a la venta
        venta_form.instance.usuario = self.request.user
        return super().form_valid(venta_form, detalle_formset)

class UserVentaUpdateView(VentaUpdateView):
    # No heredamos de UserDataMixin porque VentaUpdateView tiene un form_valid diferente
    # y heredamos directamente de View, no de UpdateView
    
    def get(self, request, *args, **kwargs):
        # Verificar que el usuario esté autenticado
        if not request.user.is_authenticated:
            return redirect('productos:login')
            
        # Verificar que la venta pertenezca al usuario actual
        venta = self.get_object()
        if venta.usuario and venta.usuario != request.user and not request.user.is_staff and not request.user.is_superuser:
            messages.error(request, 'No tienes permiso para editar esta venta')
            return redirect('productos:venta_list')
            
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # Verificar que el usuario esté autenticado
        if not request.user.is_authenticated:
            return redirect('productos:login')
            
        # Verificar que la venta pertenezca al usuario actual
        venta = self.get_object()
        if venta.usuario and venta.usuario != request.user and not request.user.is_staff and not request.user.is_superuser:
            messages.error(request, 'No tienes permiso para editar esta venta')
            return redirect('productos:venta_list')
            
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, venta_form, detalle_formset):
        # Asignar el usuario actual a la venta si no tiene usuario asignado
        if not venta_form.instance.usuario:
            venta_form.instance.usuario = self.request.user
        return super().form_valid(venta_form, detalle_formset)

class UserVentaDeleteView(UserDataMixin, VentaDeleteView):
    pass

# Vistas para DetalleVenta con autenticación
class UserDetalleVentaListView(UserDataMixin, DetalleVentaListView):
    def get_queryset(self):
        queryset = super(DetalleVentaListView, self).get_queryset()
        user = self.request.user
        
        # Si el usuario es staff o superuser, puede ver todos los datos
        if user.is_staff or user.is_superuser:
            return queryset
            
        # Filtrar detalles de venta por usuario de la venta
        return queryset.filter(venta__usuario=user)

class UserDetalleVentaDetailView(UserDataMixin, DetalleVentaDetailView):
    def get_queryset(self):
        queryset = super(DetalleVentaDetailView, self).get_queryset()
        user = self.request.user
        
        # Si el usuario es staff o superuser, puede ver todos los datos
        if user.is_staff or user.is_superuser:
            return queryset
            
        # Filtrar detalles de venta por usuario de la venta
        return queryset.filter(venta__usuario=user)

class UserDetalleVentaCreateView(UserDataMixin, DetalleVentaCreateView):
    pass

class UserDetalleVentaUpdateView(UserDataMixin, DetalleVentaUpdateView):
    pass

class UserDetalleVentaDeleteView(UserDataMixin, DetalleVentaDeleteView):
    pass

# Vistas para MetodoPago con autenticación
class UserMetodoPagoListView(UserDataMixin, MetodoPagoListView):
    pass

class UserMetodoPagoDetailView(UserDataMixin, MetodoPagoDetailView):
    pass

class UserMetodoPagoCreateView(UserDataMixin, MetodoPagoCreateView):
    pass

class UserMetodoPagoUpdateView(UserDataMixin, MetodoPagoUpdateView):
    pass

class UserMetodoPagoDeleteView(UserDataMixin, MetodoPagoDeleteView):
    pass

# Vistas para Pago con autenticación
class UserPagoListView(UserDataMixin, PagoListView):
    def get_queryset(self):
        queryset = super(PagoListView, self).get_queryset()
        user = self.request.user
        
        # Si el usuario es staff o superuser, puede ver todos los datos
        if user.is_staff or user.is_superuser:
            return queryset
            
        # Filtrar pagos por usuario de la venta
        return queryset.filter(venta__usuario=user)

class UserPagoDetailView(UserDataMixin, PagoDetailView):
    def get_queryset(self):
        queryset = super(PagoDetailView, self).get_queryset()
        user = self.request.user
        
        # Si el usuario es staff o superuser, puede ver todos los datos
        if user.is_staff or user.is_superuser:
            return queryset
            
        # Filtrar pagos por usuario de la venta
        return queryset.filter(venta__usuario=user)

class UserPagoCreateView(UserDataMixin, PagoCreateView):
    pass

class UserPagoUpdateView(UserDataMixin, PagoUpdateView):
    pass

class UserPagoDeleteView(UserDataMixin, PagoDeleteView):
    pass

# Vistas para Devolucion con autenticación
class UserDevolucionListView(UserDataMixin, DevolucionListView):
    def get_queryset(self):
        queryset = super(DevolucionListView, self).get_queryset()
        user = self.request.user
        
        # Si el usuario es staff o superuser, puede ver todos los datos
        if user.is_staff or user.is_superuser:
            return queryset
            
        # Filtrar devoluciones por usuario de la venta
        return queryset.filter(venta__usuario=user)

class UserDevolucionDetailView(UserDataMixin, DevolucionDetailView):
    def get_queryset(self):
        queryset = super(DevolucionDetailView, self).get_queryset()
        user = self.request.user
        
        # Si el usuario es staff o superuser, puede ver todos los datos
        if user.is_staff or user.is_superuser:
            return queryset
            
        # Filtrar devoluciones por usuario de la venta
        return queryset.filter(venta__usuario=user)

class UserDevolucionCreateView(UserDataMixin, DevolucionCreateView):
    pass

class UserDevolucionUpdateView(UserDataMixin, DevolucionUpdateView):
    pass

class UserDevolucionDeleteView(UserDataMixin, DevolucionDeleteView):
    pass
