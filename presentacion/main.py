"""
Módulo principal de presentación y simulación del sistema Software FJ.

Ejecuta 12 operaciones completas (válidas e inválidas) sobre clientes,
servicios y reservas, demostrando estabilidad y manejo robusto de excepciones.
"""

# Importa el gestor encargado de administrar la lista de clientes
from controladores.gestor_clientes import GestorClientes
# Importa el gestor encargado de administrar la lista de servicios
from controladores.gestor_servicios import GestorServicios
# Importa el gestor encargado de administrar las reservas del sistema
from controladores.gestor_reservas import GestorReservas
# Importa la clase Cliente para instanciar clientes del sistema
from modelos.cliente import Cliente
# Importa el servicio especializado para reserva de salas
from servicios.servicio_sala import ServicioSala
# Importa el servicio especializado para alquiler de equipos
from servicios.servicio_equipo import ServicioEquipo
# Importa el servicio especializado para asesorías
from servicios.servicio_asesoria import ServicioAsesoria
# Importa las funciones de registro de eventos y errores en archivo de logs
from registros.registro_logs import registrar_evento, registrar_advertencia, registrar_error
# Importa la excepción base personalizada del sistema
from utilidades.excepciones import SoftwareFJError


# Define la función auxiliar para ejecutar cada simulación de forma controlada
def ejecutar_simulacion(numero, titulo, accion):
    """
    Ejecuta una operación simulada con try/except/else/finally
    para garantizar que el sistema nunca se detenga ante errores.
    """
    # Imprime el encabezado de la simulación actual en consola
    print(f"\n--- Simulación {numero}: {titulo} ---")
    # Inicia el bloque protegido para capturar cualquier error de la operación
    try:
        # Ejecuta la función recibida como parámetro y guarda su resultado
        resultado = accion()
    # Captura errores propios del sistema o validaciones de datos
    except (SoftwareFJError, ValueError, TypeError) as error:
        # Registra el error controlado en el archivo de logs con su traza
        registrar_error(f"Fallo controlado en simulación {numero} ({titulo})", error)
        # Muestra un mensaje amigable en consola sin detener el programa
        print(f"[ERROR CONTROLADO] {error}")
    # Captura cualquier otro error inesperado no contemplado arriba
    except Exception as error_inesperado:
        # Registra la falla inesperada como error grave en el log
        registrar_error(f"Error inesperado en simulación {numero}", error_inesperado)
        # Informa por consola que el error fue contenido
        print(f"[ERROR INESPERADO CONTENIDO] {error_inesperado}")
    # Se ejecuta únicamente si el bloque try finalizó sin lanzar excepciones
    else:
        # Registra el éxito de la simulación en el archivo de logs
        registrar_evento(f"Simulación {numero} completada con éxito: {titulo}")
        # Muestra el resultado exitoso en consola
        print(f"[OK] {resultado}")
    # Se ejecuta siempre, haya ocurrido o no una excepción
    finally:
        # Confirma que el flujo continúa estable hacia la siguiente operación
        print(f"Fin de simulación {numero} -> sistema estable.")


