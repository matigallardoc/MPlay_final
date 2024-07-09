import sqlite3
from django.contrib.auth.models import User, Permission
from django.db import connection
from datetime import date, timedelta
from random import randint
from core.models import Categoria, Producto, Carrito, Perfil, Boleta, DetalleBoleta, Bodega

def eliminar_tabla(nombre_tabla):
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute(f"DELETE FROM {nombre_tabla}")
    conexion.commit()
    conexion.close()

def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def crear_usuario(username, tipo, nombre, apellido, correo, es_superusuario, 
    es_staff, rut, direccion, subscrito, imagen):

    try:
        print(f'Verificar si existe usuario {username}.')

        if User.objects.filter(username=username).exists():
            print(f'   Eliminar {username}')
            User.objects.get(username=username).delete()
            print(f'   Eliminado {username}')
        
        print(f'Iniciando creación de usuario {username}.')

        usuario = None
        if tipo == 'Superusuario':
            print('    Crear Superuser')
            usuario = User.objects.create_superuser(username=username, password='123')
        else:
            print('    Crear User')
            usuario = User.objects.create_user(username=username, password='Duoc@123')

        if tipo == 'Administrador':
            print('    Es administrador')
            usuario.is_staff = es_staff
            
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.save()

        if tipo == 'Administrador':
            print(f'    Dar permisos a core y apirest')
            permisos = Permission.objects.filter(content_type__app_label__in=['core', 'apirest'])
            usuario.user_permissions.set(permisos)
            usuario.save()
 
        print(f'    Crear perfil: RUT {rut}, Subscrito {subscrito}, Imagen {imagen}')
        Perfil.objects.create(
            usuario=usuario, 
            tipo_usuario=tipo,
            rut=rut,
            direccion=direccion,
            subscrito=subscrito,
            imagen=imagen)
        print("    Creado correctamente")
    except Exception as err:
        print(f"    Error: {err}")

def eliminar_tablas():
    eliminar_tabla('auth_user_groups')
    eliminar_tabla('auth_user_user_permissions')
    eliminar_tabla('auth_group_permissions')
    eliminar_tabla('auth_group')
    eliminar_tabla('auth_permission')
    eliminar_tabla('django_admin_log')
    eliminar_tabla('django_content_type')
    #eliminar_tabla('django_migrations')
    eliminar_tabla('django_session')
    eliminar_tabla('Bodega')
    eliminar_tabla('DetalleBoleta')
    eliminar_tabla('Boleta')
    eliminar_tabla('Perfil')
    eliminar_tabla('Carrito')
    eliminar_tabla('Producto')
    eliminar_tabla('Categoria')
    #eliminar_tabla('authtoken_token')
    eliminar_tabla('auth_user')

