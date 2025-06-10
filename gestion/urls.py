from django.urls import path
from .views import GenerarBoleta, listar_productos, crear_producto, editar_producto, eliminar_producto, login_view, logout_view, generar_boleta_formulario

urlpatterns = [
    

    # Vista de la API (POST que procesa el formulario)
    path('generar-boleta/', GenerarBoleta.as_view(), name='generar_boleta'),
    path('consultar-boleta/<str:serie>/<int:numero>', GenerarBoleta.as_view(), name='consultar_boleta'),
    # Vista del formulario HTML
    path('generar-boleta-formulario/', generar_boleta_formulario, name='generar_boleta_formulario'),
    path('productos/', listar_productos, name='listar_productos'),
    path('productos/crear/', crear_producto, name='crear_producto'),
    path('productos/editar/<int:id>/', editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', eliminar_producto, name='eliminar_producto'),
    path("logout/", logout_view, name="logout"),
  
]
