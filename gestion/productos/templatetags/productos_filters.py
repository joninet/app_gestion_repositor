from django import template
from django.db.models import Model

register = template.Library()

@register.filter
def get_attribute(obj, attr_name):
    """
    Obtiene un atributo de un objeto, incluyendo atributos anidados.
    Ejemplo: {{ object|get_attribute:'cliente.nombre' }}
    """
    if not attr_name:
        return ""
    
    # Manejar atributos anidados (por ejemplo, 'cliente.nombre')
    attrs = attr_name.split('.')
    value = obj
    
    for attr in attrs:
        if hasattr(value, attr):
            value = getattr(value, attr)
            # Si es un método, llamarlo
            if callable(value) and not isinstance(value, type):
                value = value()
        elif isinstance(value, dict) and attr in value:
            value = value[attr]
        else:
            return ""
    
    # Si es un modelo, usar su representación de cadena
    if isinstance(value, Model):
        return str(value)
    
    return value
