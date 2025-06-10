from rest_framework.views import APIView

from rest_framework.request import Request
from rest_framework.response import Response
from datetime import datetime
import requests
from os import environ
from .serializers import GenerarBoletaSerializer
from .models import *

from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class GenerarBoleta(APIView):
    def post(self, request: Request):
        # Acceder a datos del formulario
        nombre_usuario = request.POST.get('nombre_usuario')
        documento_usuario = request.POST.get('documento_usuario')

        # Reconstruir lista de items desde POST
        items = []
        total_general = 0
        total_igv = 0

        i = 0
        while True:
            producto_id = request.POST.get(f'items[{i}][id]')
            cantidad = request.POST.get(f'items[{i}][cantidad]')
            if not producto_id or not cantidad:
                break
            cantidad = int(cantidad)

            producto_encontrado = Producto.objects.filter(id=producto_id).first()
            if not producto_encontrado:
                return Response(data={'message': f'Producto con id {producto_id} no existe'})

            base = producto_encontrado.precio / 1.18

            producto = {
                'unidad_de_medida': 'NIU',
                'codigo': producto_encontrado.id,
                'descripcion': producto_encontrado.nombre,
                'cantidad': cantidad,
                'valor_unitario': base,
                'precio_unitario': producto_encontrado.precio,
                'subtotal': base * cantidad,
                'tipo_de_igv': 1,
                'igv': (producto_encontrado.precio - base) * cantidad,
                'total': producto_encontrado.precio * cantidad,
                'anticipo_regularizacion': False,
            }

            total_general += producto_encontrado.precio * cantidad
            total_igv += (producto_encontrado.precio - base) * cantidad
            items.append(producto)
            i += 1

        # Armar data para NubeFact
        data = {
            'operacion': 'generar_comprobante',
            'tipo_de_comprobante': 2,
            'serie': 'BBB1',
            'numero': 1,
            'sunat_transaction': 1,
            'cliente_tipo_de_documento': 1,
            'cliente_numero_de_documento': documento_usuario,
            'cliente_denominacion': nombre_usuario,
            'fecha_de_emision': datetime.now().strftime('%d-%m-%Y'),
            'moneda': 1,
            'total_igv': total_igv,
            'total_gravada': total_general - total_igv,
            'porcentaje_de_igv': 18.00,
            'total': total_general,
            'items': items
        }

        # Enviar a NubeFact
        peticion = requests.post(
            url=environ.get('NUBEFACT_URL'),
            headers={'Authorization': 'Bearer ' + environ.get('NUBEFACT_TOKEN')},
            json=data
        )

        # Al final de la función post(...)
        resultado = peticion.json()

        # Verifica si hubo errores desde NubeFact
        if 'errors' in resultado:
            return render(request, 'productos/generar_boleta.html', {
                'productos': Producto.objects.all(),
                'error': resultado['errors']
            })

        # Mostrar plantilla con los detalles de la boleta
        return render(request, 'productos/boleta_exito.html', {
            'boleta': resultado
        })

@login_required
def generar_boleta_formulario(request):
    productos = Producto.objects.all()
    return render(request, 'productos/generar_boleta.html', {'productos': productos})

   

##listar mis productos
@login_required
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/listar.html', {'productos': productos})

@login_required
def crear_producto(request):
    form = ProductoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listar_productos')
    return render(request, 'productos/form.html', {'form': form, 'accion': 'Crear'})

@login_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, pk=id)
    form = ProductoForm(request.POST or None, instance=producto)
    if form.is_valid():
        form.save()
        return redirect('listar_productos')
    return render(request, 'productos/form.html', {'form': form, 'accion': 'Editar'})

@login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, pk=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')
    return render(request, 'productos/eliminar.html', {'producto': producto})

#crear login

def login_view(request):
    if request.method == "POST":
  
  
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("productos/listar.html")  
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
        return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")


