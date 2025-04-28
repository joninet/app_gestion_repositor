from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count, Sum
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from io import BytesIO
from datetime import datetime

from .forms import VentaForm, DetalleVentaFormSet

from .models import (
    Proveedor, UnidadMedida, Marca, Producto, Stock, Cliente, 
    EstadoPago, Venta, DetalleVenta, MetodoPago, Pago, Devolucion, Zona
)

# Vista de Inicio
class IndexView(TemplateView):
    template_name = 'productos/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos_count'] = Producto.objects.count()
        context['clientes_count'] = Cliente.objects.count()
        context['ventas_count'] = Venta.objects.count()
        context['ultimas_ventas'] = Venta.objects.all().order_by('-fecha')[:5]
        context['productos_bajo_stock'] = Stock.objects.filter(cantidad__lt=10, en_uso=True).order_by('cantidad')[:5]
        return context

# Vistas para Proveedor
class ProveedorListView(ListView):
    model = Proveedor
    template_name = 'productos/proveedor_list.html'
    context_object_name = 'proveedores'

class ProveedorDetailView(DetailView):
    model = Proveedor
    template_name = 'productos/proveedor_detail.html'
    context_object_name = 'proveedor'

class ProveedorCreateView(CreateView):
    model = Proveedor
    template_name = 'productos/proveedor_form.html'
    fields = ['nombre', 'direccion', 'email', 'telefono']
    success_url = reverse_lazy('productos:proveedor_list')

    def form_valid(self, form):
        messages.success(self.request, 'Proveedor creado con éxito')
        return super().form_valid(form)

class ProveedorUpdateView(UpdateView):
    model = Proveedor
    template_name = 'productos/proveedor_form.html'
    fields = ['nombre', 'direccion', 'email', 'telefono']
    success_url = reverse_lazy('productos:proveedor_list')

    def form_valid(self, form):
        messages.success(self.request, 'Proveedor actualizado con éxito')
        return super().form_valid(form)

class ProveedorDeleteView(DeleteView):
    model = Proveedor
    template_name = 'productos/proveedor_confirm_delete.html'
    success_url = reverse_lazy('productos:proveedor_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Proveedor eliminado con éxito')
        return super().delete(request, *args, **kwargs)

# Vistas para UnidadMedida
class UnidadMedidaListView(ListView):
    model = UnidadMedida
    template_name = 'productos/unidadmedida_list.html'
    context_object_name = 'unidades_medida'

class UnidadMedidaDetailView(DetailView):
    model = UnidadMedida
    template_name = 'productos/unidadmedida_detail.html'
    context_object_name = 'unidadmedida'

class UnidadMedidaCreateView(CreateView):
    model = UnidadMedida
    template_name = 'productos/unidadmedida_form.html'
    fields = ['nombre']
    success_url = reverse_lazy('productos:unidadmedida_list')

    def form_valid(self, form):
        messages.success(self.request, 'Unidad de medida creada con éxito')
        return super().form_valid(form)

class UnidadMedidaUpdateView(UpdateView):
    model = UnidadMedida
    template_name = 'productos/unidadmedida_form.html'
    fields = ['nombre']
    success_url = reverse_lazy('productos:unidadmedida_list')

    def form_valid(self, form):
        messages.success(self.request, 'Unidad de medida actualizada con éxito')
        return super().form_valid(form)

class UnidadMedidaDeleteView(DeleteView):
    model = UnidadMedida
    template_name = 'productos/unidadmedida_confirm_delete.html'
    success_url = reverse_lazy('productos:unidadmedida_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Unidad de medida eliminada con éxito')
        return super().delete(request, *args, **kwargs)

# Vistas para Marca
class MarcaListView(ListView):
    model = Marca
    template_name = 'productos/marca_list.html'
    context_object_name = 'marcas'

class MarcaDetailView(DetailView):
    model = Marca
    template_name = 'productos/marca_detail.html'
    context_object_name = 'marca'

class MarcaCreateView(CreateView):
    model = Marca
    template_name = 'productos/marca_form.html'
    fields = ['nombre', 'proveedor']
    success_url = reverse_lazy('productos:marca_list')

    def form_valid(self, form):
        messages.success(self.request, 'Marca creada con éxito')
        return super().form_valid(form)

class MarcaUpdateView(UpdateView):
    model = Marca
    template_name = 'productos/marca_form.html'
    fields = ['nombre', 'proveedor']
    success_url = reverse_lazy('productos:marca_list')

    def form_valid(self, form):
        messages.success(self.request, 'Marca actualizada con éxito')
        return super().form_valid(form)

class MarcaDeleteView(DeleteView):
    model = Marca
    template_name = 'productos/marca_confirm_delete.html'
    success_url = reverse_lazy('productos:marca_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Marca eliminada con éxito')
        return super().delete(request, *args, **kwargs)

# Vistas para Producto
class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/producto_list.html'
    context_object_name = 'productos'

class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'productos/producto_detail.html'
    context_object_name = 'producto'

