from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from oferta.models import Oferta
from producto.models import Producto
from django.contrib.auth.hashers import make_password, check_password

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populating the database...'))

        User.objects.create(
            username='alejandro@gmail.com',
            email='alejandro@gmail.com',
            password = make_password('alejandropass123')
        )

        User.objects.create(
            username='daniel@gmail.com',
            email='daniel@gmail.com',
            password = make_password('danielpass123')
        )

        User.objects.create(
            username='rafael@gmail.com',
            email='rafael@gmail.com',
            password = make_password('rafaelpass123')
        )

        User.objects.create(
            username='juancarlos@gmail.com',
            email='juancarlos@gmail.com',
            password = make_password('juancarlospass123')
        )

        User.objects.create(
            username='maria@gmail.com',
            email='maria@gmail.com',
            password = make_password('mariapass123')
        )        

        Oferta.objects.create(
            porcentaje = 20,
        )

        Oferta.objects.create(
            porcentaje = 15,
        )

        Oferta.objects.create(
            porcentaje = 30,
        )


        Producto.objects.create(
            nombre = 'Benimar 340 UP',
            marca = 'Benimar',
            modelo = '340 UP',
            descripcion = 'Autocaravana muy amplia con cama doble atrás de fácil acceso y cama litera que se baja con motor eléctrico. Permite 5 plazas en marcha y dormir sin tener que desmontar salón, las camas siempre hechas. Dispone de un maletero gigante que es ampliable en altura moviendo la cama de abajo. Vehículo super cómodo de conducir con motor 155 CV y sólo 6,75 m de largo. Con todos los extras: portabicis, placa solar, crash sensor (para no tener que cerrar gas en marcha), sillas y mesa camping, menaje…',
            precio = 140,
            unidades = 0,
            imagen = 'https://mundovan.com/wp-content/uploads/2022/12/Foto-delantera-627x485.jpg',
            capacidad_viajar = 5,
            capacidad_dormir = 5,
            oferta = Oferta.objects.get(pk=1),
            categoria = 'integral'
        )

        Producto.objects.create(
            nombre = 'Giottiline Siena 385 Privilege',
            marca = 'Giottiline',
            modelo = 'Siena 385 Privilege',
            descripcion = 'La autocaravana perfilada Giottiline Siena 385 PRIVILEGE es un confortable modelo que te ofrece hasta 5 asientos para viajar y 5 plazas para dormir. En la parte posterior del habitáculo dispones de dos camas gemelas que se convierten en una gran cama de 2,10 m. Además, tienes otra cama doble eléctrica abatible de techo y salón convertible en una cama adicional. El equipamiento de esta autocaravana incluye también un cuarto de baño con WC y lavabo, ducha independiente, cocina completa con gran nevera, comedor de 5 plazas con mesa extensible y asientos de cabina giratorios, televisión, armarios roperos y otros espacios de almacenamiento. El garaje tiene doble portón y su altura interior es de 118 cm.',
            precio = 145,
            unidades = 7,
            imagen = 'https://mundovan.com/wp-content/uploads/2023/03/Autocaravana-de-alquiler-Giottiline-Siena-385-Privilege-627x485.jpg',
            capacidad_viajar = 6,
            capacidad_dormir = 4,
            oferta = Oferta.objects.get(pk=2),
            categoria = 'camper'
        )
            
        Producto.objects.create(
            nombre = 'Sunlight T65',
            marca = 'Sunlight',
            modelo = 'T65',
            descripcion = 'Autocaravana perfilada Sunlight modelo T65 año 2023 (grupo Hymer), sobre Fiat Ducato Multijet 3, 140cv. Confortable modelo que te ofrece hasta 5 plazas para dormir y para viajar y un equipamiento muy completo. Dispones de un dormitorio tipo suite con cama doble de 150×200 cm, cama basculante central de 150×200 cm y salón convertible en una cama de 90×210 cm. Cuarto de baño con plato de ducha independiente; cocina completa con gran nevera de 140 l y congelador; amplio salón de 5 plazas con asientos de cabina giratorios; armarios roperos, espacioso garaje con dos puertas de acceso (84×104 cm y 40×79 cm), escalón de entrada eléctrico, mosquiteras y oscurecedores en todas las ventanas, claraboyas y en puerta de entrada. Claraboya panorámica. Calefacción y agua caliente a gas Truma, tanques de agua potable y grises. Extenso equipamiento de serie: airbag para conductor y pasajero, HillHolder, ESP, ABS, ASR. Asientos giratorios “Captain Chair”, asientos conductor y acompañante regulables en altura, espejos eléctricos calefactables, ordenador de a bordo, cierre centralizado y elevalunas eléctricas, luz de día FIAT, iluminación interior de LED, Aire Acondicionado cabina, control de velocidad.',
            precio = 130,
            unidades = 3,
            imagen = 'https://mundovan.com/wp-content/uploads/2023/07/Autocaravana-alquiler-Sunlight-T65-627x485.jpg',
            capacidad_viajar = 5,
            capacidad_dormir = 4,
            oferta = Oferta.objects.get(pk=3),
            categoria = 'integral'
        )

        Producto.objects.create(
            nombre = 'Continental 840 XT',
            marca = 'Continental',
            modelo = '840 XT',
            descripcion = 'La autocaravana perfilada Continental 840 XT es un confortable modelo que te ofrece hasta 5 plazas para dormir y para viajar y un equipamiento muy completo. Libertad y autonomía, para que tus vacaciones sean las que siempre has soñado: Camas gemelas en la parte posterior, cama basculante en salón y salón convertible en cama individual. Cocina completa con nevera grande. Ducha independiente y baño completo. Garaje con doble puerta para poder viajar con tu bicicleta, moto o esquíes. Cómoda de conducir y muy sencilla de manejar. Su estudiado interior, práctico y acogedor, hará que disfrutes de cada momento.',
            precio = 150,
            unidades = 1,
            imagen = 'https://mundovan.com/wp-content/uploads/2023/04/Autocaravana-de-alquiler-Continental-840-XT.jpg',
            capacidad_viajar = 7,
            capacidad_dormir = 6,
            categoria = 'camper'
        )

        Producto.objects.create(
            nombre = 'Challenger C256',
            marca = 'Challenger',
            modelo = 'C256',
            descripcion = 'La autocaravana Challenger C256 es un confortable modelo que te ofrece hasta 5 plazas para dormir y para viajar y un equipamiento muy completo. Dispones de dos cama de 190cm x 90cm, cama central de 1,85 x1,35 m y  cama en capuchina de 2,00m x1,50 m Además, tienes un cuarto de baño con plato de ducha; cocina con nevera y congelador; salón de 7 plazas; televisión, armarios y toldo exterior.',
            precio = 135,
            unidades = 0,
            imagen = 'https://mundovan.com/wp-content/uploads/2023/07/image00002-627x485.jpeg',
            capacidad_viajar = 7,
            capacidad_dormir = 7,
            categoria = 'camper'
        )
        
        Producto.objects.create(
            nombre = 'Across 660',
            marca = 'Across',
            modelo = '660',
            descripcion = 'La autocaravana Across 660 es un confortable modelo que te ofrece hasta 6 plazas para dormir y para viajar y un equipamiento muy completo. Dispones de una cama de 150×195 cm, cama basculante central de 1,85 x1,40 m y dos camas en litera de 1,85 x1,40 m Además, tienes un cuarto de baño con plato de ducha; cocina con nevera y congelador; salón de 4 plazas; armarios',
            precio = 110,
            unidades = 8,
            imagen = 'https://mundovan.com/wp-content/uploads/2023/05/Autocaravana-de-alquiler-Across-660-627x485.jpg',
            capacidad_viajar = 7,
            capacidad_dormir = 5,
            categoria = 'perfilada'
        )

        Producto.objects.create(
            nombre = 'Benimar Sport 346 Alpha',
            marca = 'Benimar',
            modelo = 'Sport 346 Alpha',
            descripcion = 'La autocaravana Benimar Sport 346 Alpha es un confortable modelo que te ofrece hasta 5 plazas para dormir y para viajar y un equipamiento muy completo. Dispones de una cama de 135cmx195 cm, cama central de 1,85 x1,35 m y  cama en capuchina de 2,00m x1,50 m Además, tienes un cuarto de baño con plato de ducha; cocina con nevera y congelador; salón de 6 plazas; televisión, armarios y toldo exterior.',
            precio = 140,
            unidades = 5,
            imagen = 'https://mundovan.com/wp-content/uploads/2023/07/Autocaravana-alquiler-Benimar-Sport-346-Alpha-627x485.jpg',
            capacidad_viajar = 6,
            capacidad_dormir = 6,
            categoria = 'integral'
        )

        Producto.objects.create(
            nombre = 'Benimar Tessoro 442',
            marca = 'Benimar',
            modelo = 'Tessoro 442',
            descripcion = 'La autocaravana perfilada Benimar Tessoro 442 es un confortable modelo que te ofrece hasta 5 plazas para dormir y para viajar y un equipamiento muy completo. Dispones de un dormitorio con cama trasversal de 140×210 cm, cama basculante central de 140×191 cm y salón convertible en una cama de 135×200 cm. Además, tienes un cuarto de baño con plato de ducha independiente; cocina completa  con gran nevera de 140 l y congelador; amplio salón de 5 plazas con asientos de cabina giratorios; 2 televisiones, armarios roperos, espacioso garaje con altura regulable y toldo exterior.',
            precio = 125,
            unidades = 6,
            imagen = 'https://mundovan.com/wp-content/uploads/2023/03/3-3-627x485.jpg',
            capacidad_viajar = 6,
            capacidad_dormir = 5,
            categoria = 'capuchina'
        )

        Producto.objects.create(
            nombre = 'Continental 650 XT',
            marca = 'Continental',
            modelo = '650 XT',
            descripcion = 'La autocaravana perfilada Continental 650 XT es un confortable modelo que te ofrece hasta 5 plazas para dormir y para viajar y un equipamiento muy completo. Dispones de un dormitorio tipo suite con una cama en isla de 150×195 cm, cama basculante eléctrica central de 140×191 cm y salón convertible en otra cama de 90×210 cm. Aparte, esta autocaravana te ofrece un cuarto de aseo con plato de ducha independiente; cocina completa con gran nevera de 140 l y congelador; amplio salón de 5 plazas con asientos de cabina giratorios, armarios roperos, espacioso garaje con altura regulable y toldo exterior.',
            precio = 145,
            unidades = 9,
            imagen = 'https://mundovan.com/wp-content/uploads/2023/04/Continental-650-XT-627x485.jpg',
            capacidad_viajar = 5,
            capacidad_dormir = 5,
            categoria = 'integral'
        )

        Producto.objects.create(
            nombre = 'Elnagh Baron 573',
            marca = 'Elnagh',
            modelo = 'Baron 573',
            descripcion = 'La autocaravana perfilada Elnagh Baron 573 es un confortable modelo que te ofrece hasta 5 plazas para dormir y para viajar y un equipamiento muy completo. Dispone de un dormitorio con camas gemelas convertibles a cama de 240x200cm, cama basculante central automático 135×200 cm, con salón convertible en cama. Además, tienes un cuarto de baño con plato de ducha; cocina con nevera y congelador; salón de 5 plazas con asientos de cabina giratorios; televisión, armarios y toldo exterior.',
            precio = 130,
            unidades = 10,
            imagen = 'https://mundovan.com/wp-content/uploads/2023/05/Autocaravana-de-alquiler-Elnagh-Baron-573-627x485.jpg',
            capacidad_viajar = 5,
            capacidad_dormir = 5,
            categoria = 'integral'
        )

        Producto.objects.create(
            nombre = 'Etrusco 7300 DB',
            marca = 'Etrusco',
            modelo = '7300 DB',
            descripcion = 'La autocaravana capuchina Estrusco 7300DB es un confortable modelo que te ofrece hasta 6 plazas para dormir y para viajar y un equipamiento muy completo. Dispones de una cama doble transversal en la parte posterior de la autocaravana y una cama doble en la capuchina. Equipada con un comedor clásico, con el lavabo separado de la ducha. También dispone de un maletero inmenso que le facilitara poder llevar bicicletas, mesas o sillas de camping. Además, tienes un cuarto de baño con plato de ducha independiente; cocina completa  con gran nevera de 140 l y congelador; amplio salón de 6 plazas, Smart TV, armarios roperos, y toldo exterior.',
            precio = 140,
            unidades = 2,
            imagen = 'https://mundovan.com/wp-content/uploads/2023/03/Autocaravana-de-alquiler-Etrusco-7300-DB-627x485.jpg',
            capacidad_viajar = 6,
            capacidad_dormir = 6,
            categoria = 'capuchina'
        )

        Producto.objects.create(
            nombre = 'Etrusco I 7400 QB',
            marca = 'Etrusco',
            modelo = 'I 7400 QB',
            descripcion = 'La autocaravana integral ETRUSCO I7400QB es un confortable modelo que te ofrece hasta 4 plazas para dormir y para viajar y un equipamiento muy completo. Dispones de un dormitorio tipo suite con cama en isla de 135×180 cm pudiendo llegar a 200cm, cama basculante central de 135×180 cm. Además, tiene dividido el cuarto de baño y la ducha, están por separado con la comodidad que eso nos brinda. Dispone de cocina completa con gran nevera de 100 l y congelador; amplio salón de 5 plazas con asientos de cabina giratorios; 1 televisor, armarios roperos, espacioso garaje con altura de cama regulable, y toldo exterior.',
            precio = 135,
            unidades = 5,
            imagen = 'https://mundovan.com/wp-content/uploads/2023/02/Autocaravana-de-alquiler-Etrusco-I-7400-QB-627x485.jpeg',
            capacidad_viajar = 4,
            capacidad_dormir = 4,
            categoria = 'capuchina'
        )

        Producto.objects.create(
            nombre = 'Giottiline 330 Privilege',
            marca = 'Giottiline',
            modelo = '330 Privilege',
            descripcion = 'La autocaravana perfilada 330 es una autocaravana muy rutera, con tan sólo 5.99 m, tiene largo de camper, pero comodidad interior de autocaravana. Con distribución de cama francesa, y cama eléctrica en el salón y posibilidad de otra cama en la cabina. Además, tienes un cuarto de baño con plato de ducha; cocina con nevera y congelador; salón de 4 plazas con asientos de cabina giratorios; televisión, armarios.',
            precio = 145,
            unidades = 6,
            imagen = 'https://mundovan.com/wp-content/uploads/2023/10/Autocaravana-de-alquiler-Giottiline-330-Privilege-627x485.jpg',
            capacidad_viajar = 4,
            capacidad_dormir = 4,
            categoria = 'perfilada'
        )

        Producto.objects.create(
            nombre = 'Giottiline 385 Privilege',
            marca = 'Giottiline',
            modelo = '385 Privilege',
            descripcion = 'La autocaravana perfilada 385 es un confortable modelo que te ofrece hasta 5 plazas para dormir y viajar y un equipamiento muy completo. Dispones de camas gemelas, de multiples distribuciones, 2 de 80, cama King size 210*210  cm, etc, cama basculante central de 1,85 x1,40cm. Además, tienes un cuarto de baño con plato de ducha; cocina con nevera y congelador; salón de 5 plazas con asientos de cabina giratorios; televisión, armarios.',
            precio = 140,
            unidades = 3,
            imagen = 'https://mundovan.com/wp-content/uploads/2023/10/IMG20230706114851-627x485.jpg',
            capacidad_viajar = 5,
            capacidad_dormir = 5,
            categoria = 'capuchina'
        )

        Producto.objects.create(
            nombre = 'JOA CAMP J75T',
            marca = 'JOA CAMP',
            modelo = 'J75T',
            descripcion = 'La autocaravana JOA CAMP J75T es un confortable modelo que te ofrece hasta 5 plazas para dormir y viajar y un equipamiento muy completo. Dispones de una cama doble y 3 camas individuales. Además, tienes un cuarto de baño con plato de ducha; cocina con nevera y congelador; salón de 5 plazas con asientos de cabina giratorios; televisión, armarios y toldo exterior.',
            precio = 130,
            unidades = 1,
            imagen = 'https://mundovan.com/wp-content/uploads/2023/07/Autocaravana-de-alquiler-JOA-CAMP-J75T-627x485.jpeg',
            capacidad_viajar = 5,
            capacidad_dormir = 5,
            categoria = 'perfilada'
        )

        Producto.objects.create(
            nombre = 'JOA CAMP J70T',
            marca = 'JOA CAMP',
            modelo = 'J70T',
            descripcion = 'La autocaravana JOA CAMP J70T es un confortable modelo que te ofrece hasta 4 plazas para dormir viajar y un equipamiento muy completo. Dispones de una cama de 150×195 cm, y 2 individuales de 0,70m) Además, tienes un cuarto de baño con plato de ducha; cocina con nevera y congelador; salón de 4 plazas con asientos de cabina giratorios; televisión, armarios y toldo exterior.',
            precio = 120,
            unidades = 2,
            imagen = 'https://mundovan.com/wp-content/uploads/2023/07/Autocaravana-de-alquiler-JOA-CAMP-J70T-627x485.jpeg',
            capacidad_viajar = 4,
            capacidad_dormir = 4,
            categoria = 'perfilada'
        )

        Producto.objects.create(
            nombre = 'Mclouis Glamys 222',
            marca = 'Mclouis',
            modelo = 'Glamys 222',
            descripcion = 'Camila es una autocaravana de siete plazas, homologadas, versátil, funcional y con un diseño y confort excepcional. Perfecta para viajar y dormir hasta siete personas. El habitáculo de la casa está compuesto por dos salones, uno para 4 personas y otro para dos, zona de cocina con dos fuegos a gas, un fregadero, nevera, e incluye todo el menaje necesario. En la parte trasera se encuentran dos camas individuales transversales maximizando el espacio y una gran cama doble en la parte de capuchina. Tiene ducha interior con agua caliente separada del lavabo y wc. Incluido en el alquiler todo lo necesario para su funcionamiento: manguera, adaptadores de corriente, toldo, mesa y sillas de exterior.',
            precio = 135,
            unidades = 0,
            imagen = 'https://mundovan.com/wp-content/uploads/2023/03/Autocaravana-de-alquiler-Mclouis-Glamys-222-627x485.jpg',
            capacidad_viajar = 7,
            capacidad_dormir = 7,
            categoria = 'perfilada'
        )

        Producto.objects.create(
            nombre = 'Mclouis Glamys 322',
            marca = 'Mclouis',
            modelo = 'Glamys 322',
            descripcion = 'La autocaravana Mclouis Glamys 322 es un confortable modelo familiar que te ofrece hasta 7 plazas para viajar y para dormir y un equipamiento muy completo. Dispones de un dormitorio en capuchina con cama doble 150×220 cm, dos literas independientes de 90×210 cm, y 2 salones convertibles en una cama, uno de ellos hace una cama doble de 125×181 y el otro una cama individual de 67×149 para un niño. Además, tienes un cuarto de baño con WC, lavabo y plato de ducha con mampara; cocina completa con gran nevera de 175 l y congelador independiente; amplio salón de 6 plazas; televisión, numerosos armarios, ropero, espacioso garaje con doble puerta y litera plegable para poder aumentar su espacio.',
            precio = 120,
            unidades = 6,
            imagen = 'https://mundovan.com/wp-content/uploads/2023/02/Autocaravana-de-alquiler-Mclouis-Glamys-322-627x485.jpg',
            capacidad_viajar = 7,
            capacidad_dormir = 7,
            categoria = 'capuchina'
        )


        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))