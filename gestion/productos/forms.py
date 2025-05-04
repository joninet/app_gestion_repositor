from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from .models import Venta, DetalleVenta, Cliente, EstadoPago, Producto, Catalogo, ProductoCatalogo

class VentaForm(forms.ModelForm):
    monto_pagado = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        help_text='Monto pagado por el cliente'
    )
    
    class Meta:
        model = Venta
        fields = ['cliente', 'estado_pago', 'monto_pagado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'estado_pago': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Permitimos seleccionar el estado de pago
        self.fields['estado_pago'].required = True
        
        # Añadimos ayuda para el campo de estado de pago
        self.fields['estado_pago'].help_text = 'Seleccione el estado de pago inicial. Se actualizará automáticamente según el monto pagado.'
        
        # Si es una instancia existente, establecemos el valor inicial del monto pagado
        if self.instance and self.instance.pk:
            self.fields['monto_pagado'].initial = self.instance.monto_pagado

class DetalleVentaForm(forms.ModelForm):
    precio_unitario = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        initial=0,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control precio-unitario-input', 'step': '0.01'})
    )
    precio_costo = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        initial=0,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control precio-costo-input', 'step': '0.01'})
    )
    porcentaje_ganancia = forms.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        initial=20, 
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control porcentaje-input', 'step': '0.01'})
    )
    precio_venta = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        initial=0,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control precio-venta-input', 'step': '0.01'})
    )
    
    # Aseguramos que la cantidad tenga un valor predeterminado
    cantidad = forms.IntegerField(
        min_value=1,
        initial=1,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control cantidad-input', 'min': '1'})
    )

    class Meta:
        model = DetalleVenta
        fields = ['producto', 'precio_unitario', 'cantidad', 'precio_costo', 'porcentaje_ganancia', 'precio_venta']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control producto-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control cantidad-input', 'min': '1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegurarse de que cantidad tenga un valor por defecto
        if not self.initial.get('cantidad'):
            self.initial['cantidad'] = 1
        # Asegurarse de que precio_unitario y precio_costo sean iguales
        if self.instance and self.instance.precio_unitario:
            self.initial['precio_costo'] = self.instance.precio_unitario
            # Si hay precio_unitario pero no hay precio_venta, calcularlo
            if not self.instance.precio_venta:
                porcentaje = self.initial.get('porcentaje_ganancia', 20)
                self.initial['precio_venta'] = self.instance.precio_unitario * (1 + porcentaje / 100)

# Creamos un formset para DetalleVenta que estará vinculado a una Venta
DetalleVentaFormSet = inlineformset_factory(
    Venta, 
    DetalleVenta,
    form=DetalleVentaForm,
    extra=1,  # Número de formularios vacíos a mostrar
    can_delete=True  # Permitir eliminar líneas
)


class CatalogoForm(forms.ModelForm):
    class Meta:
        model = Catalogo
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProductoCatalogoForm(forms.ModelForm):
    class Meta:
        model = ProductoCatalogo
        fields = ['producto', 'porcentaje_ganancia', 'destacado', 'orden']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control producto-select'}),
            'porcentaje_ganancia': forms.NumberInput(attrs={'class': 'form-control porcentaje-input', 'step': '0.01', 'min': '0'}),
            'destacado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'orden': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si hay un producto seleccionado, mostrar su precio actual como referencia
        if self.instance and self.instance.producto_id:
            self.fields['producto'].help_text = f'Precio actual: ${self.instance.producto.precio}'


# Formset para productos en un catálogo
ProductoCatalogoFormSet = inlineformset_factory(
    Catalogo,
    ProductoCatalogo,
    form=ProductoCatalogoForm,
    extra=1,
    can_delete=True
)


# Formulario para seleccionar productos a añadir al catálogo
class SeleccionProductosForm(forms.Form):
    productos = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    porcentaje_ganancia_default = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        initial=20,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        help_text='Porcentaje de ganancia predeterminado para todos los productos seleccionados'
    )
    
    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        
        # Filtrar productos por usuario si no es staff/superuser
        if usuario and not (usuario.is_staff or usuario.is_superuser):
            self.fields['productos'].queryset = Producto.objects.filter(usuario=usuario)