class ProductoCreateView(CreateView):
    model = Producto
    template_name = 'productos/producto_form.html'
    fields = ['nombre', 'descripcion', 'precio', 'imagen', 'proveedor', 'marca', 'um']
    success_url = reverse_lazy('productos:producto_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Añadir clases CSS para mejorar la apariencia del campo de imagen
        form.fields['imagen'].widget.attrs.update({
            'class': 'form-control',
            'accept': 'image/*',  # Aceptar solo imágenes
        })
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Producto creado con éxito')
        return super().form_valid(form)

class ProductoUpdateView(UpdateView):
    model = Producto
    template_name = 'productos/producto_form.html'
    fields = ['nombre', 'descripcion', 'precio', 'imagen', 'proveedor', 'marca', 'um']
    success_url = reverse_lazy('productos:producto_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Añadir clases CSS para mejorar la apariencia del campo de imagen
        form.fields['imagen'].widget.attrs.update({
            'class': 'form-control',
            'accept': 'image/*',  # Aceptar solo imágenes
        })
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Producto actualizado con éxito')
        return super().form_valid(form)

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete.html'
    success_url = reverse_lazy('productos:producto_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Producto eliminado con éxito')
        return super().delete(request, *args, **kwargs)

# Vistas para Stock
class StockListView(ListView):
    model = Stock
    template_name = 'productos/stock_list.html'
    context_object_name = 'stocks'

class StockDetailView(DetailView):
    model = Stock
    template_name = 'productos/stock_detail.html'
    context_object_name = 'stock'

class StockCreateView(CreateView):
    model = Stock
    template_name = 'productos/stock_form.html'
    fields = ['producto', 'cantidad', 'en_uso']
    success_url = reverse_lazy('productos:stock_list')

    def form_valid(self, form):
        try:
            # En lugar de crear un nuevo registro, actualizamos el stock existente
            producto = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']
            en_uso = form.cleaned_data['en_uso']
            
            # Buscamos si ya existe un stock activo para este producto
            stock_existente = Stock.objects.filter(producto=producto, en_uso=True).first()
            
            if stock_existente:
                # Si existe, actualizamos la cantidad
                stock_existente.cantidad += cantidad
                stock_existente.save()
                messages.success(self.request, f'Stock actualizado con éxito. Cantidad actual: {stock_existente.cantidad}')
                return redirect(self.success_url)
            else:
                # Si no existe, creamos uno nuevo (comportamiento normal)
                messages.success(self.request, 'Nuevo stock creado con éxito')
                return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Error al actualizar stock: {str(e)}')
            return self.form_invalid(form)

class StockUpdateView(UpdateView):
    model = Stock
    template_name = 'productos/stock_form.html'
    fields = ['producto', 'cantidad', 'en_uso']
    success_url = reverse_lazy('productos:stock_list')

    def form_valid(self, form):
        messages.success(self.request, 'Stock actualizado con éxito')
        return super().form_valid(form)

class StockDeleteView(DeleteView):
    model = Stock
    template_name = 'productos/stock_confirm_delete.html'
    success_url = reverse_lazy('productos:stock_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Stock eliminado con éxito')
        return super().delete(request, *args, **kwargs)

# Vistas para Cliente
class ClienteListView(ListView):
    model = Cliente
    template_name = 'productos/cliente_list.html'
    context_object_name = 'clientes'

class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'productos/cliente_detail.html'
    context_object_name = 'cliente'

class ClienteCreateView(CreateView):
    model = Cliente
    template_name = 'productos/cliente_form.html'
    fields = ['nombre', 'direccion', 'telefono', 'email', 'zona']
    success_url = reverse_lazy('productos:cliente_list')

    def form_valid(self, form):
        messages.success(self.request, 'Cliente creado con éxito')
        return super().form_valid(form)

class ClienteUpdateView(UpdateView):
    model = Cliente
    template_name = 'productos/cliente_form.html'
    fields = ['nombre', 'direccion', 'telefono', 'email', 'zona']
    success_url = reverse_lazy('productos:cliente_list')

    def form_valid(self, form):
        messages.success(self.request, 'Cliente actualizado con éxito')
        return super().form_valid(form)

class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'productos/cliente_confirm_delete.html'
    success_url = reverse_lazy('productos:cliente_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Cliente eliminado con éxito')
        return super().delete(request, *args, **kwargs)

# Vistas para EstadoPago
class EstadoPagoListView(ListView):
    model = EstadoPago
    template_name = 'productos/estadopago_list.html'
    context_object_name = 'estados_pago'

class EstadoPagoDetailView(DetailView):
    model = EstadoPago
    template_name = 'productos/estadopago_detail.html'
    context_object_name = 'estadopago'

class EstadoPagoCreateView(CreateView):
    model = EstadoPago
    template_name = 'productos/estadopago_form.html'
    fields = ['estado']
    success_url = reverse_lazy('productos:estadopago_list')

    def form_valid(self, form):
        messages.success(self.request, 'Estado de pago creado con éxito')
        return super().form_valid(form)

class EstadoPagoUpdateView(UpdateView):
    model = EstadoPago
    template_name = 'productos/estadopago_form.html'
    fields = ['estado']
    success_url = reverse_lazy('productos:estadopago_list')

    def form_valid(self, form):
        messages.success(self.request, 'Estado de pago actualizado con éxito')
        return super().form_valid(form)

class EstadoPagoDeleteView(DeleteView):
    model = EstadoPago
    template_name = 'productos/estadopago_confirm_delete.html'
    success_url = reverse_lazy('productos:estadopago_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Estado de pago eliminado con éxito')
        return super().delete(request, *args, **kwargs)

# Vistas para Venta
class VentaListView(ListView):
    model = Venta
    template_name = 'productos/venta_list.html'
    context_object_name = 'ventas'

class VentaDetailView(DetailView):
    model = Venta
    template_name = 'productos/venta_detail.html'
    context_object_name = 'venta'

class VentaCreateView(View):
    template_name = 'productos/venta_form.html'
    
    def get(self, request, *args, **kwargs):
        venta_form = VentaForm(prefix='venta')
        detalle_formset = DetalleVentaFormSet(prefix='detalles')
        return render(request, self.template_name, {
            'venta_form': venta_form,
            'detalle_formset': detalle_formset,
            'productos': Producto.objects.all(),
        })
    
    def post(self, request, *args, **kwargs):
        venta_form = VentaForm(request.POST, prefix='venta')
        detalle_formset = DetalleVentaFormSet(request.POST, prefix='detalles')
        
        # Agregar mensajes de depuración
        print("Venta form is valid:", venta_form.is_valid())
        if not venta_form.is_valid():
            print("Venta form errors:", venta_form.errors)
        
        print("Detalle formset is valid:", detalle_formset.is_valid())
        if not detalle_formset.is_valid():
            print("Detalle formset errors:", detalle_formset.errors)
            for i, form in enumerate(detalle_formset):
                if not form.is_valid():
                    print(f"Form {i} errors:", form.errors)
        
        if venta_form.is_valid() and detalle_formset.is_valid():
            return self.form_valid(venta_form, detalle_formset)
        else:
            return self.form_invalid(venta_form, detalle_formset)
    
    def form_valid(self, venta_form, detalle_formset):
        try:
            with transaction.atomic():
                # Primero verificamos si hay stock suficiente para todos los productos
                detalles_temp = detalle_formset.save(commit=False)
                for detalle in detalles_temp:
                    stock_actual = Stock.objects.filter(producto=detalle.producto, en_uso=True).first()
                    if not stock_actual or stock_actual.cantidad < detalle.cantidad:
                        producto_nombre = detalle.producto.nombre
                        cantidad_disponible = stock_actual.cantidad if stock_actual else 0
                        mensaje_error = f"Stock insuficiente para <strong>{producto_nombre}</strong>. <br>Disponible: <strong>{cantidad_disponible}</strong>, Solicitado: <strong>{detalle.cantidad}</strong>"
                        raise ValueError(mensaje_error)
                
                # Obtenemos los estados de pago predeterminados
                try:
                    estado_completo = EstadoPago.objects.get(estado='Completo')
                    estado_parcial = EstadoPago.objects.get(estado='Parcial')
                    estado_debe = EstadoPago.objects.get(estado='Debe Total')
                except EstadoPago.DoesNotExist:
                    # Si hay un error al obtener los estados, mostramos un mensaje de error
                    raise ValueError('No se encontraron los estados de pago necesarios. Por favor, crea los estados "Completo", "Parcial" y "Debe Total" en la sección de Estados de Pago.')
                
                # Si hay stock suficiente, guardamos la venta
                venta = venta_form.save(commit=False)
                venta.total = Decimal('0.00')  # Inicializamos el total
                
                # Obtenemos el monto pagado del formulario
                monto_pagado = venta_form.cleaned_data.get('monto_pagado', Decimal('0.00'))
                if monto_pagado is None:
                    monto_pagado = Decimal('0.00')
                venta.monto_pagado = monto_pagado
                
                # Usamos el estado de pago seleccionado por el usuario
                # El estado de pago se actualizará más adelante según el monto pagado
                venta.save()
                print("Venta guardada con ID:", venta.id)
                
                # Guardamos los detalles y calculamos el total
                detalles = detalle_formset.save(commit=False)
                total = Decimal('0.00')
                
                print("Número de detalles a guardar:", len(detalles))
                for i, detalle in enumerate(detalles):
                    try:
                        detalle.venta = venta
                        
                        # Aseguramos que los campos de precio estén correctamente configurados
                        if not detalle.precio_unitario or detalle.precio_unitario == 0:
                            # Si no tiene precio unitario, obtenemos el precio del producto
                            detalle.precio_unitario = detalle.producto.precio
                        
                        # Aseguramos que precio_costo tenga el mismo valor que precio_unitario
                        detalle.precio_costo = detalle.precio_unitario
                        
                        # Aseguramos que el porcentaje de ganancia tenga un valor válido
                        if not detalle.porcentaje_ganancia or detalle.porcentaje_ganancia == 0:
                            detalle.porcentaje_ganancia = Decimal('20.00')  # Valor predeterminado
                        
                        # Calculamos el precio de venta basado en el porcentaje de ganancia
                        detalle.precio_venta = detalle.precio_costo * (1 + detalle.porcentaje_ganancia / 100)
                        
                        # Calculamos el subtotal
                        subtotal = detalle.cantidad * detalle.precio_venta
                        total += subtotal
                        
                        print(f"Detalle {i+1} a guardar: producto={detalle.producto.id}, cantidad={detalle.cantidad}, precio_unitario={detalle.precio_unitario}, precio_costo={detalle.precio_costo}, porcentaje={detalle.porcentaje_ganancia}, precio_venta={detalle.precio_venta}, subtotal={subtotal}")
                        
                        detalle.save()
                        print(f"Detalle {i+1} guardado con ID: {detalle.id}")
                        
                        # Actualizar el stock (restar la cantidad vendida)
                        Stock.actualizar_stock(detalle.producto.id, detalle.cantidad, es_venta=True)
                        print(f"Stock actualizado para producto {detalle.producto.id}: -{detalle.cantidad}")
                    except Exception as e:
                        print(f"Error al guardar detalle {i+1}:", str(e))
                        raise
                
                # Eliminamos los detalles marcados para eliminar
                for detalle in detalle_formset.deleted_objects:
                    detalle.delete()
                
                # Actualizamos el total de la venta
                venta.total = total
                
                # Calculamos el saldo pendiente
                venta.saldo_pendiente = venta.total - venta.monto_pagado
                
                # Actualizamos el estado de pago según el monto pagado
                if venta.monto_pagado >= venta.total:
                    # Pago completo
                    venta.estado_pago = estado_completo
                    venta.saldo_pendiente = Decimal('0.00')  # Aseguramos que no quede negativo
                elif venta.monto_pagado > 0:
                    # Pago parcial
                    venta.estado_pago = estado_parcial
                else:
                    # Debe total
                    venta.estado_pago = estado_debe
                    venta.saldo_pendiente = venta.total
                
                venta.save()
                print(f"Total de la venta actualizado: {venta.total}, Monto pagado: {venta.monto_pagado}, Saldo pendiente: {venta.saldo_pendiente}")
                
                # Si hay un pago inicial, registramos el pago
                if venta.monto_pagado > 0:
                    # Obtenemos el método de pago predeterminado o el primero disponible
                    try:
                        metodo_pago = MetodoPago.objects.first()
                        if not metodo_pago:
                            # Si no hay métodos de pago, creamos uno predeterminado
                            metodo_pago = MetodoPago.objects.create(nombre='Efectivo')
                        
                        # Registramos el pago
                        Pago.objects.create(
                            venta=venta,
                            monto=venta.monto_pagado,
                            metodo_pago=metodo_pago
                        )
                        print(f"Pago registrado por {venta.monto_pagado}")
                    except Exception as e:
                        print(f"Error al registrar el pago: {str(e)}")
            
            messages.success(self.request, 'Venta creada con éxito')
            return redirect('productos:venta_detail', pk=venta.pk)
        except Exception as e:
            print("Error al guardar la venta:", str(e))
            messages.error(self.request, f'Error al crear la venta: {str(e)}')
            return self.form_invalid(venta_form, detalle_formset)
    
    def form_invalid(self, venta_form, detalle_formset):
        return render(self.request, self.template_name, {
            'venta_form': venta_form,
            'detalle_formset': detalle_formset,
            'productos': Producto.objects.all(),
        })

class VentaUpdateView(View):
    template_name = 'productos/venta_form.html'
    
    def get_object(self):
        return get_object_or_404(Venta, pk=self.kwargs['pk'])
    
    def get(self, request, *args, **kwargs):
        venta = self.get_object()
        venta_form = VentaForm(instance=venta, prefix='venta')
        detalle_formset = DetalleVentaFormSet(instance=venta, prefix='detalles')
        
        return render(request, self.template_name, {
            'venta_form': venta_form,
            'detalle_formset': detalle_formset,
            'productos': Producto.objects.all(),
            'object': venta,  # Para que la plantilla sepa que es una edición
        })
    
    def post(self, request, *args, **kwargs):
        venta = self.get_object()
        venta_form = VentaForm(request.POST, instance=venta, prefix='venta')
        detalle_formset = DetalleVentaFormSet(request.POST, instance=venta, prefix='detalles')
        
        # Agregar mensajes de depuración
        print("[UPDATE] Venta form is valid:", venta_form.is_valid())
        if not venta_form.is_valid():
            print("[UPDATE] Venta form errors:", venta_form.errors)
        
        print("[UPDATE] Detalle formset is valid:", detalle_formset.is_valid())
        if not detalle_formset.is_valid():
            print("[UPDATE] Detalle formset errors:", detalle_formset.errors)
            for i, form in enumerate(detalle_formset):
                if not form.is_valid():
                    print(f"[UPDATE] Form {i} errors:", form.errors)
        
        if venta_form.is_valid() and detalle_formset.is_valid():
            return self.form_valid(venta_form, detalle_formset)
        else:
            return self.form_invalid(venta_form, detalle_formset)
    
    def form_valid(self, venta_form, detalle_formset):
        try:
            with transaction.atomic():
                # Obtenemos la venta original para comparar cambios
                venta_original = self.get_object()
                venta_original_detalles = {d.id: d for d in venta_original.detalleventa_set.all()}
                
                # Guardamos la venta sin actualizar el total todavía
                venta = venta_form.save(commit=False)
                print("[UPDATE] Venta a actualizar con ID:", venta.id)
                
                # Primero verificamos si hay stock suficiente para los nuevos detalles o aumentos de cantidad
                detalles_temp = detalle_formset.save(commit=False)
                for detalle in detalles_temp:
                    # Si es un detalle existente, verificamos si aumentó la cantidad
                    if detalle.id and detalle.id in venta_original_detalles:
                        detalle_original = venta_original_detalles[detalle.id]
                        cantidad_adicional = detalle.cantidad - detalle_original.cantidad
                        
                        # Si la cantidad aumentó, verificamos stock
                        if cantidad_adicional > 0:
                            stock_actual = Stock.objects.filter(producto=detalle.producto, en_uso=True).first()
                            if not stock_actual or stock_actual.cantidad < cantidad_adicional:
                                producto_nombre = detalle.producto.nombre
                                cantidad_disponible = stock_actual.cantidad if stock_actual else 0
                                mensaje_error = f"Stock insuficiente para aumentar <strong>{producto_nombre}</strong>. <br>Disponible: <strong>{cantidad_disponible}</strong>, Adicional requerido: <strong>{cantidad_adicional}</strong>"
                                raise ValueError(mensaje_error)
                    # Si es un detalle nuevo, verificamos stock para toda la cantidad
                    elif not detalle.id:
                        stock_actual = Stock.objects.filter(producto=detalle.producto, en_uso=True).first()
                        if not stock_actual or stock_actual.cantidad < detalle.cantidad:
                            producto_nombre = detalle.producto.nombre
                            cantidad_disponible = stock_actual.cantidad if stock_actual else 0
                            mensaje_error = f"Stock insuficiente para <strong>{producto_nombre}</strong>. <br>Disponible: <strong>{cantidad_disponible}</strong>, Solicitado: <strong>{detalle.cantidad}</strong>"
                            raise ValueError(mensaje_error)
                
                # Guardamos los detalles y calculamos el total
                detalles = detalle_formset.save(commit=False)
                total = Decimal('0.00')
                
                print("[UPDATE] Número de detalles a guardar/actualizar:", len(detalles))
                for i, detalle in enumerate(detalles):
                    try:
                        detalle.venta = venta
                        
                        # Aseguramos que los campos de precio estén correctamente configurados
                        if not detalle.precio_unitario or detalle.precio_unitario == 0:
                            # Si no tiene precio unitario, obtenemos el precio del producto
                            detalle.precio_unitario = detalle.producto.precio
                        
                        # Aseguramos que precio_costo tenga el mismo valor que precio_unitario
                        detalle.precio_costo = detalle.precio_unitario
                        
                        # Aseguramos que el porcentaje de ganancia tenga un valor válido
                        if not detalle.porcentaje_ganancia or detalle.porcentaje_ganancia == 0:
                            detalle.porcentaje_ganancia = Decimal('20.00')  # Valor predeterminado
                        
                        # Calculamos el precio de venta basado en el porcentaje de ganancia
                        detalle.precio_venta = detalle.precio_costo * (1 + detalle.porcentaje_ganancia / 100)
                        
                        # Calculamos el subtotal
                        subtotal = detalle.cantidad * detalle.precio_venta
                        total += subtotal
                        
                        print(f"[UPDATE] Detalle {i+1} a actualizar: producto={detalle.producto.id}, cantidad={detalle.cantidad}, precio_unitario={detalle.precio_unitario}, precio_costo={detalle.precio_costo}, porcentaje={detalle.porcentaje_ganancia}, precio_venta={detalle.precio_venta}, subtotal={subtotal}")
                        
                        # Actualizamos el stock según los cambios en la cantidad
                        if detalle.id and detalle.id in venta_original_detalles:
                            # Es un detalle existente, calculamos la diferencia de cantidad
                            detalle_original = venta_original_detalles[detalle.id]
                            diferencia = detalle.cantidad - detalle_original.cantidad
                            
                            if diferencia != 0:  # Solo actualizamos si hay cambio en la cantidad
                                # Si diferencia > 0, se está agregando más (es_venta=True)
                                # Si diferencia < 0, se está devolviendo al stock (es_venta=False)
                                Stock.actualizar_stock(detalle.producto.id, abs(diferencia), es_venta=(diferencia > 0))
                                print(f"[UPDATE] Stock actualizado para producto {detalle.producto.id}: {'-' if diferencia > 0 else '+'}{abs(diferencia)}")
                        else:
                            # Es un detalle nuevo, restamos todo del stock
                            Stock.actualizar_stock(detalle.producto.id, detalle.cantidad, es_venta=True)
                            print(f"[UPDATE] Stock actualizado para producto {detalle.producto.id}: -{detalle.cantidad}")
                        
                        detalle.save()
                        print(f"[UPDATE] Detalle {i+1} guardado: producto={detalle.producto.id}, cantidad={detalle.cantidad}, precio_venta={detalle.precio_venta}")
                    except Exception as e:
                        print(f"[UPDATE] Error al guardar detalle {i+1}:", str(e))
                        raise
                
                # Para los detalles eliminados, devolvemos la cantidad al stock
                print("[UPDATE] Detalles a eliminar:", len(detalle_formset.deleted_objects))
                for detalle in detalle_formset.deleted_objects:
                    # Devolvemos la cantidad al stock (es_venta=False)
                    Stock.actualizar_stock(detalle.producto.id, detalle.cantidad, es_venta=False)
                    print(f"[UPDATE] Stock actualizado para producto {detalle.producto.id} (eliminado): +{detalle.cantidad}")
                    detalle.delete()
                
                # Actualizamos el total de la venta
                venta.total = total
                venta.save()
                print("[UPDATE] Total de venta actualizado:", venta.total)
            
            messages.success(self.request, 'Venta actualizada con éxito')
            return redirect('productos:venta_detail', pk=venta.pk)
        except Exception as e:
            print("[UPDATE] Error al actualizar la venta:", str(e))
            messages.error(self.request, f'Error al actualizar la venta: {str(e)}')
            return self.form_invalid(venta_form, detalle_formset)
    
    def form_invalid(self, venta_form, detalle_formset):
        return render(self.request, self.template_name, {
            'venta_form': venta_form,
            'detalle_formset': detalle_formset,
            'productos': Producto.objects.all(),
            'object': self.get_object(),  # Para que la plantilla sepa que es una edición
        })

class VentaDeleteView(DeleteView):
    model = Venta
    template_name = 'productos/venta_confirm_delete.html'
    success_url = reverse_lazy('productos:venta_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Venta eliminada con éxito')
        return super().delete(request, *args, **kwargs)

# Vistas para DetalleVenta
class DetalleVentaListView(ListView):
    model = DetalleVenta
    template_name = 'productos/detalleventa_list.html'
    context_object_name = 'detalles_venta'

class DetalleVentaDetailView(DetailView):
    model = DetalleVenta
    template_name = 'productos/detalleventa_detail.html'
    context_object_name = 'detalleventa'

class DetalleVentaCreateView(CreateView):
    model = DetalleVenta
    template_name = 'productos/detalleventa_form.html'
    fields = ['venta', 'producto', 'cantidad', 'precio_unitario']
    success_url = reverse_lazy('productos:detalleventa_list')

    def form_valid(self, form):
        messages.success(self.request, 'Detalle de venta creado con éxito')
        return super().form_valid(form)

class DetalleVentaUpdateView(UpdateView):
    model = DetalleVenta
    template_name = 'productos/detalleventa_form.html'
    fields = ['venta', 'producto', 'cantidad', 'precio_unitario']
    success_url = reverse_lazy('productos:detalleventa_list')

    def form_valid(self, form):
        messages.success(self.request, 'Detalle de venta actualizado con éxito')
        return super().form_valid(form)

class DetalleVentaDeleteView(DeleteView):
    model = DetalleVenta
    template_name = 'productos/detalleventa_confirm_delete.html'
    success_url = reverse_lazy('productos:detalleventa_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Detalle de venta eliminado con éxito')
        return super().delete(request, *args, **kwargs)

# Vistas para MetodoPago
class MetodoPagoListView(ListView):
    model = MetodoPago
    template_name = 'productos/metodopago_list.html'
    context_object_name = 'metodos_pago'

class MetodoPagoDetailView(DetailView):
    model = MetodoPago
    template_name = 'productos/metodopago_detail.html'
    context_object_name = 'metodopago'

class MetodoPagoCreateView(CreateView):
    model = MetodoPago
    template_name = 'productos/metodopago_form.html'
    fields = ['metodo']
    success_url = reverse_lazy('productos:metodopago_list')

    def form_valid(self, form):
        messages.success(self.request, 'Método de pago creado con éxito')
        return super().form_valid(form)

class MetodoPagoUpdateView(UpdateView):
    model = MetodoPago
    template_name = 'productos/metodopago_form.html'
    fields = ['metodo']
    success_url = reverse_lazy('productos:metodopago_list')

    def form_valid(self, form):
        messages.success(self.request, 'Método de pago actualizado con éxito')
        return super().form_valid(form)

class MetodoPagoDeleteView(DeleteView):
    model = MetodoPago
    template_name = 'productos/metodopago_confirm_delete.html'
    success_url = reverse_lazy('productos:metodopago_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Método de pago eliminado con éxito')
        return super().delete(request, *args, **kwargs)

# Vistas para Pago
class PagoListView(ListView):
    model = Pago
    template_name = 'productos/pago_list.html'
    context_object_name = 'pagos'

class PagoDetailView(DetailView):
    model = Pago
    template_name = 'productos/pago_detail.html'
    context_object_name = 'pago'

class PagoCreateView(CreateView):
    model = Pago
    template_name = 'productos/pago_form.html'
    fields = ['venta', 'monto', 'metodo_pago']
    success_url = reverse_lazy('productos:pago_list')

    def form_valid(self, form):
        messages.success(self.request, 'Pago creado con éxito')
        return super().form_valid(form)

class PagoUpdateView(UpdateView):
    model = Pago
    template_name = 'productos/pago_form.html'
    fields = ['venta', 'monto', 'metodo_pago']
    success_url = reverse_lazy('productos:pago_list')

    def form_valid(self, form):
        messages.success(self.request, 'Pago actualizado con éxito')
        return super().form_valid(form)

class PagoDeleteView(DeleteView):
    model = Pago
    template_name = 'productos/pago_confirm_delete.html'
    success_url = reverse_lazy('productos:pago_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Pago eliminado con éxito')
        return super().delete(request, *args, **kwargs)

# Vistas para Devolucion
class DevolucionListView(ListView):
    model = Devolucion
    template_name = 'productos/devolucion_list.html'
    context_object_name = 'devoluciones'

class DevolucionDetailView(DetailView):
    model = Devolucion
    template_name = 'productos/devolucion_detail.html'
    context_object_name = 'devolucion'

class DevolucionCreateView(CreateView):
    model = Devolucion
    template_name = 'productos/devolucion_form.html'
    fields = ['venta', 'producto', 'cantidad', 'volver_al_stock', 'motivo']
    success_url = reverse_lazy('productos:devolucion_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Añadir clases CSS y placeholders para mejorar la apariencia
        form.fields['volver_al_stock'].widget.attrs.update({
            'class': 'form-check-input',
        })
        form.fields['motivo'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Indique el motivo de la devolución',
            'rows': 3,
        })
        return form

    def form_valid(self, form):
        # Guardar la devolución
        devolucion = form.save(commit=False)
        
        try:
            # Si el producto debe volver al stock, actualizamos el stock
            if devolucion.volver_al_stock:
                # Actualizamos el stock (sumamos la cantidad devuelta)
                Stock.actualizar_stock(
                    producto_id=devolucion.producto.id,
                    cantidad=devolucion.cantidad,
                    es_venta=False  # False indica que se suma al stock
                )
                messages.success(self.request, f'Devolución creada con éxito. Se han añadido {devolucion.cantidad} unidades al stock.')
            else:
                messages.success(self.request, 'Devolución creada con éxito. El producto NO se ha devuelto al stock.')
                
            # Guardar la devolución
            devolucion.save()
            return redirect(self.success_url)
            
        except Exception as e:
            messages.error(self.request, f'Error al procesar la devolución: {str(e)}')
            return self.form_invalid(form)

class DevolucionUpdateView(UpdateView):
    model = Devolucion
    template_name = 'productos/devolucion_form.html'
    fields = ['venta', 'producto', 'cantidad', 'volver_al_stock', 'motivo']
    success_url = reverse_lazy('productos:devolucion_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Añadir clases CSS y placeholders para mejorar la apariencia
        form.fields['volver_al_stock'].widget.attrs.update({
            'class': 'form-check-input',
        })
        form.fields['motivo'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Indique el motivo de la devolución',
            'rows': 3,
        })
        return form

    def form_valid(self, form):
        # Obtener la devolución original antes de los cambios
        devolucion_original = Devolucion.objects.get(pk=self.object.pk)
        volver_al_stock_original = devolucion_original.volver_al_stock
        cantidad_original = devolucion_original.cantidad
        
        # Guardar la devolución actualizada
        devolucion = form.save(commit=False)
        
        try:
            # Calcular la diferencia de cantidad si ha cambiado
            diferencia_cantidad = devolucion.cantidad - cantidad_original
            
            # Manejar los cambios en el stock según los cambios en la devolución
            if diferencia_cantidad != 0 or volver_al_stock_original != devolucion.volver_al_stock:
                # Caso 1: Antes no volvía al stock, ahora sí
                if not volver_al_stock_original and devolucion.volver_al_stock:
                    # Añadir toda la cantidad al stock
                    Stock.actualizar_stock(
                        producto_id=devolucion.producto.id,
                        cantidad=devolucion.cantidad,
                        es_venta=False
                    )
                    messages.success(self.request, f'Se han añadido {devolucion.cantidad} unidades al stock.')
                
                # Caso 2: Antes volvía al stock, ahora no
                elif volver_al_stock_original and not devolucion.volver_al_stock:
                    # Quitar toda la cantidad del stock
                    Stock.actualizar_stock(
                        producto_id=devolucion.producto.id,
                        cantidad=cantidad_original,
                        es_venta=True
                    )
                    messages.success(self.request, f'Se han quitado {cantidad_original} unidades del stock.')
                
                # Caso 3: Sigue volviendo al stock pero cambió la cantidad
                elif volver_al_stock_original and devolucion.volver_al_stock and diferencia_cantidad != 0:
                    # Actualizar el stock con la diferencia
                    Stock.actualizar_stock(
                        producto_id=devolucion.producto.id,
                        cantidad=diferencia_cantidad,
                        es_venta=diferencia_cantidad < 0  # Si es negativo, es una venta (resta)
                    )
                    if diferencia_cantidad > 0:
                        messages.success(self.request, f'Se han añadido {diferencia_cantidad} unidades adicionales al stock.')
                    else:
                        messages.success(self.request, f'Se han quitado {abs(diferencia_cantidad)} unidades del stock.')
            
            # Guardar la devolución
            devolucion.save()
            messages.success(self.request, 'Devolución actualizada con éxito')
            return redirect(self.success_url)
            
        except Exception as e:
            messages.error(self.request, f'Error al actualizar la devolución: {str(e)}')
            return self.form_invalid(form)

class DevolucionDeleteView(DeleteView):
    model = Devolucion
    template_name = 'productos/devolucion_confirm_delete.html'
    success_url = reverse_lazy('productos:devolucion_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Devolución eliminada con éxito')
        return super().delete(request, *args, **kwargs)


# Vistas para gestionar clientes con deudas pendientes y pagos
class RegistrarPagoView(LoginRequiredMixin, View):
    template_name = 'productos/registrar_pago.html'
    
    def get(self, request, venta_id, *args, **kwargs):
        try:
            venta = Venta.objects.get(pk=venta_id)
            metodos_pago = MetodoPago.objects.all()
            
            return render(request, self.template_name, {
                'venta': venta,
                'metodos_pago': metodos_pago,
            })
        except Venta.DoesNotExist:
            messages.error(request, 'La venta no existe')
            return redirect('productos:venta_list')
    
    def post(self, request, venta_id, *args, **kwargs):
        try:
            venta = Venta.objects.get(pk=venta_id)
            monto = Decimal(request.POST.get('monto', '0'))
            metodo_pago_id = request.POST.get('metodo_pago')
            
            # Validaciones
            if monto <= 0:
                messages.error(request, 'El monto debe ser mayor a cero')
                return redirect('productos:registrar_pago', venta_id=venta_id)
            
            if monto > venta.saldo_pendiente:
                messages.error(request, f'El monto no puede ser mayor al saldo pendiente (${venta.saldo_pendiente})')
                return redirect('productos:registrar_pago', venta_id=venta_id)
            
            try:
                metodo_pago = MetodoPago.objects.get(pk=metodo_pago_id)
            except MetodoPago.DoesNotExist:
                messages.error(request, 'El método de pago seleccionado no existe')
                return redirect('productos:registrar_pago', venta_id=venta_id)
            
            # Registrar el pago
            with transaction.atomic():
                # Crear el pago
                pago = Pago.objects.create(
                    venta=venta,
                    monto=monto,
                    metodo_pago=metodo_pago
                )
                
                # Actualizar la venta
                venta.monto_pagado += monto
                venta.actualizar_saldo()
                
                messages.success(request, f'Pago de ${monto} registrado con éxito. Saldo pendiente: ${venta.saldo_pendiente}')
                
                # Redirigir a la página de detalle de la venta
                return redirect('productos:venta_detail', pk=venta_id)
                
        except Venta.DoesNotExist:
            messages.error(request, 'La venta no existe')
            return redirect('productos:venta_list')
        except Exception as e:
            messages.error(request, f'Error al registrar el pago: {str(e)}')
            return redirect('productos:registrar_pago', venta_id=venta_id)


# Vistas para gestionar clientes con deudas pendientes
# Vista para generar PDF de remito para una venta
class VentaPDFView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        try:
            venta = Venta.objects.get(pk=pk)
            
            # Crear un buffer para el PDF
            buffer = BytesIO()
            
            # Crear el documento PDF
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Contenedor para los elementos del PDF
            elements = []
            
            # Estilos
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(
                name='Centered',
                parent=styles['Heading1'],
                alignment=TA_CENTER
            ))
            styles.add(ParagraphStyle(
                name='Right',
                parent=styles['Normal'],
                alignment=TA_RIGHT
            ))
            
            # Título
            elements.append(Paragraph("REMITO DE VENTA", styles['Centered']))
            elements.append(Spacer(1, 0.5*cm))
            
            # Información de la venta
            fecha = venta.fecha.strftime("%d/%m/%Y %H:%M")
            elements.append(Paragraph(f"<b>Fecha:</b> {fecha}", styles['Normal']))
            elements.append(Paragraph(f"<b>Cliente:</b> {venta.cliente.nombre}", styles['Normal']))
            elements.append(Paragraph(f"<b>Número de Venta:</b> {venta.id}", styles['Normal']))
            elements.append(Spacer(1, 0.5*cm))
            
            # Tabla de productos
            data = [
                ['Producto', 'Cantidad', 'Precio Unitario', 'Subtotal']
            ]
            
            # Añadir detalles de la venta
            total = Decimal('0.00')
            for detalle in venta.detalleventa_set.all():
                # Usar el precio de venta (con ganancia) en lugar del precio de costo
                precio_unitario = detalle.precio_venta
                subtotal = detalle.cantidad * precio_unitario
                total += subtotal
                
                data.append([
                    detalle.producto.nombre,
                    str(detalle.cantidad),
                    f"${precio_unitario:.2f}",
                    f"${subtotal:.2f}"
                ])
            
            # Añadir fila de total
            data.append(['', '', '<b>Total</b>', f"<b>${total:.2f}</b>"])
            
            # Crear la tabla
            table = Table(data, colWidths=[8*cm, 2*cm, 3*cm, 3*cm])
            
            # Estilo de la tabla
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 1*cm))
            
            # Información adicional
            elements.append(Paragraph("<b>Observaciones:</b>", styles['Normal']))
            elements.append(Paragraph("Este documento sirve como comprobante de entrega de los productos detallados.", styles['Normal']))
            elements.append(Spacer(1, 1*cm))
            
            # Firmas
            elements.append(Paragraph("_____________________", styles['Normal']))
            elements.append(Paragraph("Firma del Cliente", styles['Normal']))
            
            # Construir el PDF
            doc.build(elements)
            
            # Obtener el valor del buffer y crear la respuesta HTTP
            pdf = buffer.getvalue()
            buffer.close()
            
            # Crear la respuesta HTTP con el PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="remito_venta_{venta.id}.pdf"'
            response.write(pdf)
            
            return response
            
        except Venta.DoesNotExist:
            messages.error(request, 'La venta no existe')
            return redirect('productos:venta_list')
        except Exception as e:
            messages.error(request, f'Error al generar el PDF: {str(e)}')
            return redirect('productos:venta_detail', pk=pk)


