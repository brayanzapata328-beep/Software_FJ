
from modelos.cliente import Cliente
from servicios.servicio_sala import ServicioSala
from servicios.servicio_equipo import ServicioEquipo
from servicios.servicio_asesoria import ServicioAsesoria

from controladores.gestor_clientes import GestorClientes
from controladores.gestor_servicios import GestorServicios
from controladores.gestor_reservas import GestorReservas

from registros.registro_logs import registrar_evento, registrar_error


def leer_texto(mensaje):
    """Solicita un texto obligatorio."""
    while True:
        valor = input(mensaje).strip()

        if valor:
            return valor

        print("El campo no puede estar vacío.")


def leer_entero(mensaje, minimo=1):
    """Solicita un número entero dentro del rango permitido."""
    while True:
        try:
            valor = int(input(mensaje))

            if valor < minimo:
                print(f"El valor debe ser igual o superior a {minimo}.")
                continue

            return valor

        except ValueError:
            print("Ingresa un número entero válido.")


def leer_decimal(mensaje, minimo=0):
    """Solicita un número decimal."""
    while True:
        try:
            valor = float(input(mensaje).replace(",", "."))

            if valor < minimo:
                print(f"El valor debe ser igual o superior a {minimo}.")
                continue

            return valor

        except ValueError:
            print("Ingresa un número válido.")


def leer_opcion(mensaje, opciones):
    """Solicita una opción perteneciente a una lista."""
    while True:
        opcion = input(mensaje).strip()

        if opcion in opciones:
            return opcion

        print("Opción no válida.")


