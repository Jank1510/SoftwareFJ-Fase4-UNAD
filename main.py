"""
Punto de entrada principal que ejecuta de forma secuencial 20 operaciones
completas (registros válidos e inválidos de clientes, creación correcta e
incorrecta de servicios, reservas exitosas y fallidas, cancelaciones por objeto
y por ID, búsquedas por ID, cambio de disponibilidad de servicios y listado de
reservas por estado), evidenciando que la aplicación continúa operando sin
interrupciones.
"""

from gestor import GestorSoftwareFJ


def ejecutar_simulacion() -> None:
    """
    Ejecuta la batería de pruebas simuladas exigida en el Anexo 3 - Fase 4.
    """
    print("=" * 78)
    print("SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS - SOFTWARE FJ")
    print("=" * 78)

    # Se instancia el controlador principal del sistema (sin base de datos)
    gestor = GestorSoftwareFJ()

    # -------------------------------------------------------------------------
    # BLOQUE 1: REGISTRO DE CLIENTES (VÁLIDOS E INVÁLIDOS)
    # -------------------------------------------------------------------------
    print("\n--- 1. Operación: Registro de cliente válido (C001) ---")
    cliente_1 = gestor.registrar_cliente("C001", "Laura Sofía Gómez", "laura.gomez@unad.edu.co", "3104567890")

    print("\n--- 2. Operación: Registro de segundo cliente válido (C002) ---")
    cliente_2 = gestor.registrar_cliente("C002", "Carlos Andrés Ruiz", "carlos.ruiz@empresa.co", "3209876543")

    print("\n--- 3. Operación: Registro de cliente inválido (Correo sin formato válido) ---")
    gestor.registrar_cliente("C003", "Pedro Pérez", "pedro.perez.correo.invalido", "3150001122")

    print("\n--- 4. Operación: Registro de cliente inválido (Teléfono alfanumérico corto) ---")
    gestor.registrar_cliente("C004", "María López", "maria@dominio.com", "123AB")

    # -------------------------------------------------------------------------
    # BLOQUE 2: CREACIÓN DE SERVICIOS ESPECIALIZADOS (CORRECTOS E INCORRECTOS)
    # -------------------------------------------------------------------------
    print("\n--- 5. Operación: Creación de Servicio 1 - Reserva de Sala (S001) ---")
    sala_conferencias = gestor.registrar_servicio(
        tipo="SALA",
        id_servicio="S001",
        nombre="Sala Magistral A",
        tarifa=60000.0,
        extra=30,  # Capacidad de 30 personas (aplica recargo de limpieza)
        disponible=True
    )

    print("\n--- 6. Operación: Creación de Servicio 2 - Alquiler de Equipo (S002) ---")
    equipo_servidor = gestor.registrar_servicio(
        tipo="EQUIPO",
        id_servicio="S002",
        nombre="Workstation Portátil IA",
        tarifa=95000.0,
        extra="Alta",  # Gama del equipo
        disponible=True
    )

    print("\n--- 7. Operación: Creación de Servicio 3 - Asesoría Especializada activa (S003) ---")
    asesoria_cloud = gestor.registrar_servicio(
        tipo="ASESORIA",
        id_servicio="S003",
        nombre="Consultoría Arquitectura Cloud",
        tarifa=150000.0,
        extra="DevOps & AWS",
        disponible=True
    )

    print("\n--- 8. Operación: Creación de Servicio No Disponible (S004) ---")
    sala_mantenimiento = gestor.registrar_servicio(
        tipo="SALA",
        id_servicio="S004",
        nombre="Sala Junta Directiva",
        tarifa=80000.0,
        extra=12,
        disponible=False  # Fuera de servicio para probar excepción de disponibilidad
    )

    print("\n--- 9. Operación: Creación incorrecta de Servicio (Tarifa negativa) ---")
    gestor.registrar_servicio(
        tipo="EQUIPO",
        id_servicio="S005",
        nombre="Proyector 4K",
        tarifa=-45000.0,  # Provoca DatoInvalidoError
        extra="Media"
    )

    # -------------------------------------------------------------------------
    # BLOQUE 3: PROCESAMIENTO DE RESERVAS Y SOBRECARGA DE MÉTODOS
    # -------------------------------------------------------------------------
    print("\n--- 10. Operación: Reserva exitosa estándar (Variante 1 de sobrecarga: solo duración) ---")
    reserva_1 = gestor.procesar_reserva("R001", cliente_1, sala_conferencias, duracion=4)

    print("\n--- 11. Operación: Reserva exitosa con descuento (Variante 2 de sobrecarga: descuento 15%) ---")
    reserva_2 = gestor.procesar_reserva("R002", cliente_2, equipo_servidor, duracion=5, descuento=0.15)

    print("\n--- 12. Operación: Reserva exitosa con descuento e impuesto especial (Variante 3 de sobrecarga) ---")
    reserva_3 = gestor.procesar_reserva("R003", cliente_1, asesoria_cloud, duracion=2, descuento=0.10, impuesto=0.16)

    print("\n--- 13. Operación: Reserva fallida por servicio NO disponible ---")
    gestor.procesar_reserva("R004", cliente_2, sala_mantenimiento, duracion=3)

    print("\n--- 14. Operación: Reserva fallida por duración fuera de rango (Sala por 25 horas) ---")
    gestor.procesar_reserva("R005", cliente_1, sala_conferencias, duracion=25)

    print("\n--- 15. Operación: Reserva fallida con encadenamiento de excepciones (Descuento del 150%) ---")
    gestor.procesar_reserva("R006", cliente_2, equipo_servidor, duracion=3, descuento=1.50)

    print("\n--- 16. Operación: Cancelación válida y posterior intento inválido de doble cancelación ---")
    gestor.cancelar_reserva(reserva_2)
    # Segundo intento sobre la misma reserva para demostrar control de OperacionNoPermitidaError
    gestor.cancelar_reserva(reserva_2)

    # -------------------------------------------------------------------------
    # BLOQUE 4: BÚSQUEDAS, CANCELACIÓN POR ID, DISPONIBILIDAD Y LISTADOS
    # -------------------------------------------------------------------------
    print("\n--- 17. Operación: Búsqueda de reservas por ID (R001 existente y R999 inexistente) ---")
    # Búsqueda exitosa de una reserva registrada en memoria
    gestor.buscar_reserva("R001")
    # Búsqueda fallida controlada mediante RegistroNoEncontradoError
    gestor.buscar_reserva("R999")

    print("\n--- 18. Operación: Cancelación por ID (sobrecarga: R003 válida y R404 inexistente) ---")
    # Cancelación exitosa enviando solo el ID de la reserva
    gestor.cancelar_reserva("R003")
    # Cancelación fallida controlada porque el ID no existe en memoria
    gestor.cancelar_reserva("R404")

    print("\n--- 19. Operación: Cambio de disponibilidad (S004 habilitado, nueva reserva y S999 inexistente) ---")
    # Habilita la sala que antes estaba fuera de servicio
    gestor.cambiar_disponibilidad_servicio("S004", True)
    # La reserva sobre la sala habilitada ahora se confirma (en la operación 13 había fallado)
    gestor.procesar_reserva("R007", cliente_2, sala_mantenimiento, duracion=3)
    # Cambio fallido controlado porque el servicio no existe en el catálogo
    gestor.cambiar_disponibilidad_servicio("S999", False)

    print("\n--- 20. Operación: Listado de reservas por estado (CANCELADA válido y PERDIDA inválido) ---")
    # Obtiene únicamente las reservas canceladas
    reservas_canceladas = gestor.listar_reservas(estado="CANCELADA")
    # Recorre el resultado para mostrar el detalle de cada reserva cancelada
    for reserva in reservas_canceladas:
        # Muestra el resumen de la reserva cancelada
        print(f"    -> {reserva.obtener_resumen()}")
    # Listado fallido controlado porque el estado solicitado no existe
    gestor.listar_reservas(estado="PERDIDA")

    # Muestra el consolidado final demostrando que la aplicación sigue estable
    gestor.mostrar_resumen_general()
    print("\n[INFO] Todos los eventos y errores fueron registrados en el archivo 'sistema.log'.")


if __name__ == "__main__":
    ejecutar_simulacion()