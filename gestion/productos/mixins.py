from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import DeleteView

class UserDataMixin(LoginRequiredMixin):
    """
    Mixin para filtrar los datos por usuario autenticado.
    Debe ser usado con vistas basadas en clases que tengan un método get_queryset.
    """
    
    def get_queryset(self):
        """
        Filtra el queryset para mostrar solo los datos del usuario autenticado.
        Si el usuario es staff o superuser, puede ver todos los datos.
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        # Si el usuario es staff o superuser, puede ver todos los datos
        if user.is_staff or user.is_superuser:
            return queryset
            
        # Si el modelo tiene un campo usuario, filtramos por ese campo
        if hasattr(queryset.model, 'usuario'):
            # Incluir tanto los elementos del usuario como los que no tienen usuario asignado
            return queryset.filter(Q(usuario=user) | Q(usuario__isnull=True))
            
        return queryset
    
    def form_valid(self, form):
        """
        Asigna el usuario autenticado al objeto que se está creando o actualizando.
        Solo aplica para vistas CreateView y UpdateView, no para DeleteView.
        """
        # Verificar si estamos en una vista de eliminación
        if isinstance(self, DeleteView):
            return super().form_valid(form)
            
        # Para vistas de creación y actualización
        if hasattr(form, 'instance') and hasattr(form.instance, 'usuario') and not form.instance.usuario:
            form.instance.usuario = self.request.user
        return super().form_valid(form)