def poblar_bd(test_user_email=''):
    eliminar_tablas()

    crear_usuario(
        username='lfernandez',
        tipo='Cliente', 
        nombre='Lucia', 
        apellido='Fernández', 
        correo='lfernandez@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='25.747.200-0',	
        direccion='123 Armijo, Isla de Maipo, \nIsla de Maipo 9790000 \nChile', 
        subscrito=True, 
        imagen='perfiles/lfernandez.webp')

    crear_usuario(
        username='mperez',
        tipo='Cliente', 
        nombre='Mateo', 
        apellido='Pérez', 
        correo='mperez@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='12.202.357-5', 
        direccion='234 Andres Bello, Santiago, \nSantiago 6513491 \nChile', 
        subscrito=True, 
        imagen='perfiles/mperez.png')

    crear_usuario(
        username='sgomez',
        tipo='Cliente', 
        nombre='Sofía', 
        apellido='Gómez', 
        correo='sgomez@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='11.991.600-3', 
        direccion='234 21 de Mayo, \nPomaire 9580280 \nChile', 
        subscrito=False, 
        imagen='perfiles/sgomez.png')

    crear_usuario(
        username='vramirez',
        tipo='Cliente', 
        nombre='Valentina', 
        apellido='Ramírez', 
        correo='vramirez@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='16.469.725-8', 
        direccion='2356 Federico Scotto, \nEstación Central 1080000 \nChile', 
        subscrito=False, 
        imagen='perfiles/vramirez.webp')

    crear_usuario(
        username='trodriguez',
        tipo='Administrador', 
        nombre='Tomás', 
        apellido='Rodríguez', 
        correo='trodriguez@gmail.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='19.441.980-5', 
        direccion='345 Los lirios, Isla de Maipo, \nIsla de Maipo 9790000 \nChile', 
        subscrito=False, 
        imagen='perfiles/trodriguez.jpeg')
    
    crear_usuario(
        username='dsanchez',
        tipo='Administrador', 
        nombre='Diego', 
        apellido='Sánchez', 
        correo='dsanchez@gmail.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='21.708.052-5', 
        direccion='2345 Lautaro, \nEstación Central 1080000  \nChile', 
        subscrito=False, 
        imagen='perfiles/dsanchez.jpeg')

    crear_usuario(
        username='super',
        tipo='Superusuario',
        nombre='Emilio',
        apellido='Torres',
        correo='super.etorres@gmail.com',
        es_superusuario=True,
        es_staff=True,
        rut='13.029.317-4',
        direccion='3186 Camino del Maillin, Lo Barnechea, \n Santiago 7590932 \nChile',
        subscrito=False,
        imagen='perfiles/super.webp')
    
    categorias_data = [
        { 'id': 1, 'nombre': 'Acción'},
        { 'id': 2, 'nombre': 'Aventura'},
        { 'id': 3, 'nombre': 'Estrategia'},
        { 'id': 4, 'nombre': 'RPG'},
    ]

    print('Crear categorías')
    for categoria in categorias_data:
        Categoria.objects.create(**categoria)
    print('Categorías creadas correctamente')

    productos_data = [
        # Categoría "Acción" (8 juegos)
        {
            'id': 1,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Ark: Survival Ascended',
            'descripcion': 'Ark: Survival Evolved es un juego de supervivencia y aventura desarrollado por Studio Wildcard. Ambientado en un mundo abierto prehistórico, los jugadores cazan, recolectan recursos, construyen refugios y domestican dinosaurios y otras criaturas. Ofrece modos de juego para un jugador y multijugador, con énfasis en la exploración, combate y entornos dinámicos.',
            'precio': 29990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/1.jpg'
        },
        {
            'id': 2,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Red Dead Redemption 2',
            'descripcion': 'Red Dead Redemption 2 es una épica historia sobre la vida en el despiadado corazón de América. Su vasto y evocador mundo también será la base para una nueva experiencia multijugador online, ofreciendo a los jugadores la oportunidad de explorar y vivir en este entorno dinámico y lleno de detalles.',
            'precio': 20000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/2.jpg'
        },
        {
            'id': 3,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Zelda: Breath of the Wild',
            'descripcion': 'The Legend of Zelda: Breath of the Wild es un juego de acción-aventura de 2017 de Nintendo, conocido por su mundo abierto y no lineal. Los jugadores controlan a Link en un mundo postapocalíptico, enfrentándose a Ganon. Recibió elogios por su innovación y fue premiado como juego del año.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/3.jpeg'
        },
        {
            'id': 4,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'God of War Ragnarök',
            'descripcion': 'Únete a Kratos y Atreus en un viaje mítico por los Nueve Reinos mientras se preparan para la profetizada batalla que acabará con el mundo. En God of War Ragnarök, explorarás paisajes impresionantes y te enfrentarás a temibles enemigos, tanto dioses como monstruos, mientras buscas respuestas y aliados antes de que llegue el Ragnarök.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/4.png'
        },
        {
            'id': 5,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'EA sports FC24',
            'descripcion': 'FIFA es una serie de videojuegos de simulación de fútbol desarrollada por EA Sports. Con actualizaciones anuales, permite a los jugadores controlar equipos y competir en ligas y torneos internacionales, destacando por su realismo, gráficos avanzados, y modos de juego tanto para un jugador como multijugador en línea.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/5.webp'
        },
        {
            'id': 6,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'NBA 24',
            'descripcion': 'NBA 2K es una franquicia de videojuegos de simulación de baloncesto desarrollada por Visual Concepts y publicada por 2K Sports. Con lanzamientos anuales, ofrece realismo gráfico y jugabilidad, permitiendo a los jugadores competir con equipos y estrellas de la NBA en modos de juego variados, incluyendo multijugador online.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/6.jpeg'
        },
        {
            'id': 7,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Horizon Forbidden West',
            'descripcion': 'Horizon Forbidden West es la secuela de Horizon Zero Dawn. El juego sigue a Aloy, una joven cazadora en un mundo postapocalíptico gobernado por máquinas. En Forbidden West, Aloy debe viajar a una nueva y peligrosa frontera para investigar una misteriosa plaga que está matando la vida vegetal y animal.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/8.jpg'
        },
        {
            'id': 8,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Gran turismo 7',
            'descripcion': 'Gran Turismo es una icónica serie de simulación de carreras desarrollada por Polyphony Digital y publicada por Sony Interactive Entertainment. Reconocida por su realismo, ofrece una amplia selección de coches y pistas, modos de carrera detallados y gráficos impresionantes, atrayendo a jugadores por su autenticidad y experiencia de conducción inmersiva.',
            'precio': 49990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/7.jpg'
        },
        # Categoría "Aventura" (4 juegos)
        {
            'id': 9,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'UNCHARTED 4',
            'descripcion': 'Uncharted es una serie de juegos de acción y aventuras desarrollada por Naughty Dog y publicada por Sony Interactive Entertainment. Protagonizada por Nathan Drake, combina exploración, plataformas y combate en escenarios exóticos y emocionantes. Reconocida por su narrativa cinematográfica, personajes carismáticos y secuencias de acción espectaculares.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/9.jpeg'
        },
        {
            'id': 10,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'FARCRY 6',
            'descripcion': 'Far Cry 6 es un juego de acción y aventura desarrollado por Ubisoft. Ambientado en un entorno ficticio inspirado en Cuba, los jugadores enfrentan un régimen dictatorial mientras exploran un mundo abierto lleno de conflictos y posibilidades. Destaca por su narrativa intensa, mecánicas de juego variadas y entornos detallados y dinámicos.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/10.jpg'
        },
        {
            'id': 11,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'UFC 5',
            'descripcion': 'UFC 5 es un juego de simulación de artes marciales mixtas desarrollado por EA Sports. Permite a los jugadores controlar a peleadores famosos de UFC, ofreciendo combates realistas y emocionantes en distintos modos de juego, incluyendo competiciones en línea. Destaca por su atención al detalle en movimientos y estrategias de combate.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/11.jpg'
        },
        {
            'id': 12,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'TOM CLANCYS THE DIVISION',
            'descripcion': 'Tom Clancys The Division es un juego de disparos táctico en línea desarrollado por Ubisoft Massive. Ambientado en un Nueva York devastado por una pandemia, los jugadores forman parte de una unidad especial para restaurar el orden. Destaca por su jugabilidad cooperativa, elementos RPG y un mundo abierto detallado y dinámico.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/12.jpg'
        },
        # Categoría "Estrategia" (4 juegos)
        {
            'id': 13,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'GTA V',
            'descripcion': 'Grand Theft Auto V (GTA V) es un juego de acción y aventura desarrollado por Rockstar North. Ambientado en la ficticia ciudad de Los Santos, ofrece una experiencia de mundo abierto donde los jugadores pueden explorar, realizar misiones y participar en actividades como robos y carreras. Reconocido por su narrativa compleja, personajes memorables y vasta variedad de opciones de juego.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/13.jpg'
        },
        {
            'id': 14,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Mortal kombat 1',
            'descripcion': 'Mortal Kombat es una icónica serie de juegos de lucha desarrollada por NetherRealm Studios. Conocida por su violencia gráfica y combate visceral, los jugadores controlan personajes con habilidades únicas en peleas uno contra uno. La serie se destaca por sus fatalities elaborados, historia intrigante y competitividad en torneos.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/14.jpeg'
        },
        {
            'id': 15,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Crash Bandicoot 4: Its About Time',
            'descripcion': 'Crash Bandicoot es una serie de juegos de plataformas desarrollada originalmente por Naughty Dog y ahora por otros estudios. Conocido por su protagonista, Crash, un marsupial que debe enfrentarse a enemigos y superar obstáculos en niveles coloridos y variados. La serie es famosa por su jugabilidad clásica, desafíos de saltos precisos y personajes carismáticos.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/15.jpg'
        },
        {
            'id': 16,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Dragon ball xenoverse 2',
            'descripcion': 'Dragon Ball Xenoverse 2 es un juego de acción y lucha basado en el universo Dragon Ball, desarrollado por Dimps y publicado por Bandai Namco Entertainment. Permite a los jugadores crear un personaje personalizado y explorar diferentes líneas temporales, participando en batallas épicas con personajes icónicos de la serie. Ofrece un extenso contenido multijugador y actualizaciones regulares para mantener la experiencia fresca.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/16.jpeg'
        },
        # Categoría "RPG" (4 juegos)
        {
            'id': 17,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Spider-Man 2',
            'descripcion': 'Spider-Man 2 es un juego de acción y aventura basado en el icónico superhéroe de Marvel, desarrollado por Insomniac Games y publicado por Sony Interactive Entertainment. Los jugadores controlan a Spider-Man en un mundo abierto de Nueva York, combinando combate fluido, acrobacias espectaculares y una narrativa emocionante. Se destaca por su fidelidad al personaje y mecánicas innovadoras de juego.',
            'precio': 29990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/17.jpg'
        },
        {
            'id': 18,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'The Last of Us Parte 2',
            'descripcion': 'The Last of Us Parte 2 es un juego de acción y supervivencia desarrollado por Naughty Dog y publicado por Sony Interactive Entertainment. Continúa la historia de Ellie en un mundo postapocalíptico, explorando temas de venganza y moralidad en un entorno devastador. Destaca por su narrativa emotiva, gráficos impresionantes y mecánicas de juego mejoradas.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/18.jpg'
        },
        {
            'id': 19,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Shandow of the Colossus',
            'descripcion': 'Shadow of the Colossus es un juego de acción y aventura desarrollado por Team Ico y publicado por Sony Computer Entertainment. Los jugadores asumen el papel de Wander, quien debe derrotar a colosos imponentes en un mundo vasto y misterioso para salvar a una joven. Destaca por su atmósfera única, diseño artístico impresionante y emocionantes batallas contra criaturas gigantescas.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/19.jpg'
        },
        {
            'id': 20,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'The Sims 4',
            'descripcion': 'The Sims 4 es un juego de simulación de vida desarrollado por Maxis y publicado por Electronic Arts. Permite a los jugadores crear y controlar personajes virtuales llamados Sims, gestionando sus vidas diarias, relaciones, carreras y actividades. Destaca por su libertad creativa, personalización profunda y expansión constante con packs de contenido adicionales.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/20.jpg'
        }
    ]

    print('Crear productos')
    for producto in productos_data:
        Producto.objects.create(**producto)
    print('Productos creados correctamente')

    print('Crear carritos')
    for rut in ['25.747.200-0', '11.991.600-3']:
        cliente = Perfil.objects.get(rut=rut)
        for cantidad_productos in range(1, 11):
            producto = Producto.objects.get(pk=randint(1, 10))
            if cliente.subscrito:
                descuento_subscriptor = producto.descuento_subscriptor
            else:
                descuento_subscriptor = 0
            descuento_oferta = producto.descuento_oferta
            descuento_total = descuento_subscriptor + descuento_oferta
            descuentos = int(round(producto.precio * descuento_total / 100))
            precio_a_pagar = producto.precio - descuentos
            Carrito.objects.create(
                cliente=cliente,
                producto=producto,
                precio=producto.precio,
                descuento_subscriptor=descuento_subscriptor,
                descuento_oferta=descuento_oferta,
                descuento_total=descuento_total,
                descuentos=descuentos,
                precio_a_pagar=precio_a_pagar
            )
    print('Carritos creados correctamente')

    print('Crear boletas')
    nro_boleta = 0
    perfiles_cliente = Perfil.objects.filter(tipo_usuario='Cliente')
    for cliente in perfiles_cliente:
        estado_index = -1
        for cant_boletas in range(1, randint(6, 21)):
            nro_boleta += 1
            estado_index += 1
            if estado_index > 3:
                estado_index = 0
            estado = Boleta.ESTADO_CHOICES[estado_index][1]
            fecha_venta = date(2023, randint(1, 5), randint(1, 28))
            fecha_despacho = fecha_venta + timedelta(days=randint(0, 3))
            fecha_entrega = fecha_despacho + timedelta(days=randint(0, 3))
            if estado == 'Anulado':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Vendido':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Despachado':
                fecha_entrega = None
            boleta = Boleta.objects.create(
                nro_boleta=nro_boleta, 
                cliente=cliente,
                monto_sin_iva=0,
                iva=0,
                total_a_pagar=0,
                fecha_venta=fecha_venta,
                fecha_despacho=fecha_despacho,
                fecha_entrega=fecha_entrega,
                estado=estado)
            detalle_boleta = []
            total_a_pagar = 0
            for cant_productos in range(1, randint(4, 6)):
                producto_id = randint(1, 10)
                producto = Producto.objects.get(id=producto_id)
                precio = producto.precio
                descuento_subscriptor = 0
                if cliente.subscrito:
                    descuento_subscriptor = producto.descuento_subscriptor
                descuento_oferta = producto.descuento_oferta
                descuento_total = descuento_subscriptor + descuento_oferta
                descuentos = int(round(precio * descuento_total / 100))
                precio_a_pagar = precio - descuentos
                bodega = Bodega.objects.create(producto=producto)
                DetalleBoleta.objects.create(
                    boleta=boleta,
                    bodega=bodega,
                    precio=precio,
                    descuento_subscriptor=descuento_subscriptor,
                    descuento_oferta=descuento_oferta,
                    descuento_total=descuento_total,
                    descuentos=descuentos,
                    precio_a_pagar=precio_a_pagar)
                total_a_pagar += precio_a_pagar
            monto_sin_iva = int(round(total_a_pagar / 1.19))
            iva = total_a_pagar - monto_sin_iva
            boleta.monto_sin_iva = monto_sin_iva
            boleta.iva = iva
            boleta.total_a_pagar = total_a_pagar
            boleta.fecha_venta = fecha_venta
            boleta.fecha_despacho = fecha_despacho
            boleta.fecha_entrega = fecha_entrega
            boleta.estado = estado
            boleta.save()
            print(f'    Creada boleta Nro={nro_boleta} Cliente={cliente.usuario.first_name} {cliente.usuario.last_name}')
    print('Boletas creadas correctamente')

    print('Agregar productos a bodega')
    for producto_id in range(1, 11):
        producto = Producto.objects.get(id=producto_id)
        cantidad = 0
        for cantidad in range(1, randint(2, 31)):
            Bodega.objects.create(producto=producto)
        print(f'    Agregados {cantidad} "{producto.nombre}" a la bodega')
    print('Productos agregados a bodega')

