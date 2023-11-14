from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from producto.models import Producto

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populating the database...'))

        # Your code to populate the database goes here
        for i in range(10):
            User.objects.create(
                username=f'Usuario {i}',
                password=get_random_string(length=50)
            )

        for i in range(20):
            Producto.objects.create(
                nombre = f'Nombre {i}',
                marca = f'Marca {i}',
                modelo = f'Modelo {i}',
                descripcion = f'Descripción {i}',
                precio = i*1000+25*i,
                imagen = 'https://phantom-expansion.unidadeditorial.es/6ead8f7540efd52167440444bd610040/resize/828/f/jpg/assets/multimedia/imagenes/2023/01/10/16733818691897.jpg'
            )


        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))