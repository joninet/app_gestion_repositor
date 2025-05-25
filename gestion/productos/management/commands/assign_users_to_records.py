from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from productos.models import UnidadMedida, Marca, Zona, MetodoPago, EstadoPago

class Command(BaseCommand):
    help = 'Asigna usuarios a registros existentes sin usuario asignado'

    def handle(self, *args, **kwargs):
        # Obtener todos los usuarios
        users = User.objects.all()
        
        if not users.exists():
            self.stdout.write(self.style.ERROR('No hay usuarios en el sistema'))
            return
            
        # Por defecto, asignar al primer usuario (puedes cambiar esto según tu lógica)
        default_user = users.first()
        self.stdout.write(f'Usuario por defecto: {default_user.username}')
        
        # Asignar usuario a UnidadMedida
        unidades = UnidadMedida.objects.filter(usuario__isnull=True)
        count = unidades.update(usuario=default_user)
        self.stdout.write(f'Asignadas {count} unidades de medida a {default_user.username}')
        
        # Asignar usuario a Marca
        marcas = Marca.objects.filter(usuario__isnull=True)
        count = marcas.update(usuario=default_user)
        self.stdout.write(f'Asignadas {count} marcas a {default_user.username}')
        
        # Asignar usuario a Zona
        zonas = Zona.objects.filter(usuario__isnull=True)
        count = zonas.update(usuario=default_user)
        self.stdout.write(f'Asignadas {count} zonas a {default_user.username}')
        
        # Asignar usuario a MetodoPago
        metodos = MetodoPago.objects.filter(usuario__isnull=True)
        count = metodos.update(usuario=default_user)
        self.stdout.write(f'Asignados {count} métodos de pago a {default_user.username}')
        
        # Asignar usuario a EstadoPago
        estados = EstadoPago.objects.filter(usuario__isnull=True)
        count = estados.update(usuario=default_user)
        self.stdout.write(f'Asignados {count} estados de pago a {default_user.username}')
        
        self.stdout.write(self.style.SUCCESS('Proceso completado con éxito'))