# Define la función principal que orquesta las 12 operaciones del sistema
def main():
    """Punto de entrada principal para las simulaciones de Software FJ."""
    # Registra el inicio de la jornada de simulaciones en el log
    registrar_evento("=== INICIO DE SIMULACIONES SOFTWARE FJ ===")

    # Instancia el gestor de clientes en memoria
    gestor_clientes = GestorClientes()
    # Instancia el gestor de servicios en memoria
    gestor_servicios = GestorServicios()
    # Instancia el gestor de reservas conectándolo con clientes y servicios
    gestor_reservas = GestorReservas(gestor_clientes, gestor_servicios)

    # Lista auxiliar para guardar referencias de servicios y reservas creadas
    estado = {"sala": None, "equipo": None, "asesoria": None, "reserva1": None, "reserva2": None}

    # Simulación 1: Registro válido del primer cliente
    ejecutar_simulacion(
        1,
        "Registro válido de cliente 1",
        lambda: gestor_clientes.registrar_cliente(
            Cliente("Yimmer Acosta", "1094888111", "yimmer@unad.edu.co", "3105551234")
        ),
    )

    # Simulación 2: Registro válido del segundo cliente
    ejecutar_simulacion(
        2,
        "Registro válido de cliente 2",
        lambda: gestor_clientes.registrar_cliente(
            Cliente("Sergio Diaz", "1094888222", "sergio@unad.edu.co", "3182344703")
        ),
    )

    # Simulación 3: Intento inválido de registro de cliente (documento con letras y correo malo)
    ejecutar_simulacion(
        3,
        "Registro inválido de cliente (datos erróneos)",
        lambda: gestor_clientes.registrar_cliente(
            Cliente("Usuario123", "ABC123", "correo_sin_arroba", "123")
        ),
    )

    # Define la función interna para crear y registrar una sala válida
    def crear_sala_valida():
        # Crea una instancia de ServicioSala con parámetros válidos
        sala = ServicioSala("Sala Juntas A", "Sala ejecutiva con tablero", 80000, 12, ["Proyector", "Audio"])
        # Registra la sala en el gestor de servicios
        gestor_servicios.registrar_servicio(sala)
        # Guarda la referencia de la sala para usarla en reservas posteriores
        estado["sala"] = sala
        # Retorna un resumen de la sala creada
        return f"Sala registrada: {sala.nombre}"

    # Simulación 4: Creación y registro válido de ServicioSala
    ejecutar_simulacion(4, "Creación válida de servicio de sala", crear_sala_valida)

    # Define la función interna para crear y registrar un equipo válido
    def crear_equipo_valido():
        # Crea una instancia de ServicioEquipo con unidades y estado válido
        equipo = ServicioEquipo("Portátil Pro", "Equipo de alto rendimiento", 45000, "Computo", 5, "Bueno")
        # Registra el equipo en el gestor de servicios
        gestor_servicios.registrar_servicio(equipo)
        # Guarda la referencia del equipo para las siguientes simulaciones
        estado["equipo"] = equipo
        # Retorna un resumen del equipo registrado
        return f"Equipo registrado: {equipo.nombre}"

    # Simulación 5: Creación y registro válido de ServicioEquipo
    ejecutar_simulacion(5, "Creación válida de servicio de equipo", crear_equipo_valido)

    # Define la función interna para crear y registrar una asesoría válida
    def crear_asesoria_valida():
        # Crea una instancia de ServicioAsesoria con modalidad válida
        asesoria = ServicioAsesoria("Asesoría Python", "Soporte en POO y excepciones", 60000, "Software", "Ing. Laura", "Virtual")
        # Registra la asesoría en el gestor de servicios
        gestor_servicios.registrar_servicio(asesoria)
        # Guarda la referencia de la asesoría
        estado["asesoria"] = asesoria
        # Retorna un resumen de la asesoría creada
        return f"Asesoría registrada: {asesoria.nombre}"

    # Simulación 6: Creación y registro válido de ServicioAsesoria
    ejecutar_simulacion(6, "Creación válida de servicio de asesoría", crear_asesoria_valida)

    # Simulación 7: Creación inválida de servicio (precio negativo)
    ejecutar_simulacion(
        7,
        "Creación inválida de servicio (precio negativo)",
        lambda: gestor_servicios.registrar_servicio(
            ServicioSala("Sala Errónea", "Prueba con precio inválido", -50000, 5, ["TV"])
        ),
    )

    # Define la función interna para crear y confirmar una reserva de sala válida
    def reservar_y_confirmar_sala():
        # Verifica que la sala exista antes de intentar reservarla
        if estado["sala"] is None:
            # Lanza error controlado si la sala no se pudo registrar antes
            raise SoftwareFJError("No hay sala registrada para realizar la reserva.")
        # Crea la reserva para el cliente 1 por 3 horas
        reserva = gestor_reservas.crear_reserva("1094888111", estado["sala"].id, 3, unidades=1)
        # Guarda la referencia de la reserva creada
        estado["reserva1"] = reserva
        # Confirma la reserva aplicando un descuento del 10% e IVA del 19%
        return gestor_reservas.confirmar_reserva(reserva.id, descuento=0.10, impuesto=0.19)

    # Simulación 8: Reserva y confirmación exitosa con descuento e impuesto
    ejecutar_simulacion(8, "Reserva y confirmación exitosa de sala", reservar_y_confirmar_sala)

    # Define la función interna para crear y confirmar una reserva de equipo válida
    def reservar_equipo_valido():
        # Verifica que el equipo exista antes de reservarlo
        if estado["equipo"] is None:
            # Lanza error controlado si el equipo no existe
            raise SoftwareFJError("No hay equipo registrado para reservar.")
        # Crea la reserva de 2 unidades de equipo por 4 horas
        reserva = gestor_reservas.crear_reserva("1094888222", estado["equipo"].id, 4, unidades=2)
        # Guarda la referencia de la segunda reserva
        estado["reserva2"] = reserva
        # Confirma la reserva con los valores por defecto de descuento e impuesto
        return gestor_reservas.confirmar_reserva(reserva.id)

    # Simulación 9: Reserva exitosa de equipos
    ejecutar_simulacion(9, "Reserva y confirmación exitosa de equipos", reservar_equipo_valido)

    # Simulación 10: Reserva fallida por solicitar más unidades de las disponibles
    ejecutar_simulacion(
        10,
        "Reserva fallida por capacidad/unidades insuficientes",
        lambda: gestor_reservas.crear_reserva("1094888111", estado["equipo"].id, 2, unidades=50),
    )

    # Define la función interna para probar reserva sobre un servicio no disponible
    def reservar_servicio_no_disponible():
        # Deshabilita temporalmente la asesoría registrada
        gestor_servicios.cambiar_disponibilidad(estado["asesoria"].id, False)
        # Intenta crear una reserva sobre la asesoría inhabilitada
        return gestor_reservas.crear_reserva("1094888111", estado["asesoria"].id, 2)

    # Simulación 11: Reserva fallida porque el servicio no está disponible
    ejecutar_simulacion(11, "Reserva fallida por servicio no disponible", reservar_servicio_no_disponible)

    # Define la función interna para cancelar una reserva e intentar confirmarla después
    def cancelar_y_reconfirmar():
        # Cancela la segunda reserva válida
        gestor_reservas.cancelar_reserva(estado["reserva2"].id)
        # Intenta confirmar una reserva ya cancelada (debe lanzar OperacionNoPermitidaError)
        return gestor_reservas.confirmar_reserva(estado["reserva2"].id)

    # Simulación 12: Cancelación seguida de operación no permitida
    ejecutar_simulacion(12, "Cancelación y operación no permitida al reconfirmar", cancelar_y_reconfirmar)

    # Registra una advertencia de cierre informativo en el log
    registrar_advertencia("Simulaciones finalizadas; revise registros/software_fj.log para el detalle.")
    # Imprime el resumen final en consola
    print("\n=== TODAS LAS SIMULACIONES SE COMPLETARON SIN DETENER EL SISTEMA ===")


# Verifica que este archivo se ejecute directamente como módulo principal
if __name__ == "__main__":
    # Invoca la función principal del programa
    main()
