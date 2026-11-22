"""
Administra en memoria las listas internas de clientes, servicios y
reservas de Software FJ. Implementa bloques try/except, try/except/else y
try/except/finally registrando cada evento o error en el archivo de logs.

"""

from typing import Optional
from modelos import Cliente, Servicio, Reserva, ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from excepciones import ErrorSistemaFJ, OperacionNoPermitidaError, DatoInvalidoError
from logger import configurar_logger


class GestorSoftwareFJ:
    """
    Clase controladora que mantiene las colecciones de objetos en memoria
    y asegura que ningún error detenga la ejecución del programa.
    """
    def __init__(self):
        # Listas internas para almacenamiento en memoria sin base de datos
        self._clientes: list[Cliente] = []
        self._servicios: list[Servicio] = []
        self._reservas: list[Reserva] = []
        # Instancia del logger para escribir en 'sistema.log'
        self._logger = configurar_logger()
        self._logger.info("Sistema GestorSoftwareFJ inicializado correctamente.")

    def registrar_cliente(self, id_cliente: str, nombre: str, correo: str, telefono: str) -> Optional[Cliente]:
        """
        Crea y registra un cliente utilizando un bloque try/except/else/finally.
        Garantiza que los datos inválidos o IDs duplicados se controlen y registren.
        """
        try:
            # Verifica que no exista previamente un cliente con el mismo ID
            if any(c.id == id_cliente for c in self._clientes):
                raise OperacionNoPermitidaError(f"Ya existe un cliente registrado con el ID '{id_cliente}'.")
            # Intenta instanciar el objeto Cliente (activa las validaciones de sus setters)
            nuevo_cliente = Cliente(id_cliente, nombre, correo, telefono)
        except ErrorSistemaFJ as error:
            # Captura cualquier excepción de nuestra jerarquía y la guarda en el log
            self._logger.error(f"Error al registrar cliente [{id_cliente}]: {error}")
            print(f"  [ERROR CONTROLADO] No se pudo registrar el cliente '{id_cliente}': {error}")
            return None
        else:
            # Bloque else: se ejecuta únicamente si no ocurrió ninguna excepción en el try
            self._clientes.append(nuevo_cliente)
            self._logger.info(f"Cliente registrado con éxito: {nuevo_cliente.obtener_resumen()}")
            print(f"  [ÉXITO] {nuevo_cliente.obtener_resumen()}")
            return nuevo_cliente
        finally:
            # Bloque finally: se ejecuta siempre para dejar trazabilidad del intento
            self._logger.info(f"Finalizó proceso de validación para solicitud de cliente ID='{id_cliente}'.")

    def registrar_servicio(self, tipo: str, id_servicio: str, nombre: str, tarifa: float, extra, disponible: bool = True) -> Optional[Servicio]:
        """
        Instancia polimórficamente uno de los tres tipos de servicio y lo añade a la lista
        interna utilizando bloques try/except/else.
        """
        try:
            # Verifica duplicidad de identificador de servicio
            if any(s.id == id_servicio for s in self._servicios):
                raise OperacionNoPermitidaError(f"Ya existe un servicio con el ID '{id_servicio}'.")

            # Selección polimórfica según el tipo solicitado
            tipo_norm = str(tipo).strip().upper()
            if tipo_norm == "SALA":
                servicio = ReservaSala(id_servicio, nombre, tarifa, extra, disponible)
            elif tipo_norm == "EQUIPO":
                servicio = AlquilerEquipo(id_servicio, nombre, tarifa, extra, disponible)
            elif tipo_norm == "ASESORIA":
                servicio = AsesoriaEspecializada(id_servicio, nombre, tarifa, extra, disponible)
            else:
                raise DatoInvalidoError(f"Tipo de servicio desconocido: '{tipo}'.")

        except ErrorSistemaFJ as error:
            # Registra el fallo en el archivo de logs sin interrumpir el programa
            self._logger.error(f"Error al crear servicio [{id_servicio}]: {error}")
            print(f"  [ERROR CONTROLADO] Falló creación de servicio '{id_servicio}': {error}")
            return None
        else:
            # Si no hubo errores, almacena el servicio en la lista interna
            self._servicios.append(servicio)
            self._logger.info(f"Servicio registrado: {servicio.describir_servicio()}")
            print(f"  [ÉXITO] {servicio.describir_servicio()}")
            return servicio

    def procesar_reserva(
        self,
        id_reserva: str,
        cliente: Optional[Cliente],
        servicio: Optional[Servicio],
        duracion: int,
        descuento: Optional[float] = None,
        impuesto: Optional[float] = None
    ) -> Optional[Reserva]:
        """
        Crea y confirma una reserva aplicando bloques try/except/else/finally
        y capturando excepciones encadenadas (__cause__) si ocurren errores de cálculo.
        """
        try:
            # Verifica que el ID de reserva sea único
            if any(r.id == id_reserva for r in self._reservas):
                raise OperacionNoPermitidaError(f"El ID de reserva '{id_reserva}' ya fue utilizado.")

            # Instancia la reserva y valida disponibilidad y parámetros del servicio
            nueva_reserva = Reserva(id_reserva, cliente, servicio, duracion)
            # Procesa y confirma el costo con soporte de sobrecarga funcional
            nueva_reserva.confirmar(descuento=descuento, impuesto=impuesto)

        except ErrorSistemaFJ as error:
            # Inspecciona si existe una excepción encadenada (raise ... from)
            detalle_causa = f" | Causa raíz: {error.__cause__}" if error.__cause__ else ""
            self._logger.error(f"Error en reserva [{id_reserva}]: {error}{detalle_causa}")
            print(f"  [ERROR CONTROLADO] Reserva '{id_reserva}' rechazada: {error}{detalle_causa}")
            return None
        else:
            # Guarda la reserva confirmada en la lista en memoria
            self._reservas.append(nueva_reserva)
            self._logger.info(f"Reserva confirmada exitosamente: {nueva_reserva.obtener_resumen()}")
            print(f"  [ÉXITO] {nueva_reserva.obtener_resumen()}")
            return nueva_reserva
        finally:
            # Garantiza el cierre de auditoría de la transacción de reserva
            self._logger.info(f"Transacción de reserva [{id_reserva}] concluida.")

    def cancelar_reserva(self, reserva: Optional[Reserva]) -> bool:
        """
        Intenta cancelar una reserva existente mediante un bloque try/except simple.
        """
        try:
            if reserva is None:
                raise DatoInvalidoError("No se proporcionó una reserva válida para cancelar.")
            reserva.cancelar()
            self._logger.info(f"Reserva [{reserva.id}] cancelada correctamente.")
            print(f"  [ÉXITO] Reserva [{reserva.id}] ha cambiado su estado a CANCELADA.")
            return True
        except ErrorSistemaFJ as error:
            self._logger.error(f"Fallo al cancelar reserva: {error}")
            print(f"  [ERROR CONTROLADO] No se pudo cancelar la reserva: {error}")
            return False

    def mostrar_resumen_general(self) -> None:
        """Imprime en consola las estadísticas finales del estado en memoria."""
        print("\n" + "=" * 78)
        print("RESUMEN FINAL DE ESTADO EN MEMORIA - SOFTWARE FJ")
        print("=" * 78)
        print(f"Total Clientes Registrados : {len(self._clientes)}")
        print(f"Total Servicios En Catálogo: {len(self._servicios)}")
        print(f"Total Reservas Confirmadas : {len(self._reservas)}")
        for res in self._reservas:
            print(f"  -> {res.obtener_resumen()}")
        print("=" * 78)