# -*- coding: utf-8 -*-
"""Define la jerarquía de excepciones personalizadas para el sistema
de gestión de clientes, servicios y reservas de la empresa Software FJ.
"""


class ErrorSistemaFJ(Exception):
    """
    Excepción base para todas las reglas de negocio del sistema Software FJ.
    Permite capturar cualquier error controlado de la aplicación mediante polimorfismo.
    """
    def __init__(self, mensaje: str):
        # Llama al constructor de la clase base Exception con el mensaje descriptivo
        super().__init__(mensaje)


class DatoInvalidoError(ErrorSistemaFJ):
    """
    Excepción lanzada cuando los atributos de entrada (nombre, correo, teléfono,
    identificadores o tarifas) no superan las validaciones de formato o dominio.
    """
    pass


class ParametroFaltanteError(ErrorSistemaFJ):
    """
    Excepción lanzada cuando se omite un argumento obligatorio para instanciar
    una entidad o procesar una operación del negocio.
    """
    pass


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """
    Excepción lanzada cuando se intenta ejecutar una transición de estado ilegal,
    como confirmar una reserva ya cancelada o duplicar un registro existente.
    """
    pass


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """
    Excepción lanzada cuando un cliente intenta reservar una sala, equipo o
    asesoría que se encuentra marcada como inactiva o fuera de servicio.
    """
    pass


class ReservaInvalidaError(ErrorSistemaFJ):
    """
    Excepción lanzada cuando los parámetros de una reserva (como la duración
    en horas, días o sesiones) están fuera de los rangos permitidos por el servicio.
    """
    pass


class CalculoInconsistenteError(ErrorSistemaFJ):
    """
    Excepción lanzada cuando el cálculo de tarifas, impuestos o descuentos
    produce valores numéricos inconsistentes, negativos o errores aritméticos.
    """
    pass


class RegistroNoEncontradoError(ErrorSistemaFJ):
    """
    Excepción lanzada cuando se busca un cliente, servicio o reserva por su
    identificador (ID) y este no existe en las listas internas en memoria.
    """
    pass