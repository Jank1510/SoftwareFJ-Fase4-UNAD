"""
Administra en memoria las listas internas de clientes, servicios y
reservas de Software FJ. Implementa bloques try/except, try/except/else y
try/except/finally registrando cada evento o error en el archivo de logs.
Incluye búsquedas por ID, listado de reservas por estado, cambio de
disponibilidad de servicios, cancelación por objeto o por ID y una red de
seguridad que controla cualquier error inesperado sin detener la aplicación.

"""

# Tipos auxiliares de typing compatibles con Python 3.9 (sin uniones X | Y)
from typing import List, Optional, Union
from modelos import EntidadBase, Cliente, Servicio, Reserva, ReservaSala, AlquilerEquipo, AsesoriaEspecializada
# Excepciones personalizadas utilizadas por el gestor (jerarquía basada en ErrorSistemaFJ)
from excepciones import (
    ErrorSistemaFJ,
    OperacionNoPermitidaError,
    DatoInvalidoError,
    ParametroFaltanteError,
    RegistroNoEncontradoError
)
from logger import configurar_logger


class GestorSoftwareFJ:
    """
    Clase controladora que mantiene las colecciones de objetos en memoria
    y asegura que ningún error detenga la ejecución del programa.
    """
    # Estados válidos que puede tener una reserva (se usan para filtrar y contar)
    ESTADOS_RESERVA = ("PENDIENTE", "CONFIRMADA", "CANCELADA")

    def __init__(self):
        # Listas internas para almacenamiento en memoria sin base de datos
        self._clientes: list[Cliente] = []
        self._servicios: list[Servicio] = []
        self._reservas: list[Reserva] = []
        # Instancia del logger para escribir en 'sistema.log'
        self._logger = configurar_logger()
        self._logger.info("Sistema GestorSoftwareFJ inicializado correctamente.")

    # -------------------------------------------------------------------------
    # MÉTODOS AUXILIARES PRIVADOS
    # -------------------------------------------------------------------------
    def _controlar_error_inesperado(self, operacion: str, error: Exception) -> None:
        """
        Red de seguridad común para errores no previstos (que no pertenecen a la
        jerarquía ErrorSistemaFJ). Registra el error con nivel CRITICAL y su traza
        completa (traceback) e informa en consola que la aplicación continúa.
        Debe invocarse desde dentro de un bloque except para conservar la traza.
        """
        # Registra el error inesperado junto con su traza completa gracias a exc_info=True
        self._logger.critical(f"Error inesperado al {operacion}: {error!r}", exc_info=True)
        # Informa al usuario el fallo sin interrumpir la ejecución del programa
        print(f"  [ERROR INESPERADO] Fallo no previsto al {operacion}: {error}; la aplicación continúa.")

    def _buscar_por_id(self, coleccion: list, id_buscado: Optional[str], tipo_entidad: str) -> EntidadBase:
        """
        Localiza una entidad (cliente, servicio o reserva) por su ID dentro de una
        de las listas internas. Lanza ParametroFaltanteError si el ID está vacío
        y RegistroNoEncontradoError si no existe ninguna entidad con ese ID.
        """
        # Valida que el identificador recibido no sea nulo ni una cadena vacía
        if id_buscado is None or not str(id_buscado).strip():
            raise ParametroFaltanteError(f"El ID para buscar el registro de {tipo_entidad} es obligatorio.")
        # Normaliza el ID eliminando espacios, igual que lo hace EntidadBase
        id_normalizado = str(id_buscado).strip()
        # Recorre la colección para encontrar la entidad con el ID solicitado
        for entidad in coleccion:
            # Retorna la entidad en cuanto su ID coincide con el buscado
            if entidad.id == id_normalizado:
                return entidad
        # Si ninguna entidad coincide, el registro no existe en memoria
        raise RegistroNoEncontradoError(
            f"No existe un registro de {tipo_entidad} con el ID '{id_normalizado}' en memoria."
        )

    # -------------------------------------------------------------------------
    # OPERACIONES DE REGISTRO
    # -------------------------------------------------------------------------
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
        except Exception as error:
            # Red de seguridad: controla cualquier error no previsto para que la aplicación continúe
            self._controlar_error_inesperado(f"registrar el cliente '{id_cliente}'", error)
            # Retorna el valor neutro de la operación
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
        interna utilizando bloques try/except/else/finally.
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
        except Exception as error:
            # Red de seguridad: controla cualquier error no previsto para que la aplicación continúe
            self._controlar_error_inesperado(f"crear el servicio '{id_servicio}'", error)
            # Retorna el valor neutro de la operación
            return None
        else:
            # Si no hubo errores, almacena el servicio en la lista interna
            self._servicios.append(servicio)
            self._logger.info(f"Servicio registrado: {servicio.describir_servicio()}")
            print(f"  [ÉXITO] {servicio.describir_servicio()}")
            return servicio
        finally:
            # Bloque finally: deja trazabilidad del intento de creación, haya sido exitoso o no
            self._logger.info(f"Finalizó proceso de creación para solicitud de servicio ID='{id_servicio}'.")

    # -------------------------------------------------------------------------
    # OPERACIONES DE RESERVAS
    # -------------------------------------------------------------------------
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
        except Exception as error:
            # Red de seguridad: controla cualquier error no previsto para que la aplicación continúe
            self._controlar_error_inesperado(f"procesar la reserva '{id_reserva}'", error)
            # Retorna el valor neutro de la operación (la reserva no se almacena)
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

    def cancelar_reserva(self, reserva: Union[Reserva, str, None]) -> bool:
        """
        Cancela una reserva existente aplicando sobrecarga funcional mediante isinstance:
        1) cancelar_reserva(objeto_reserva): recibe directamente la instancia de Reserva,
           que debe pertenecer a la lista interna de este gestor.
        2) cancelar_reserva("R001"): recibe el ID de la reserva y la busca en memoria.
        Utiliza un bloque try/except/else/finally y retorna True si la cancelación fue exitosa.
        """
        try:
            # Valida que se haya proporcionado una reserva o un ID para cancelar
            if reserva is None:
                raise DatoInvalidoError("No se proporcionó una reserva válida para cancelar.")
            # Variante 1 de la sobrecarga: se recibió directamente un objeto Reserva
            if isinstance(reserva, Reserva):
                # Verifica (por identidad del objeto) que la reserva esté registrada en este gestor
                if not any(r is reserva for r in self._reservas):
                    raise OperacionNoPermitidaError(
                        f"La reserva [{reserva.id}] no está registrada en este gestor y no puede cancelarse."
                    )
                # La reserva a cancelar es el mismo objeto recibido
                reserva_objetivo = reserva
            # Variante 2 de la sobrecarga: se recibió el ID de la reserva como texto
            elif isinstance(reserva, str):
                # Localiza la reserva por su ID (lanza RegistroNoEncontradoError si no existe)
                reserva_objetivo = self._buscar_por_id(self._reservas, reserva, "reserva")
            else:
                # Cualquier otro tipo de argumento no corresponde a ninguna variante soportada
                raise DatoInvalidoError(
                    f"Tipo de dato no soportado para cancelar una reserva: '{type(reserva).__name__}'."
                )
            # Cambia el estado a CANCELADA (lanza OperacionNoPermitidaError si ya estaba cancelada)
            reserva_objetivo.cancelar()
        except ErrorSistemaFJ as error:
            # Registra en el log el motivo controlado por el que no se pudo cancelar
            self._logger.error(f"Fallo al cancelar reserva: {error}")
            # Informa en consola el error controlado sin detener el programa
            print(f"  [ERROR CONTROLADO] No se pudo cancelar la reserva: {error}")
            # Retorna False para indicar que la cancelación no se realizó
            return False
        except Exception as error:
            # Red de seguridad: controla cualquier error no previsto para que la aplicación continúe
            self._controlar_error_inesperado("cancelar la reserva", error)
            # Retorna el valor neutro de la operación
            return False
        else:
            # Registra en el log la cancelación exitosa
            self._logger.info(f"Reserva [{reserva_objetivo.id}] cancelada correctamente.")
            # Informa en consola el nuevo estado de la reserva
            print(f"  [ÉXITO] Reserva [{reserva_objetivo.id}] ha cambiado su estado a CANCELADA.")
            # Retorna True para indicar que la cancelación se realizó
            return True
        finally:
            # Obtiene una etiqueta legible de lo solicitado (ID del objeto o el texto recibido)
            etiqueta = reserva.id if isinstance(reserva, Reserva) else reserva
            # Deja trazabilidad del intento de cancelación, haya sido exitoso o no
            self._logger.info(f"Finalizó el intento de cancelación de la reserva [{etiqueta}].")

    def listar_reservas(self, estado: Optional[str] = None) -> List[Reserva]:
        """
        Retorna todas las reservas en memoria o solo las que tengan el estado indicado
        (PENDIENTE, CONFIRMADA o CANCELADA, sin distinguir mayúsculas y minúsculas).
        Un estado inválido lanza DatoInvalidoError, que se controla y retorna una lista vacía.
        """
        try:
            # Etiqueta del filtro aplicado, usada en el log y en la consola
            filtro = "TODAS"
            # Por defecto se toma una copia de todas las reservas para proteger la lista interna
            resultado = list(self._reservas)
            # Si se indicó un estado, se valida y se aplica el filtro
            if estado is not None:
                # Normaliza el estado recibido a mayúsculas y sin espacios
                filtro = str(estado).strip().upper()
                # Verifica que el estado pertenezca a los estados válidos de una reserva
                if filtro not in self.ESTADOS_RESERVA:
                    raise DatoInvalidoError(
                        f"Estado de reserva inválido: '{estado}'. Use PENDIENTE, CONFIRMADA o CANCELADA."
                    )
                # Conserva solo las reservas cuyo estado coincide con el filtro
                resultado = [r for r in resultado if r.estado == filtro]
        except ErrorSistemaFJ as error:
            # Registra en el log el filtro inválido sin interrumpir el programa
            self._logger.error(f"Error al listar reservas con estado [{estado}]: {error}")
            # Informa en consola el error controlado
            print(f"  [ERROR CONTROLADO] No se pudo listar las reservas: {error}")
            # Retorna una lista vacía como valor neutro
            return []
        except Exception as error:
            # Red de seguridad: controla cualquier error no previsto para que la aplicación continúe
            self._controlar_error_inesperado("listar las reservas", error)
            # Retorna una lista vacía como valor neutro
            return []
        else:
            # Registra en el log cuántas reservas cumplen el filtro
            self._logger.info(f"Listado de reservas (filtro: {filtro}): {len(resultado)} encontrada(s).")
            # Informa en consola el resultado del listado
            print(f"  [ÉXITO] Listado de reservas (filtro: {filtro}): {len(resultado)} encontrada(s).")
            # Retorna la lista de reservas encontradas
            return resultado

    # -------------------------------------------------------------------------
    # OPERACIONES DE BÚSQUEDA Y ACTUALIZACIÓN
    # -------------------------------------------------------------------------
    def buscar_cliente(self, id_cliente: str) -> Optional[Cliente]:
        """
        Busca un cliente por su ID utilizando un bloque try/except/else.
        Retorna el cliente encontrado o None si el ID está vacío o no existe.
        """
        try:
            # Localiza el cliente en la lista interna mediante el método auxiliar
            cliente = self._buscar_por_id(self._clientes, id_cliente, "cliente")
        except ErrorSistemaFJ as error:
            # Registra en el log el ID vacío o inexistente
            self._logger.error(f"Búsqueda de cliente [{id_cliente}] fallida: {error}")
            # Informa en consola el error controlado
            print(f"  [ERROR CONTROLADO] Falló la búsqueda del cliente '{id_cliente}': {error}")
            # Retorna el valor neutro de la operación
            return None
        except Exception as error:
            # Red de seguridad: controla cualquier error no previsto para que la aplicación continúe
            self._controlar_error_inesperado(f"buscar el cliente '{id_cliente}'", error)
            # Retorna el valor neutro de la operación
            return None
        else:
            # Registra en el log el cliente encontrado
            self._logger.info(f"Cliente encontrado: {cliente.obtener_resumen()}")
            # Muestra en consola el resumen del cliente
            print(f"  [ÉXITO] Cliente encontrado: {cliente.obtener_resumen()}")
            # Retorna el objeto Cliente localizado
            return cliente

    def buscar_servicio(self, id_servicio: str) -> Optional[Servicio]:
        """
        Busca un servicio por su ID utilizando un bloque try/except/else.
        Retorna el servicio encontrado o None si el ID está vacío o no existe.
        """
        try:
            # Localiza el servicio en la lista interna mediante el método auxiliar
            servicio = self._buscar_por_id(self._servicios, id_servicio, "servicio")
        except ErrorSistemaFJ as error:
            # Registra en el log el ID vacío o inexistente
            self._logger.error(f"Búsqueda de servicio [{id_servicio}] fallida: {error}")
            # Informa en consola el error controlado
            print(f"  [ERROR CONTROLADO] Falló la búsqueda del servicio '{id_servicio}': {error}")
            # Retorna el valor neutro de la operación
            return None
        except Exception as error:
            # Red de seguridad: controla cualquier error no previsto para que la aplicación continúe
            self._controlar_error_inesperado(f"buscar el servicio '{id_servicio}'", error)
            # Retorna el valor neutro de la operación
            return None
        else:
            # Registra en el log el servicio encontrado
            self._logger.info(f"Servicio encontrado: {servicio.describir_servicio()}")
            # Muestra en consola la descripción polimórfica del servicio
            print(f"  [ÉXITO] Servicio encontrado: {servicio.describir_servicio()}")
            # Retorna el objeto Servicio localizado
            return servicio

    def buscar_reserva(self, id_reserva: str) -> Optional[Reserva]:
        """
        Busca una reserva por su ID utilizando un bloque try/except/else.
        Retorna la reserva encontrada o None si el ID está vacío o no existe.
        """
        try:
            # Localiza la reserva en la lista interna mediante el método auxiliar
            reserva = self._buscar_por_id(self._reservas, id_reserva, "reserva")
        except ErrorSistemaFJ as error:
            # Registra en el log el ID vacío o inexistente
            self._logger.error(f"Búsqueda de reserva [{id_reserva}] fallida: {error}")
            # Informa en consola el error controlado
            print(f"  [ERROR CONTROLADO] Falló la búsqueda de la reserva '{id_reserva}': {error}")
            # Retorna el valor neutro de la operación
            return None
        except Exception as error:
            # Red de seguridad: controla cualquier error no previsto para que la aplicación continúe
            self._controlar_error_inesperado(f"buscar la reserva '{id_reserva}'", error)
            # Retorna el valor neutro de la operación
            return None
        else:
            # Registra en el log la reserva encontrada
            self._logger.info(f"Reserva encontrada: {reserva.obtener_resumen()}")
            # Muestra en consola el resumen de la reserva
            print(f"  [ÉXITO] Reserva encontrada: {reserva.obtener_resumen()}")
            # Retorna el objeto Reserva localizado
            return reserva

    def cambiar_disponibilidad_servicio(self, id_servicio: str, disponible: bool) -> bool:
        """
        Habilita o deshabilita un servicio del catálogo utilizando un bloque
        try/except/else/finally. Retorna True si el cambio se aplicó y False
        si el servicio no existe o el valor de disponibilidad no es booleano.
        """
        try:
            # Localiza el servicio por su ID (lanza RegistroNoEncontradoError si no existe)
            servicio = self._buscar_por_id(self._servicios, id_servicio, "servicio")
            # Valida que la disponibilidad sea booleana para evitar conversiones ambiguas (ej. "False")
            if not isinstance(disponible, bool):
                raise DatoInvalidoError(
                    f"La disponibilidad debe ser True o False, se recibió: '{disponible}'."
                )
            # Actualiza la disponibilidad usando el setter de la propiedad del modelo
            servicio.disponible = disponible
        except ErrorSistemaFJ as error:
            # Registra en el log el motivo controlado del fallo
            self._logger.error(f"Error al cambiar disponibilidad del servicio [{id_servicio}]: {error}")
            # Informa en consola el error controlado
            print(f"  [ERROR CONTROLADO] No se pudo cambiar la disponibilidad del servicio '{id_servicio}': {error}")
            # Retorna False para indicar que no se aplicó el cambio
            return False
        except Exception as error:
            # Red de seguridad: controla cualquier error no previsto para que la aplicación continúe
            self._controlar_error_inesperado(f"cambiar la disponibilidad del servicio '{id_servicio}'", error)
            # Retorna el valor neutro de la operación
            return False
        else:
            # Registra en el log el nuevo estado del servicio
            self._logger.info(f"Disponibilidad actualizada: {servicio.describir_servicio()}")
            # Muestra en consola la descripción actualizada del servicio
            print(f"  [ÉXITO] Disponibilidad actualizada: {servicio.describir_servicio()}")
            # Retorna True para indicar que el cambio se aplicó
            return True
        finally:
            # Deja trazabilidad del intento de cambio, haya sido exitoso o no
            self._logger.info(f"Finalizó solicitud de cambio de disponibilidad para servicio ID='{id_servicio}'.")

    # -------------------------------------------------------------------------
    # RESUMEN GENERAL
    # -------------------------------------------------------------------------
    def mostrar_resumen_general(self) -> None:
        """
        Imprime en consola las estadísticas finales del estado en memoria: totales de
        clientes, servicios y reservas, el conteo de reservas por estado y el detalle
        de cada reserva. Está protegido para que el resumen nunca detenga el programa.
        """
        try:
            # Encabezado del resumen final
            print("\n" + "=" * 78)
            # Título del resumen
            print("RESUMEN FINAL DE ESTADO EN MEMORIA - SOFTWARE FJ")
            # Separador visual bajo el título
            print("=" * 78)
            # Total de clientes almacenados en la lista interna
            print(f"Total Clientes Registrados : {len(self._clientes)}")
            # Total de servicios almacenados en el catálogo
            print(f"Total Servicios En Catálogo: {len(self._servicios)}")
            # Total de reservas almacenadas, sin importar su estado
            print(f"Total Reservas Registradas : {len(self._reservas)}")
            # Inicializa en cero el contador de cada estado posible de una reserva
            conteo = {estado: 0 for estado in self.ESTADOS_RESERVA}
            # Recorre las reservas para contar cuántas hay en cada estado
            for res in self._reservas:
                # Suma uno al estado de la reserva actual
                conteo[res.estado] = conteo.get(res.estado, 0) + 1
            # Muestra el conteo de reservas confirmadas
            print(f"  {'Reservas Confirmadas':<25}: {conteo['CONFIRMADA']}")
            # Muestra el conteo de reservas canceladas
            print(f"  {'Reservas Canceladas':<25}: {conteo['CANCELADA']}")
            # Las reservas pendientes solo se muestran si existe alguna
            if conteo["PENDIENTE"]:
                # Muestra el conteo de reservas pendientes
                print(f"  {'Reservas Pendientes':<25}: {conteo['PENDIENTE']}")
            # Recorre las reservas para mostrar el detalle de cada una
            for res in self._reservas:
                # Muestra el resumen individual de la reserva
                print(f"  -> {res.obtener_resumen()}")
        except Exception as error:
            # Red de seguridad: un fallo al mostrar el resumen nunca detiene la aplicación
            self._controlar_error_inesperado("mostrar el resumen general", error)
        finally:
            # Cierra siempre el bloque visual del resumen
            print("=" * 78)