class MenuSoftwareFJ:
    """Interfaz de consola para administrar Software FJ."""

    def __init__(self):
        self.gestor_clientes = GestorClientes()
        self.gestor_servicios = GestorServicios()

        self.gestor_reservas = GestorReservas(
            self.gestor_clientes,
            self.gestor_servicios
        )

    def mostrar_menu_principal(self):
        print("\n========================================")
        print("       SOFTWARE FJ")
        print(" Sistema Integral de Gestión")
        print("========================================")
        print("1. Gestión de clientes")
        print("2. Gestión de servicios")
        print("3. Gestión de reservas")
        print("4. Consultar resumen del sistema")
        print("0. Salir")
        print("========================================")

    def ejecutar(self):
        registrar_evento("Inicio de Software FJ")

        while True:
            try:
                self.mostrar_menu_principal()
                opcion = input("Selecciona una opción: ").strip()

                if opcion == "1":
                    self.menu_clientes()

                elif opcion == "2":
                    self.menu_servicios()

                elif opcion == "3":
                    self.menu_reservas()

                elif opcion == "4":
                    self.mostrar_resumen()

                elif opcion == "0":
                    print("\nGracias por utilizar Software FJ.")
                    registrar_evento("Cierre de Software FJ")
                    break

                else:
                    print("Selecciona una opción válida.")

            except KeyboardInterrupt:
                print("\nOperación interrumpida por el usuario.")
                registrar_evento("Interrupción manual del sistema")
                break

            except Exception as error:
                registrar_error("Error no controlado en el menú principal", error)
                print(f"Se produjo un error: {error}")
                print("El sistema continuará funcionando.")

    # ==========================================
    # GESTIÓN DE CLIENTES
    # ==========================================

    def menu_clientes(self):
        while True:
            print("\n----------- CLIENTES -----------")
            print("1. Registrar cliente")
            print("2. Buscar cliente por documento")
            print("3. Listar clientes")
            print("4. Eliminar cliente")
            print("0. Volver")

            opcion = input("Selecciona una opción: ").strip()

            try:
                if opcion == "1":
                    self.registrar_cliente()

                elif opcion == "2":
                    self.buscar_cliente()

                elif opcion == "3":
                    self.listar_clientes()

                elif opcion == "4":
                    self.eliminar_cliente()

                elif opcion == "0":
                    break

                else:
                    print("Opción no válida.")

            except Exception as error:
                registrar_error("Error en el módulo de clientes", error)
                print(f"No se pudo completar la operación: {error}")

    def registrar_cliente(self):
        print("\nREGISTRO DE CLIENTE")

        nombre = leer_texto("Nombre completo: ")
        documento = leer_texto("Documento: ")
        correo = leer_texto("Correo electrónico: ")
        telefono = leer_texto("Teléfono: ")

        cliente = Cliente(nombre, documento, correo, telefono)

        self.gestor_clientes.registrar_cliente(cliente)

        print("Cliente registrado correctamente.")

    def buscar_cliente(self):
        documento = leer_texto("Documento del cliente: ")

        cliente = self.gestor_clientes.buscar_por_documento(documento)

        print("\nCLIENTE ENCONTRADO")
        print(f"Nombre: {cliente.nombre}")
        print(f"Documento: {cliente.documento}")
        print(f"Correo: {cliente.correo}")
        print(f"Teléfono: {cliente.telefono}")
        print(f"ID: {cliente.id}")

    def listar_clientes(self):
        clientes = self.gestor_clientes.listar_clientes()

        if not clientes:
            print("No hay clientes registrados.")
            return

        print("\nLISTADO DE CLIENTES")

        for cliente in clientes:
            print(
                f"Nombre: {cliente.nombre} | "
                f"Documento: {cliente.documento} | "
                f"ID: {cliente.id}"
            )

    def eliminar_cliente(self):
        documento = leer_texto("Documento del cliente que deseas eliminar: ")

        cliente = self.gestor_clientes.buscar_por_documento(documento)

        confirmacion = leer_opcion(
            f"¿Eliminar a {cliente.nombre}? (s/n): ",
            ["s", "n"]
        )

        if confirmacion == "s":
            self.gestor_clientes.eliminar_cliente(documento)
            print("Cliente eliminado correctamente.")
        else:
            print("Operación cancelada.")

    # ==========================================
    # GESTIÓN DE SERVICIOS
    # ==========================================

    def menu_servicios(self):
        while True:
            print("\n----------- SERVICIOS -----------")
            print("1. Registrar servicio")
            print("2. Listar servicios")
            print("3. Consultar servicio por ID")
            print("4. Cambiar disponibilidad")
            print("5. Eliminar servicio")
            print("0. Volver")

            opcion = input("Selecciona una opción: ").strip()

            try:
                if opcion == "1":
                    self.registrar_servicio()

                elif opcion == "2":
                    self.listar_servicios()

                elif opcion == "3":
                    self.buscar_servicio()

                elif opcion == "4":
                    self.cambiar_disponibilidad()

                elif opcion == "5":
                    self.eliminar_servicio()

                elif opcion == "0":
                    break

                else:
                    print("Opción no válida.")

            except Exception as error:
                registrar_error("Error en el módulo de servicios", error)
                print(f"No se pudo completar la operación: {error}")

    def registrar_servicio(self):
        print("\nTIPOS DE SERVICIO")
        print("1. Servicio de sala")
        print("2. Alquiler de equipo")
        print("3. Asesoría especializada")

        tipo = leer_opcion("Selecciona el tipo: ", ["1", "2", "3"])

        nombre = leer_texto("Nombre del servicio: ")
        descripcion = leer_texto("Descripción: ")
        precio = leer_decimal("Precio base: ", 0)

        if tipo == "1":
            capacidad = leer_entero("Capacidad de personas: ")
            equipamiento = leer_texto("Equipamiento disponible: ")

            servicio = ServicioSala(
                nombre,
                descripcion,
                precio,
                capacidad,
                equipamiento
            )

        elif tipo == "2":
            tipo_equipo = leer_texto("Tipo de equipo: ")
            unidades = leer_entero("Unidades disponibles: ")
            estado = leer_texto("Estado del equipo: ")

            servicio = ServicioEquipo(
                nombre,
                descripcion,
                precio,
                tipo_equipo,
                unidades,
                estado
            )

        else:
            especialidad = leer_texto("Especialidad: ")
            profesional = leer_texto("Profesional responsable: ")
            modalidad = leer_texto("Modalidad: ")

            servicio = ServicioAsesoria(
                nombre,
                descripcion,
                precio,
                especialidad,
                profesional,
                modalidad
            )

        self.gestor_servicios.registrar_servicio(servicio)

        print("\nServicio registrado correctamente.")
        print(f"Identificador: {servicio.id}")

    def listar_servicios(self):
        servicios = self.gestor_servicios.listar_servicios()

        if not servicios:
            print("No hay servicios registrados.")
            return

        print("\nLISTADO DE SERVICIOS")

        for servicio in servicios:
            print("----------------------------------------")
            print(f"Nombre: {servicio.nombre}")
            print(f"Descripción: {servicio.descripcion}")
            print(f"Precio base: {servicio.precio_base}")
            print(f"Disponible: {servicio.disponible}")
            print(f"Tipo: {servicio.__class__.__name__}")
            print(f"ID: {servicio.id}")

    def buscar_servicio(self):
        identificador = leer_texto("ID del servicio: ")

        servicio = self.gestor_servicios.buscar_por_id(identificador)

        print("\nSERVICIO ENCONTRADO")
        print(servicio.describir())
        print(f"Precio base: {servicio.precio_base}")
        print(f"Disponible: {servicio.disponible}")
        print(f"ID: {servicio.id}")

    def cambiar_disponibilidad(self):
        identificador = leer_texto("ID del servicio: ")

        servicio = self.gestor_servicios.buscar_por_id(identificador)

        nueva_disponibilidad = not servicio.disponible

        self.gestor_servicios.cambiar_disponibilidad(
            identificador,
            nueva_disponibilidad
        )

        print(
            "Servicio ahora disponible."
            if nueva_disponibilidad
            else "Servicio ahora no disponible."
        )

    def eliminar_servicio(self):
        identificador = leer_texto("ID del servicio que deseas eliminar: ")

        servicio = self.gestor_servicios.buscar_por_id(identificador)

        confirmacion = leer_opcion(
            f"¿Eliminar {servicio.nombre}? (s/n): ",
            ["s", "n"]
        )

        if confirmacion == "s":
            self.gestor_servicios.eliminar_servicio(identificador)
            print("Servicio eliminado correctamente.")
        else:
            print("Operación cancelada.")

    # ==========================================
    # GESTIÓN DE RESERVAS
    # ==========================================

    def menu_reservas(self):
        while True:
            print("\n----------- RESERVAS -----------")
            print("1. Crear reserva")
            print("2. Listar reservas")
            print("3. Buscar reserva por ID")
            print("4. Confirmar reserva")
            print("5. Cancelar reserva")
            print("6. Completar reserva")
            print("0. Volver")

            opcion = input("Selecciona una opción: ").strip()

            try:
                if opcion == "1":
                    self.crear_reserva()

                elif opcion == "2":
                    self.listar_reservas()

                elif opcion == "3":
                    self.buscar_reserva()

                elif opcion == "4":
                    self.confirmar_reserva()

                elif opcion == "5":
                    self.cancelar_reserva()

                elif opcion == "6":
                    self.completar_reserva()

                elif opcion == "0":
                    break

                else:
                    print("Opción no válida.")

            except Exception as error:
                registrar_error("Error en el módulo de reservas", error)
                print(f"No se pudo completar la operación: {error}")

    def crear_reserva(self):
        print("\nCREAR RESERVA")

        documento = leer_texto("Documento del cliente: ")
        identificador = leer_texto("ID del servicio: ")
        duracion = leer_decimal("Duración o cantidad de horas: ")

        servicio = self.gestor_servicios.buscar_por_id(identificador)

        unidades = 1

        if isinstance(servicio, ServicioEquipo):
            unidades = leer_entero("Cantidad de unidades de equipo: ")

        reserva = self.gestor_reservas.crear_reserva(
            documento,
            identificador,
            duracion,
            unidades
        )

        print("\nReserva creada correctamente.")
        print(f"Identificador de reserva: {reserva.id}")
        print(f"Estado: {reserva.estado}")

    def listar_reservas(self):
        reservas = self.gestor_reservas.listar_reservas()

        if not reservas:
            print("No hay reservas registradas.")
            return

        print("\nLISTADO DE RESERVAS")

        for reserva in reservas:
            print("----------------------------------------")
            print(f"ID: {reserva.id}")
            print(f"Cliente: {reserva.cliente.nombre}")
            print(f"Servicio: {reserva.servicio.nombre}")
            print(f"Duración: {reserva.duracion}")
            print(f"Estado: {reserva.estado}")
            print(f"Costo: {reserva.costo_total}")

    def buscar_reserva(self):
        identificador = leer_texto("ID de la reserva: ")

        reserva = self.gestor_reservas.buscar_por_id(identificador)

        print("\nRESERVA ENCONTRADA")
        print(f"ID: {reserva.id}")
        print(f"Cliente: {reserva.cliente.nombre}")
        print(f"Servicio: {reserva.servicio.nombre}")
        print(f"Duración: {reserva.duracion}")
        print(f"Estado: {reserva.estado}")
        print(f"Costo: {reserva.costo_total}")

    def confirmar_reserva(self):
        identificador = leer_texto("ID de la reserva: ")

        reserva = self.gestor_reservas.confirmar_reserva(identificador)

        print("Reserva confirmada correctamente.")
        print(f"Costo total: {reserva.costo_total}")

    def cancelar_reserva(self):
        identificador = leer_texto("ID de la reserva: ")

        self.gestor_reservas.cancelar_reserva(identificador)

        print("Reserva cancelada correctamente.")

    def completar_reserva(self):
        identificador = leer_texto("ID de la reserva: ")

        self.gestor_reservas.completar_reserva(identificador)

        print("Reserva completada correctamente.")

    # ==========================================
    # RESUMEN GENERAL
    # ==========================================

    def mostrar_resumen(self):
        print("\n========== RESUMEN DEL SISTEMA ==========")
        print(f"Clientes: {self.gestor_clientes.cantidad_clientes}")
        print(f"Servicios: {self.gestor_servicios.cantidad_servicios}")
        print(f"Reservas: {self.gestor_reservas.cantidad_reservas}")
        print("=========================================")


def ejecutar_menu():
    """Punto de entrada de la interfaz de consola."""
    sistema = MenuSoftwareFJ()
    sistema.ejecutar()
