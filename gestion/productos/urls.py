from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import auth_views as custom_auth_views
from . import dashboard_views
from . import user_views
from . import catalogo_views
from django.contrib.auth.decorators import login_required

app_name = 'productos'

urlpatterns = [
    # Autenticación
    path('login/', custom_auth_views.login_view, name='login'),
    path('logout/', custom_auth_views.logout_view, name='logout'),
    path('register/', custom_auth_views.register_view, name='register'),
    path('profile/', custom_auth_views.profile_view, name='profile'),
    path('change-password/', custom_auth_views.change_password_view, name='change_password'),
    
    # Dashboard
    path('dashboard/', dashboard_views.DashboardView.as_view(), name='dashboard'),
    
    # Vista de inicio (redirige a dashboard si está autenticado)
    path('', login_required(user_views.UserIndexView.as_view()), name='index'),
    # Proveedor URLs
    path('proveedores/', user_views.UserProveedorListView.as_view(), name='proveedor_list'),
    path('proveedores/nuevo/', user_views.UserProveedorCreateView.as_view(), name='proveedor_create'),
    path('proveedores/<int:pk>/', user_views.UserProveedorDetailView.as_view(), name='proveedor_detail'),
    path('proveedores/<int:pk>/editar/', user_views.UserProveedorUpdateView.as_view(), name='proveedor_update'),
    path('proveedores/<int:pk>/eliminar/', user_views.UserProveedorDeleteView.as_view(), name='proveedor_delete'),
    
    # UnidadMedida URLs
    path('unidades-medida/', user_views.UserUnidadMedidaListView.as_view(), name='unidadmedida_list'),
    path('unidades-medida/nueva/', user_views.UserUnidadMedidaCreateView.as_view(), name='unidadmedida_create'),
    path('unidades-medida/<int:pk>/', user_views.UserUnidadMedidaDetailView.as_view(), name='unidadmedida_detail'),
    path('unidades-medida/<int:pk>/editar/', user_views.UserUnidadMedidaUpdateView.as_view(), name='unidadmedida_update'),
    path('unidades-medida/<int:pk>/eliminar/', user_views.UserUnidadMedidaDeleteView.as_view(), name='unidadmedida_delete'),
    
    # Marca URLs
    path('marcas/', user_views.UserMarcaListView.as_view(), name='marca_list'),
    path('marcas/nueva/', user_views.UserMarcaCreateView.as_view(), name='marca_create'),
    path('marcas/<int:pk>/', user_views.UserMarcaDetailView.as_view(), name='marca_detail'),
    path('marcas/<int:pk>/editar/', user_views.UserMarcaUpdateView.as_view(), name='marca_update'),
    path('marcas/<int:pk>/eliminar/', user_views.UserMarcaDeleteView.as_view(), name='marca_delete'),
    
    # Producto URLs
    path('productos/', user_views.UserProductoListView.as_view(), name='producto_list'),
    path('productos/nuevo/', user_views.UserProductoCreateView.as_view(), name='producto_create'),
    path('productos/<int:pk>/', user_views.UserProductoDetailView.as_view(), name='producto_detail'),
    path('productos/<int:pk>/editar/', user_views.UserProductoUpdateView.as_view(), name='producto_update'),
    path('productos/<int:pk>/eliminar/', user_views.UserProductoDeleteView.as_view(), name='producto_delete'),
    
    # Stock URLs
    path('stocks/', user_views.UserStockListView.as_view(), name='stock_list'),
    path('stocks/nuevo/', user_views.UserStockCreateView.as_view(), name='stock_create'),
    path('stocks/<int:pk>/', user_views.UserStockDetailView.as_view(), name='stock_detail'),
    path('stocks/<int:pk>/editar/', user_views.UserStockUpdateView.as_view(), name='stock_update'),
    path('stocks/<int:pk>/eliminar/', user_views.UserStockDeleteView.as_view(), name='stock_delete'),
    
    # Zonas
    path('zonas/', login_required(views.ZonaListView.as_view()), name='zona_list'),
    path('zonas/<int:pk>/', login_required(views.ZonaDetailView.as_view()), name='zona_detail'),
    path('zonas/create/', login_required(views.ZonaCreateView.as_view()), name='zona_create'),
    path('zonas/<int:pk>/update/', login_required(views.ZonaUpdateView.as_view()), name='zona_update'),
    path('zonas/<int:pk>/delete/', login_required(views.ZonaDeleteView.as_view()), name='zona_delete'),
    
    # Cliente URLs
    path('clientes/', user_views.UserClienteListView.as_view(), name='cliente_list'),
    path('clientes/nuevo/', user_views.UserClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/<int:pk>/', user_views.UserClienteDetailView.as_view(), name='cliente_detail'),
    path('clientes/<int:pk>/editar/', user_views.UserClienteUpdateView.as_view(), name='cliente_update'),
    path('clientes/<int:pk>/eliminar/', user_views.UserClienteDeleteView.as_view(), name='cliente_delete'),
    
    # EstadoPago URLs
    path('estados-pago/', user_views.UserEstadoPagoListView.as_view(), name='estadopago_list'),
    path('estados-pago/nuevo/', user_views.UserEstadoPagoCreateView.as_view(), name='estadopago_create'),
    path('estados-pago/<int:pk>/', user_views.UserEstadoPagoDetailView.as_view(), name='estadopago_detail'),
    path('estados-pago/<int:pk>/editar/', user_views.UserEstadoPagoUpdateView.as_view(), name='estadopago_update'),
    path('estados-pago/<int:pk>/eliminar/', user_views.UserEstadoPagoDeleteView.as_view(), name='estadopago_delete'),
    
    # Venta URLs
    path('ventas/', user_views.UserVentaListView.as_view(), name='venta_list'),
    path('ventas/nueva/', user_views.UserVentaCreateView.as_view(), name='venta_create'),
    path('ventas/<int:pk>/', user_views.UserVentaDetailView.as_view(), name='venta_detail'),
    path('ventas/<int:pk>/editar/', user_views.UserVentaUpdateView.as_view(), name='venta_update'),
    path('ventas/<int:pk>/eliminar/', user_views.UserVentaDeleteView.as_view(), name='venta_delete'),
    
    # DetalleVenta URLs
    path('detalles-venta/', user_views.UserDetalleVentaListView.as_view(), name='detalleventa_list'),
    path('detalles-venta/nuevo/', user_views.UserDetalleVentaCreateView.as_view(), name='detalleventa_create'),
    path('detalles-venta/<int:pk>/', user_views.UserDetalleVentaDetailView.as_view(), name='detalleventa_detail'),
    path('detalles-venta/<int:pk>/editar/', user_views.UserDetalleVentaUpdateView.as_view(), name='detalleventa_update'),
    path('detalles-venta/<int:pk>/eliminar/', user_views.UserDetalleVentaDeleteView.as_view(), name='detalleventa_delete'),
    
    # MetodoPago URLs
    path('metodos-pago/', user_views.UserMetodoPagoListView.as_view(), name='metodopago_list'),
    path('metodos-pago/nuevo/', user_views.UserMetodoPagoCreateView.as_view(), name='metodopago_create'),
    path('metodos-pago/<int:pk>/', user_views.UserMetodoPagoDetailView.as_view(), name='metodopago_detail'),
    path('metodos-pago/<int:pk>/editar/', user_views.UserMetodoPagoUpdateView.as_view(), name='metodopago_update'),
    path('metodos-pago/<int:pk>/eliminar/', user_views.UserMetodoPagoDeleteView.as_view(), name='metodopago_delete'),
    
    # Pago URLs
    path('pagos/', user_views.UserPagoListView.as_view(), name='pago_list'),
    path('pagos/nuevo/', user_views.UserPagoCreateView.as_view(), name='pago_create'),
    path('pagos/<int:pk>/', user_views.UserPagoDetailView.as_view(), name='pago_detail'),
    path('pagos/<int:pk>/editar/', user_views.UserPagoUpdateView.as_view(), name='pago_update'),
    path('pagos/<int:pk>/eliminar/', user_views.UserPagoDeleteView.as_view(), name='pago_delete'),
    
    # Devolucion URLs
    path('devoluciones/', user_views.UserDevolucionListView.as_view(), name='devolucion_list'),
    path('devoluciones/nueva/', user_views.UserDevolucionCreateView.as_view(), name='devolucion_create'),
    path('devoluciones/<int:pk>/', user_views.UserDevolucionDetailView.as_view(), name='devolucion_detail'),
    path('devoluciones/<int:pk>/editar/', user_views.UserDevolucionUpdateView.as_view(), name='devolucion_update'),
    path('devoluciones/<int:pk>/eliminar/', user_views.UserDevolucionDeleteView.as_view(), name='devolucion_delete'),
    
    # Clientes Deudores y Pagos
    path('clientes/deudores/', login_required(views.ClientesDeudoresView.as_view()), name='clientes_deudores'),
    path('ventas/<int:venta_id>/registrar-pago/', login_required(views.RegistrarPagoView.as_view()), name='registrar_pago'),
    
    # PDF de remito
    path('ventas/<int:pk>/pdf/', login_required(views.VentaPDFView.as_view()), name='venta_pdf'),
    
    # Catálogo URLs (privadas, requieren autenticación)
    path('catalogos/', login_required(catalogo_views.CatalogoListView.as_view()), name='catalogo_list'),
    path('catalogos/nuevo/', login_required(catalogo_views.CatalogoCreateView.as_view()), name='catalogo_create'),
    path('catalogos/<int:pk>/', login_required(catalogo_views.CatalogoDetailView.as_view()), name='catalogo_detail'),
    path('catalogos/<int:pk>/editar/', login_required(catalogo_views.CatalogoUpdateView.as_view()), name='catalogo_update'),
    path('catalogos/<int:pk>/eliminar/', login_required(catalogo_views.CatalogoDeleteView.as_view()), name='catalogo_delete'),
    path('catalogos/<int:pk>/productos/', login_required(catalogo_views.ProductosCatalogoView.as_view()), name='productos_catalogo'),
    path('catalogos/<int:pk>/agregar-productos/', login_required(catalogo_views.AgregarProductosCatalogoView.as_view()), name='agregar_productos_catalogo'),
    
    # URL pública para ver catálogos (no requiere autenticación)
    path('c/<uuid:codigo>/', catalogo_views.CatalogoPublicoView.as_view(), name='catalogo_publico'),
]
