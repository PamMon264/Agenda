import pymongo

print("BIENVENIDO A LA AGENDA DE CONTACTOS DE PAM.")

class Persona:
    def __init__(self, nombre, apellido, fecha_nacimiento):
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'fecha_nacimiento': self.fecha_nacimiento
        }

class Direccion:
    def __init__(self, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia):
        self.calle = calle
        self.ciudad = ciudad
        self.codigo_postal = codigo_postal
        self.numero_exterior = numero_exterior
        self.numero_interior = numero_interior
        self.colonia = colonia

    def to_dict(self):
        return {
            'calle': self.calle,
            'ciudad': self.ciudad,
            'codigo_postal': self.codigo_postal,
            'numero_exterior': self.numero_exterior,
            'numero_interior': self.numero_interior,
            'colonia': self.colonia
        }

class Telefono:
    def __init__(self, numero):
        self.numero = numero

    def to_dict(self):
        return {'numero': self.numero}

class CorreoElectronico:
    def __init__(self, email, pagina_web):
        self.email = email
        self.pagina_web = pagina_web

    def to_dict(self):
        return {'email': self.email, 'pagina_web': self.pagina_web}

class Contacto(Persona, Direccion, Telefono, CorreoElectronico):
    def __init__(self, nombre, apellido, fecha_nacimiento, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia, numero, email, pagina_web):
        Persona.__init__(self, nombre, apellido, fecha_nacimiento)
        Direccion.__init__(self, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia)
        Telefono.__init__(self, numero)
        CorreoElectronico.__init__(self, email, pagina_web)

    def to_dict(self):
        contacto_dict = {}
        contacto_dict.update(Persona.to_dict(self))
        contacto_dict.update(Direccion.to_dict(self))
        contacto_dict.update(Telefono.to_dict(self))
        contacto_dict.update(CorreoElectronico.to_dict(self))
        return contacto_dict

class Agenda:
    def __init__(self):
        self.cliente = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.cliente["Agenda"]
        self.collection = self.db["contactos"]

    def agregar_contacto(self, contacto):
        self.collection.insert_one(contacto.to_dict())
        print("Contacto agregado exitosamente.")

    def visualizar_agenda(self):
        # Obtenemos todos los contactos ordenados por nombre
        contactos = self.collection.find().sort('nombre')

        # Convertimos el cursor a una lista para poder contar elementos
        contactos_lista = list(contactos)

        if len(contactos_lista) == 0:
            print("La agenda está vacía.")
        else:
            print("\nAgenda:")
            print("{:<5} {:<15} {:<15} {:<15} {:<20} {:<15}".format(
                "ID", "Nombre", "Apellido", "Fecha Nac.", "Teléfono", "Correo Electrónico"))
            print("-" * 85)

            for contacto in contactos_lista:
                print("{:<5} {:<15} {:<15} {:<15} {:<20} {:<15}".format(
                    str(contacto['_id']),
                    contacto['nombre'],
                    contacto['apellido'],
                    contacto['fecha_nacimiento'],
                    contacto['numero'],
                    contacto['email']
                ))
            print("-" * 85)

    def modificar_contacto(self):
        # Mostramos todos los contactos para que el usuario elija por el número de teléfono
        self.visualizar_agenda()
        numero_telefono = input("\nIngrese el número de teléfono del contacto que desea modificar: ")

        # Buscamos el contacto por número de teléfono
        query = {'numero': numero_telefono}
        contacto = self.collection.find_one(query)

        if contacto:
            # Mostramos las opciones de campos a modificar
            print("\nCampos disponibles para modificar:")
            print("1. Nombre")
            print("2. Apellido")
            print("3. Fecha de Nacimiento")
            print("4. Calle")
            print("5. Ciudad")
            print("6. Código Postal")
            print("7. Número Exterior")
            print("8. Número Interior")
            print("9. Colonia")
            print("10. Correo Electrónico")
            print("11. Página Web")

            opcion = input("Seleccione el número del campo que desea modificar: ")

            # Validamos la opción
            if opcion.isdigit() and 1 <= int(opcion) <= 11:
                campo = None
                nuevo_valor = input("Ingrese el nuevo valor: ")

                # Asignamos el campo correspondiente
                if opcion == "1":
                    campo = 'nombre'
                elif opcion == "2":
                    campo = 'apellido'
                elif opcion == "3":
                    campo = 'fecha_nacimiento'
                elif opcion == "4":
                    campo = 'calle'
                elif opcion == "5":
                    campo = 'ciudad'
                elif opcion == "6":
                    campo = 'codigo_postal'
                elif opcion == "7":
                    campo = 'numero_exterior'
                elif opcion == "8":
                    campo = 'numero_interior'
                elif opcion == "9":
                    campo = 'colonia'
                elif opcion == "10":
                    campo = 'email'
                elif opcion == "11":
                    campo = 'pagina_web'

                # Modificamos el contacto
                self.collection.update_one({'numero': numero_telefono}, {'$set': {campo: nuevo_valor}})
                print("Contacto modificado exitosamente.")

            else:
                print("Opción no válida.")

        else:
            print("No se encontró ningún contacto con ese número de teléfono.")

    def eliminar_contacto(self):
        # Mostramos todos los contactos para que el usuario elija por el número de teléfono
        self.visualizar_agenda()
        numero_telefono = input("\nIngrese el número de teléfono del contacto que desea eliminar: ")

        # Buscamos el contacto por número de teléfono
        query = {'numero': numero_telefono}
        contacto = self.collection.find_one(query)

        if contacto:
            # Confirmamos si el usuario realmente desea eliminar el contacto
            confirmacion = input(f"¿Está seguro de que desea eliminar a {contacto['nombre']} {contacto['apellido']}? (s/n): ")

            if confirmacion.lower() == 's':
                # Eliminamos el contacto
                self.collection.delete_one(query)
                print("Contacto eliminado exitosamente.")

        else:
            print("No se encontró ningún contacto con ese número de teléfono.")

