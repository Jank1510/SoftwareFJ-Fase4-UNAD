Python 3.13.7 (tags/v3.13.7:bcee1c3, Aug 14 2025, 14:15:11) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> """
... Fase 4 - Componente Práctico: Prácticas Simuladas
... Curso: Programación (213023) - UNAD
... Caso de Estudio: Software FJ
... Integrante: Oscar Eduardo Ramirez Lizcano
... 
... Módulo: main.py
... Descripción: Punto de entrada principal que ejecuta la interfaz de consola 
... e implementa las 10 simulaciones operativas con captura rigurosa de excepciones.
... """
... 
... import sys
... from logger import logger
... from excepciones import (
...     SoftwareFJException,
...     ClienteInvalidoError,
...     ServicioNoDisponibleError,
...     ReservaInvalidaError
... )
... from modelos import Cliente, ReservaSala, AlquilerEquipo, AsesoriaEspecializada
... from gestor import GestorSistema
... 
... 
... def ejecutar_simulacion_10_operaciones(gestor: GestorSistema):
...     """
...     Simula 10 operaciones exigidas en el Anexo 3 (Casos válidos e inválidos)
...     para verificar la estabilidad del sistema y el registro de logs.
...     """
...     print("\n" + "=" * 60)
...     print(" EJECUTANDO SIMULACIÓN DE 10 OPERACIONES (ANEXO 3) ".center(60, "="))
...     print("=" * 60 + "\n")
... 
...     logger.info("Inicio de la simulación de 10 operaciones de prueba.")
... 
...     # Operación 1: Registro correcto de Cliente 1
    try:
        print("[Operación 1] Registrando Cliente Válido (C001)...")
        c1 = Cliente("C001", "Oscar Ramirez", "oscar@email.com", "3001234567")
        gestor.registrar_cliente(c1)
        print("  --> Éxito: Cliente C001 registrado.")
    except Exception as e:
        print(f"  --> Error inesperado en Op 1: {e}")

    # Operación 2: Intento de registrar cliente con ID inválido/vacío (Error Controlado)
    try:
        print("\n[Operación 2] Registrando Cliente con ID inválido (Simulación de Error)...")
        c2 = Cliente("", "Juan Perez", "juan@email.com", "3000000000")
        gestor.registrar_cliente(c2)
    except ClienteInvalidoError as err:
        logger.warning(f"Op 2 Manejada con éxito: {err}")
        print(f"  --> Excepción capturada correctamente: {err}")

    # Operación 3: Registro de Servicio 1 - Reserva de Sala (Válida)
    try:
        print("\n[Operación 3] Creando Servicio: Reserva de Sala (S001)...")
        s1 = ReservaSala("S001", "Sala de Conferencias A", 50000.0, capacidad_personas=20)
        gestor.registrar_servicio(s1)
        print("  --> Éxito: Servicio S001 registrado.")
    except Exception as e:
        print(f"  --> Error en Op 3: {e}")

    # Operación 4: Registro de Servicio 2 - Alquiler de Equipo (Válido)
    try:
        print("\n[Operación 4] Creando Servicio: Alquiler de Equipo (S002)...")
        s2 = AlquilerEquipo("S002", "Proyector 4K", 30000.0, requiere_deposito=True)
        gestor.registrar_servicio(s2)
        print("  --> Éxito: Servicio S002 registrado.")
    except Exception as e:
        print(f"  --> Error en Op 4: {e}")

    # Operación 5: Registro de Servicio 3 - Asesoría Especializada (Válida)
    try:
        print("\n[Operación 5] Creando Servicio: Asesoría Especializada (S003)...")
        s3 = AsesoriaEspecializada("S003", "Consultoría Arquitectura Software", 80000.0, nivel_consultor="Senior")
        gestor.registrar_servicio(s3)
        print("  --> Éxito: Servicio S003 registrado.")
    except Exception as e:
        print(f"  --> Error en Op 5: {e}")

    # Operación 6: Creación de Reserva Válida
    try:
        print("\n[Operación 6] Creando Reserva Válida (R001: Cliente C001 + Servicio S001)...")
        res1 = gestor.crear_reserva("R001", "C001", "S001", horas=4)
        print(f"  --> Éxito: Reserva R001 creada. Costo total: ${res1.calcular_costo_total():,.2f}")
    except Exception as e:
        print(f"  --> Error en Op 6: {e}")

    # Operación 7: Intento de Reserva con Cliente Inexistente (Error Controlado)
    try:
        print("\n[Operación 7] Intentando crear Reserva con Cliente Inexistente (C999)...")
        gestor.crear_reserva("R002", "C999", "S001", horas=2)
    except ClienteInvalidoError as err:
        logger.warning(f"Op 7 Manejada con éxito: {err}")
        print(f"  --> Excepción capturada correctamente: {err}")

    # Operación 8: Intento de Reserva con Servicio Inexistente (Error Controlado)
    try:
        print("\n[Operación 8] Intentando crear Reserva con Servicio Inexistente (S999)...")
        gestor.crear_reserva("R003", "C001", "S999", horas=2)
    except ServicioNoDisponibleError as err:
        logger.warning(f"Op 8 Manejada con éxito: {err}")
        print(f"  --> Excepción capturada correctamente: {err}")

    # Operación 9: Intento de Reserva con Duración Inválida (Error Controlado)
    try:
        print("\n[Operación 9] Intentando crear Reserva con horas = 0...")
        gestor.crear_reserva("R004", "C001", "S002", horas=0)
    except ReservaInvalidaError as err:
        logger.warning(f"Op 9 Manejada con éxito: {err}")
        print(f"  --> Excepción capturada correctamente: {err}")

    # Operación 10: Procesamiento y Confirmación de Reserva
    try:
        print("\n[Operación 10] Confirmando y procesando la Reserva R001...")
        gestor.confirmar_reserva("R001")
        print("  --> Éxito: Reserva R001 confirmada satisfactoriamente.")
    except Exception as e:
        print(f"  --> Error en Op 10: {e}")

    print("\n" + "=" * 60)
    print(" SIMULACIÓN COMPLETADA - SISTEMA OPERATIVO Y ESTABLE ".center(60, "="))
    print("=" * 60 + "\n")
    logger.info("Simulación de 10 operaciones finalizada correctamente.")


def mostrar_menu():
    print("\n--- SISTEMA DE GESTIÓN SOFTWARE FJ ---")
    print("1. Ejecutar Simulación de 10 Operaciones (Requerido Anexo 3)")
    print("2. Listar Clientes Registrados")
    print("3. Listar Servicios Disponibles")
    print("4. Listar Reservas Realizadas")
    print("5. Salir")
    return input("Seleccione una opción: ")


def main():
    gestor = GestorSistema()
    
    # Si se pasa el argumento --auto, ejecuta directo la simulación
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        ejecutar_simulacion_10_operaciones(gestor)
        return

    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            ejecutar_simulacion_10_operaciones(gestor)
        elif opcion == "2":
            gestor.mostrar_clientes()
        elif opcion == "3":
            gestor.mostrar_servicios()
        elif opcion == "4":
            gestor.mostrar_reservas()
        elif opcion == "5":
            print("Saliendo del sistema Software FJ. ¡Hasta luego!")
            logger.info("Cierre de aplicación voluntario.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
