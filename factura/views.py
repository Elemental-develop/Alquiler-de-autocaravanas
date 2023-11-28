import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from .models import Factura, Factura_productos_personalizado
from cesta.models import Pedido
from producto.models import Producto

@login_required
def generar_factura(request):
    carrito = Pedido.objects.filter(usuario=request.user).last()

    if carrito is None:
        messages.error(request, 'No se encontró un carrito para este usuario.')
        return redirect('some_redirect_url')

    total_factura = carrito.precio

    nueva_factura = Factura.objects.create(cliente=request.user, total=total_factura)

    productos = json.loads(carrito.productos)

    for producto_info in productos:
        nombre_producto = producto_info['nombre']
        cantidad_pedido = producto_info['cantidad']

        producto_existente = Producto.objects.get(nombre=nombre_producto)

        Factura_productos_personalizado.objects.create(factura=nueva_factura, producto=producto_existente, cantidad=cantidad_pedido)

    return redirect('detalle_factura', factura_id=nueva_factura.id)

@login_required
def detalle_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    return render(request, 'detalle_factura.html', {'factura': factura})

@login_required
def generar_factura_pdf(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=factura_{factura.id}.pdf'

    p = canvas.Canvas(response, pagesize=letter)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "FACTURA")

    p.setFont("Helvetica", 12)
    p.drawString(100, 730, f"Cliente: {factura.cliente.username}")
    p.drawString(100, 715, f"Fecha de Emisión: {factura.fecha_emision}")

    productos = Factura_productos_personalizado.objects.filter(factura=factura)
    col_widths = [300, 50, 50, 50]
    row_height = 20
    table_x = 100
    table_y = 680
    p.setFillColorRGB(0.2, 0.2, 0.2)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(table_x, table_y, "Descripción")
    p.drawString(table_x + col_widths[0], table_y, "Precio")
    p.drawString(table_x + col_widths[0] + col_widths[1], table_y, "Cantidad")
    p.drawString(table_x + col_widths[0] + col_widths[1] + col_widths[2], table_y, "Subtotal")
    p.setFillColorRGB(0, 0, 0)

    for i, producto in enumerate(productos):
        row_y = table_y - (i + 1) * row_height
        p.drawString(table_x, row_y, producto.producto.nombre)
        p.drawString(table_x + col_widths[0], row_y, f"${producto.producto.precio:.2f}")

        cantidad = producto.cantidad

        p.drawString(table_x + col_widths[0] + col_widths[1], row_y, str(cantidad))

        subtotal = producto.producto.precio * cantidad
        p.drawString(table_x + col_widths[0] + col_widths[1] + col_widths[2], row_y, f"${subtotal:.2f}")

    total = sum(producto.producto.precio * producto.cantidad for producto in productos)

    p.line(table_x, table_y - (len(productos) + 1) * row_height, table_x + sum(col_widths), table_y - (len(productos) + 1) * row_height)

    p.drawString(table_x + col_widths[0] + col_widths[1] + col_widths[2], table_y - (len(productos) + 2) * row_height, f"Total: ${total:.2f}")

    p.showPage()
    p.save()
    return response
