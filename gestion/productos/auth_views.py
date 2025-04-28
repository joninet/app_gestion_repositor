from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count

from .models import Venta, Producto, Cliente, Proveedor

def login_view(request):
    if request.user.is_authenticated:
        return redirect('productos:dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido, {username}!')
            return redirect('productos:dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'productos/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, '¡Has cerrado sesión correctamente!')
    return redirect('productos:login')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('productos:dashboard')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}! Ahora puedes iniciar sesión.')
            return redirect('productos:login')
    else:
        form = UserCreationForm()
    
    return render(request, 'productos/register.html', {'form': form})

@login_required
def profile_view(request):
    # Contar elementos asociados al usuario
    ventas_count = Venta.objects.filter(usuario=request.user).count()
    productos_count = Producto.objects.filter(usuario=request.user).count()
    clientes_count = Cliente.objects.filter(usuario=request.user).count()
    proveedores_count = Proveedor.objects.filter(usuario=request.user).count()
    
    context = {
        'ventas_count': ventas_count,
        'productos_count': productos_count,
        'clientes_count': clientes_count,
        'proveedores_count': proveedores_count,
    }
    
    return render(request, 'productos/profile.html', context)

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Mantener la sesión activa después de cambiar la contraseña
            update_session_auth_hash(request, user)
            messages.success(request, '¡Tu contraseña ha sido actualizada correctamente!')
            return redirect('productos:profile')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'productos/change_password.html', {'form': form})
