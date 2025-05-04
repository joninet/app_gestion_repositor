from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db import transaction

from .models import Catalogo, ProductoCatalogo, Producto
from .forms import CatalogoForm, ProductoCatalogoFormSet, SeleccionProductosForm
from .mixins import UserDataMixin

# Vistas para Catálogo (privadas, requieren autenticación)
class CatalogoListView(LoginRequiredMixin, ListView):
    model = Catalogo
    template_name = 'productos/catalogo_list.html'
    context_object_name = 'catalogos'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Si el usuario es staff o superuser, puede ver todos los catálogos
        if user.is_staff or user.is_superuser:
            return queryset
            
        # Filtrar catálogos por usuario
        return queryset.filter(usuario=user)


class CatalogoDetailView(LoginRequiredMixin, DetailView):
    model = Catalogo
    template_name = 'productos/catalogo_detail.html'
    context_object_name = 'catalogo'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Si el usuario es staff o superuser, puede ver todos los catálogos
        if user.is_staff or user.is_superuser:
            return queryset
            
        # Filtrar catálogos por usuario
        return queryset.filter(usuario=user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos_catalogo'] = ProductoCatalogo.objects.filter(
            catalogo=self.object
        ).select_related('producto').order_by('orden', 'producto__nombre')
        context['url_publica'] = self.request.build_absolute_uri(
            reverse('productos:catalogo_publico', args=[str(self.object.codigo_acceso)])
        )
        return context


class CatalogoCreateView(LoginRequiredMixin, CreateView):
    model = Catalogo
    form_class = CatalogoForm
    template_name = 'productos/catalogo_form.html'
    success_url = reverse_lazy('productos:catalogo_list')
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Catálogo creado con éxito')
        return super().form_valid(form)


class CatalogoUpdateView(LoginRequiredMixin, UpdateView):
    model = Catalogo
    form_class = CatalogoForm
    template_name = 'productos/catalogo_form.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Si el usuario es staff o superuser, puede editar todos los catálogos
        if user.is_staff or user.is_superuser:
            return queryset
            
        # Filtrar catálogos por usuario
        return queryset.filter(usuario=user)
    
    def get_success_url(self):
        return reverse_lazy('productos:catalogo_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Catálogo actualizado con éxito')
        return super().form_valid(form)


class CatalogoDeleteView(LoginRequiredMixin, DeleteView):
    model = Catalogo
    template_name = 'productos/catalogo_confirm_delete.html'
    success_url = reverse_lazy('productos:catalogo_list')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Si el usuario es staff o superuser, puede eliminar todos los catálogos
        if user.is_staff or user.is_superuser:
            return queryset
            
        # Filtrar catálogos por usuario
        return queryset.filter(usuario=user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Catálogo eliminado con éxito')
        return super().delete(request, *args, **kwargs)


# Vista para gestionar productos en un catálogo
class ProductosCatalogoView(LoginRequiredMixin, UpdateView):
    model = Catalogo
    template_name = 'productos/productos_catalogo_form.html'
    fields = []  # No necesitamos campos del catálogo aquí
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Si el usuario es staff o superuser, puede editar todos los catálogos
        if user.is_staff or user.is_superuser:
            return queryset
            
        # Filtrar catálogos por usuario
        return queryset.filter(usuario=user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.POST:
            context['formset'] = ProductoCatalogoFormSet(
                self.request.POST, 
                instance=self.object
            )
        else:
            context['formset'] = ProductoCatalogoFormSet(instance=self.object)
            
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        with transaction.atomic():
            if formset.is_valid():
                formset.save()
                messages.success(self.request, 'Productos del catálogo actualizados con éxito')
                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse_lazy('productos:catalogo_detail', kwargs={'pk': self.object.pk})


# Vista para añadir múltiples productos a un catálogo
class AgregarProductosCatalogoView(LoginRequiredMixin, FormView):
    template_name = 'productos/agregar_productos_catalogo.html'
    form_class = SeleccionProductosForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalogo'] = get_object_or_404(Catalogo, pk=self.kwargs['pk'])
        
        # Obtener productos que ya están en el catálogo para excluirlos
        productos_en_catalogo = ProductoCatalogo.objects.filter(
            catalogo_id=self.kwargs['pk']
        ).values_list('producto_id', flat=True)
        
        # Filtrar productos que no están en el catálogo
        user = self.request.user
        if user.is_staff or user.is_superuser:
            productos_disponibles = Producto.objects.exclude(id__in=productos_en_catalogo)
        else:
            productos_disponibles = Producto.objects.filter(
                usuario=user
            ).exclude(id__in=productos_en_catalogo)
        
        context['form'].fields['productos'].queryset = productos_disponibles
        return context
    
    def form_valid(self, form):
        catalogo = get_object_or_404(Catalogo, pk=self.kwargs['pk'])
        productos_seleccionados = form.cleaned_data['productos']
        porcentaje_ganancia = form.cleaned_data['porcentaje_ganancia_default']
        
        # Verificar que el usuario tiene permiso para modificar este catálogo
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            if catalogo.usuario != self.request.user:
                messages.error(self.request, 'No tienes permiso para modificar este catálogo')
                return redirect('productos:catalogo_list')
        
        # Añadir productos al catálogo
        contador = 0
        for producto in productos_seleccionados:
            ProductoCatalogo.objects.create(
                catalogo=catalogo,
                producto=producto,
                porcentaje_ganancia=porcentaje_ganancia,
                orden=ProductoCatalogo.objects.filter(catalogo=catalogo).count() + 1
            )
            contador += 1
        
        messages.success(self.request, f'{contador} productos añadidos al catálogo')
        return redirect('productos:catalogo_detail', pk=catalogo.pk)


# Vista pública del catálogo (no requiere autenticación)
class CatalogoPublicoView(DetailView):
    model = Catalogo
    template_name = 'productos/catalogo_publico.html'
    context_object_name = 'catalogo'
    slug_field = 'codigo_acceso'
    slug_url_kwarg = 'codigo'
    
    def get_queryset(self):
        # Solo mostrar catálogos activos
        return Catalogo.objects.filter(activo=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener productos del catálogo
        context['productos'] = ProductoCatalogo.objects.filter(
            catalogo=self.object
        ).select_related('producto').order_by('orden', 'producto__nombre')
        
        # Productos destacados
        context['productos_destacados'] = context['productos'].filter(destacado=True)
        
        return context