# Ejemplo de uso interactivo
if __name__ == "__main__":
    agenda = Agenda()

    while True:
        print("\n1. Agregar contacto")
        print("2. Visualizar agenda")
        print("3. Modificar contacto")
        print("4. Eliminar contacto")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Validaciones de entrada al agregar contacto
            nombre = input("Nombre: ")
            while not nombre.isalpha():
                print("Por favor, ingrese solo letras para el nombre.")
                nombre = input("Nombre: ")

            apellido = input("Apellido: ")
            while not apellido.isalpha():
                print("Por favor, ingrese solo letras para el apellido.")
                apellido = input("Apellido: ")

            # Ingresar día, mes y año por separado para la fecha de nacimiento
            dia_nacimiento = input("Día de Nacimiento: ")
            mes_nacimiento = input("Mes de Nacimiento: ")
            anio_nacimiento = input("Año de Nacimiento: ")

            # Validar que la fecha de nacimiento sea válida
            while not (dia_nacimiento.isdigit() and mes_nacimiento.isdigit() and anio_nacimiento.isdigit() and 1 <= int(dia_nacimiento) <= 31 and 1 <= int(mes_nacimiento) <= 12):
                print("Por favor, ingrese una fecha de nacimiento válida.")
                dia_nacimiento = input("Día de Nacimiento: ")
                mes_nacimiento = input("Mes de Nacimiento: ")
                anio_nacimiento = input("Año de Nacimiento: ")

            fecha_nacimiento = f"{dia_nacimiento}/{mes_nacimiento}/{anio_nacimiento}"

            calle = input("Calle: ")
            while not calle.replace(" ", "").isalpha():
                print("Por favor, ingrese solo letras para el nombre de la calle.")
                calle = input("Calle: ")

            ciudad = input("Ciudad: ")
            while not ciudad.replace(" ", "").isalpha():
                print("Por favor, ingrese solo letras para el nombre de la ciudad.")
                ciudad = input("Ciudad: ")

            codigo_postal = input("Código Postal: ")

            # Validar que el código postal contenga solo números
            while not codigo_postal.isdigit():
                print("Por favor, ingrese solo números para el código postal.")
                codigo_postal = input("Código Postal: ")

            numero_exterior = input("Número Exterior: ")
            # Validar que el número exterior contenga solo números
            while not numero_exterior.isdigit():
                print("Por favor, ingrese solo números para el número exterior.")
                numero_exterior = input("Número Exterior: ")

            numero_interior = input("Número Interior: ")
            # Validar que el número interior contenga solo números
            while not numero_interior.isdigit():
                print("Por favor, ingrese solo números para el número interior.")
                numero_interior = input("Número Interior: ")

            colonia = input("Colonia: ")
            while not colonia.replace(" ", "").isalpha():
                print("Por favor, ingrese solo letras para el nombre de la colonia.")
                colonia = input("Colonia: ")

            numero_telefono = input("Número de Teléfono: ")
            # Validar que el número de teléfono contenga solo números y tenga longitud 10
            while not numero_telefono.isdigit() or len(numero_telefono) != 10:
                print("Por favor, ingrese un número de teléfono válido (10 dígitos).")
                numero_telefono = input("Número de Teléfono: ")

            email = input("Correo Electrónico: ")
            # Validar que el correo electrónico sea válido
            while "@" not in email or "." not in email:
                print("Por favor, ingrese un correo electrónico válido.")
                email = input("Correo Electrónico: ")

            pagina_web = input("Página Web (opcional): ")

            nuevo_contacto = Contacto(
                nombre,
                apellido,
                fecha_nacimiento,
                calle,
                ciudad,
                codigo_postal,
                numero_exterior,
                numero_interior,
                colonia,
                numero_telefono,
                email,
                pagina_web
            )
            agenda.agregar_contacto(nuevo_contacto)

        elif opcion == "2":
            agenda.visualizar_agenda()

        elif opcion == "3":
            agenda.modificar_contacto()

        elif opcion == "4":
            agenda.eliminar_contacto()

        elif opcion == "5":
            print("Saliendo del programa. ¡Hasta luego!")
            break

        else:
            print("Opción no válida. Inténtelo de nuevo.")