# Vistas para gestionar zonas
class ZonaListView(LoginRequiredMixin, ListView):
    model = Zona
    template_name = 'productos/zona_list.html'
    context_object_name = 'zonas'


class ZonaDetailView(LoginRequiredMixin, DetailView):
    model = Zona
    template_name = 'productos/zona_detail.html'
    context_object_name = 'zona'


class ZonaCreateView(LoginRequiredMixin, CreateView):
    model = Zona
    template_name = 'productos/zona_form.html'
    fields = ['nombre', 'localidades']
    success_url = reverse_lazy('productos:zona_list')

    def form_valid(self, form):
        messages.success(self.request, 'Zona creada con éxito')
        return super().form_valid(form)


class ZonaUpdateView(LoginRequiredMixin, UpdateView):
    model = Zona
    template_name = 'productos/zona_form.html'
    fields = ['nombre', 'localidades']
    success_url = reverse_lazy('productos:zona_list')

    def form_valid(self, form):
        messages.success(self.request, 'Zona actualizada con éxito')
        return super().form_valid(form)


class ZonaDeleteView(LoginRequiredMixin, DeleteView):
    model = Zona
    template_name = 'productos/zona_confirm_delete.html'
    success_url = reverse_lazy('productos:zona_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Zona eliminada con éxito')
        return super().delete(request, *args, **kwargs)


# Vistas para gestionar clientes con deudas pendientes
class ClientesDeudoresView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'productos/clientes_deudores.html'
    context_object_name = 'clientes'
    
    def get_queryset(self):
        # Obtener clientes con ventas que tienen saldo pendiente
        return Cliente.objects.filter(
            venta__saldo_pendiente__gt=0
        ).distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Para cada cliente, obtener sus ventas con saldo pendiente
        clientes_con_deudas = []
        for cliente in context['clientes']:
            ventas_pendientes = Venta.objects.filter(
                cliente=cliente,
                saldo_pendiente__gt=0
            )
            total_deuda = sum(venta.saldo_pendiente for venta in ventas_pendientes)
            
            clientes_con_deudas.append({
                'cliente': cliente,
                'ventas_pendientes': ventas_pendientes,
                'total_deuda': total_deuda,
                'cantidad_ventas': ventas_pendientes.count()
            })
        
        context['clientes_con_deudas'] = clientes_con_deudas
        return context
