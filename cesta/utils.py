import json
from cesta.models import Carrito, Estado, Pedido


def create_pedido(request, datos_pedido, productos, estado=Estado.PENDIENTE):
    
    carrito = Carrito.objects.get(usuario=request.user)
    pedido = Pedido(
                    usuario=request.user,
                    telefono=datos_pedido.telefono,
                    direccion_envio=datos_pedido.direccion_envio,
                    direccion_facturacion=datos_pedido.direccion_facturacion,
                    instrucciones_entrega=datos_pedido.instrucciones_entrega,
                    email=datos_pedido.email,
                    first_name=datos_pedido.first_name,
                    last_name=datos_pedido.last_name,
                    forma_entrega=datos_pedido.forma_entrega,
                    forma_pago=datos_pedido.forma_pago,
                    productos=json.dumps(productos),
                    precio=carrito.calcular_total(),
                    estado=estado
                )

    pedido.save()


def get_productos_from_carrito(carrito):
    productos = []
    
    for item in carrito.items.all():
        producto_info = {
            'id': item.producto.id,
            'nombre': item.producto.nombre,
            'precio': float(item.producto.precio),  # Convertir Decimal a float
            'cantidad': item.cantidad,
            'subtotal': float(item.calcular_subtotal()),  # Convertir Decimal a float
        }
        productos.append(producto_info)
    
    return productos