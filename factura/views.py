import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from .models import Factura, Factura_productos_personalizado
from cesta.models import Pedido
from producto.models import Producto
from django.conf import settings
from django.core.mail import EmailMessage

def generar_factura(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    total_factura = pedido.precio

    nueva_factura = Factura.objects.create(pedido=pedido, total=total_factura)

    productos = json.loads(pedido.productos)

    for producto_info in productos:
        nombre_producto = producto_info['nombre']
        cantidad_pedido = producto_info['cantidad']

        producto_existente = Producto.objects.filter(nombre=nombre_producto).order_by("nombre").first()

        Factura_productos_personalizado.objects.create(factura=nueva_factura, producto=producto_existente, cantidad=cantidad_pedido)

    enviar_correo_factura(request, nueva_factura)

    return redirect('detalle_factura', factura_id=nueva_factura.id)

def detalle_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    return render(request, 'detalle_factura.html', {'factura': factura})

def generar_factura_pdf(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=factura_{factura.id}.pdf'

    p = canvas.Canvas(response, pagesize=letter)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "FACTURA")

    p.setFont("Helvetica", 12)
    p.drawString(100, 730, f"Pedido: {factura.pedido.id}")
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

def enviar_correo_factura(request, factura):
    pdf_response = generar_factura_pdf(request, factura.id)

    mensaje = "Adjunto encontrarás la factura correspondiente a tu pedido."

    pedido = factura.pedido

    email = EmailMessage(
        'Factura de tu pedido',
        mensaje,
        settings.DEFAULT_FROM_EMAIL,
        [pedido.email],
    )
    
    email.attach(f'factura_{factura.id}.pdf', pdf_response.content, 'application/pdf')
    email.send(fail_silently=False)