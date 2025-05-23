"""
URL configuration for gestion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Redirigir /accounts/login/ a /login/
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=True)),
    # Incluir todas las URLs de la aplicación productos
    path('', include('productos.urls')),
]

# Añadir URLs para servir archivos multimedia durante el desarrollo
# En producción (Vercel), esto no funcionará directamente y necesitarás un servicio de almacenamiento externo
# Sin embargo, lo dejamos configurado para que funcione en desarrollo y para que Vercel al menos
# intente servir los archivos de media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
