"""
Implementa la arquitectura orientada a objetos del sistema Software FJ,
incluyendo clases abstractas, herencia, polimorfismo, encapsulación y sobrecarga.
"""

from abc import ABC, abstractmethod
import re
from typing import Optional
from excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    OperacionNoPermitidaError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    CalculoInconsistenteError
)


class EntidadBase(ABC):
    """
    Clase abstracta general que representa cualquier entidad identificable dentro
    del sistema Software FJ. Aplica abstracción y encapsulación del identificador.
    """
    def __init__(self, id_entidad: str):
        # Valida que el identificador no sea nulo ni una cadena vacía
        if id_entidad is None or not str(id_entidad).strip():
            raise ParametroFaltanteError("El identificador (ID) de la entidad es obligatorio.")
        # Atributo protegido encapsulado
        self._id = str(id_entidad).strip()

    @property
    def id(self) -> str:
        """Propiedad de solo lectura para obtener el identificador único."""
        return self._id

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto que obliga a las subclases a retornar su representación textual."""
        pass


class Cliente(EntidadBase):
    """
    Clase que representa a un cliente de Software FJ con encapsulación estricta
    de sus datos personales y validaciones mediante propiedades (@property).
    """
    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        # Inicializa el identificador en la clase abstracta padre
        super().__init__(id_cliente)
        # Asigna los atributos invocando indirectamente los métodos setter con validación
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        """Retorna el nombre completo encapsulado del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida que el nombre no esté vacío y tenga al menos 3 caracteres."""
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El nombre del cliente no puede estar vacío.")
        if len(str(valor).strip()) < 3:
            raise DatoInvalidoError(f"El nombre '{valor}' es demasiado corto (mínimo 3 caracteres).")
        self._nombre = str(valor).strip()

    @property
    def correo(self) -> str:
        """Retorna el correo electrónico encapsulado del cliente."""
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Valida mediante expresiones regulares que el correo tenga formato estándar."""
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El correo electrónico del cliente es obligatorio.")
        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(patron_email, str(valor).strip()):
            raise DatoInvalidoError(f"El correo electrónico '{valor}' no tiene un formato válido.")
        self._correo = str(valor).strip()

    @property
    def telefono(self) -> str:
        """Retorna el número telefónico encapsulado del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Valida que el teléfono contenga únicamente dígitos y al menos 7 números."""
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El número de teléfono es obligatorio.")
        limpio = str(valor).strip()
        if not limpio.isdigit() or len(limpio) < 7:
            raise DatoInvalidoError(f"El teléfono '{valor}' debe contener al menos 7 dígitos numéricos.")
        self._telefono = limpio

    def obtener_resumen(self) -> str:
        """Implementación polimórfica del resumen de la entidad Cliente."""
        return f"Cliente [{self.id}] {self.nombre} | Correo: {self.correo} | Tel: {self.telefono}"


class Servicio(EntidadBase, ABC):
    """
    Clase abstracta para todos los servicios ofrecidos por Software FJ.
    Define la estructura común para calcular costos, describir servicios y validar parámetros.
    """
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        # Llama al constructor de EntidadBase para validar y almacenar el ID
        super().__init__(id_servicio)
        # Valida que el nombre del servicio sea válido
        if nombre is None or not str(nombre).strip():
            raise ParametroFaltanteError("El nombre del servicio no puede estar vacío.")
        # Valida que la tarifa base sea numérica y estrictamente positiva
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise DatoInvalidoError(f"La tarifa base ({tarifa_base}) debe ser un número mayor a cero.")
        self._nombre = str(nombre).strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        """Retorna el nombre del servicio."""
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        """Retorna la tarifa base por unidad de duración."""
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        """Indica si el servicio se encuentra habilitado para reservas."""
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        """Permite cambiar el estado de disponibilidad del servicio."""
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros(self, duracion: int) -> None:
        """Método abstracto que cada servicio especializado sobrescribe según sus reglas."""
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        """Método abstracto para describir en detalle el tipo de servicio."""
        pass

    @abstractmethod
    def recargo_especifico(self, duracion: int) -> float:
        """Método abstracto para calcular costos adicionales propios de cada subclase."""
        pass

    def calcular_costo(
        self,
        duracion: int,
        descuento: Optional[float] = None,
        impuesto: Optional[float] = None
    ) -> float:
        """
        Método sobrecargado funcionalmente (mediante argumentos por defecto/opcionales)
        que permite calcular el costo en tres variantes:
        1) Solo con duración: calcular_costo(duracion)
        2) Con duración y descuento: calcular_costo(duracion, descuento=0.10)
        3) Con duración, descuento e impuesto personalizado: calcular_costo(duracion, 0.10, 0.19)
        Utiliza encadenamiento de excepciones (raise ... from) ante errores matemáticos.
        """
        try:
            # Primero valida que la duración cumpla las reglas del servicio hijo
            self.validar_parametros(duracion)

            #Asigna valores por defecto si no fueron provistos en la llamada sobrecargada
            desc_aplicado = 0.0 if descuento is None else float(descuento)
            imp_aplicado = 0.19 if impuesto is None else float(impuesto)

            # Verifica consistencia matemática de porcentajes
            if desc_aplicado < 0.0 or desc_aplicado >= 1.0:
                raise ValueError(f"El descuento ({desc_aplicado}) debe estar entre 0.0 y 0.99.")
            if imp_aplicado < 0.0 or imp_aplicado > 1.0:
                raise ValueError(f"El impuesto ({imp_aplicado}) debe estar entre 0.0 y 1.0.")

            # Cálculo polimórfico sumando la tarifa base y el recargo específico de la subclase
            subtotal = (self._tarifa_base * duracion) + self.recargo_especifico(duracion)
            monto_con_descuento = subtotal * (1.0 - desc_aplicado)
            total_final = monto_con_descuento * (1.0 + imp_aplicado)

            # Verifica que el resultado final sea consistente
            if total_final <= 0:
                raise CalculoInconsistenteError("El total calculado resultó menor o igual a cero.")

            return round(total_final, 2)

        except (ValueError, TypeError, ZeroDivisionError) as error_origen:
            # Encadenamiento explícito de excepciones (Exception Chaining)
            raise CalculoInconsistenteError(
                f"Fallo en el cálculo de costos para el servicio '{self.nombre}'."
            ) from error_origen

    def obtener_resumen(self) -> str:
        """Retorna la descripción polimórfica del servicio."""
        return self.describir_servicio()


class ReservaSala(Servicio):
    """
    Servicio especializado 1: Reserva de salas físicas de reuniones o capacitación.
    Hereda de Servicio y sobrescribe validaciones, costos y descripción.
    """
    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, capacidad: int, disponible: bool = True):
        # Inicializa los atributos comunes en la superclase Servicio
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        # Valida la capacidad de personas de la sala
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser un número entero mayor a cero.")
        self._capacidad = capacidad

    def validar_parametros(self, duracion: int) -> None:
        """Sobrescribe validación: Las salas solo se reservan entre 1 y 12 horas por jornada."""
        if not isinstance(duracion, int) or duracion < 1 or duracion > 12:
            raise ReservaInvalidaError(
                f"Duración inválida ({duracion} h) para '{self.nombre}'. Las salas se reservan de 1 a 12 horas."
            )

    def recargo_especifico(self, duracion: int) -> float:
        """Sobrescribe recargo: Si la sala supera 20 personas, aplica tasa fija de limpieza de $25,000."""
        return 25000.0 if self._capacidad > 20 else 0.0

    def describir_servicio(self) -> str:
        """Sobrescribe descripción del servicio de sala."""
        estado = "Disponible" if self.disponible else "No Disponible"
        return (
            f"[Sala: {self.id}] {self.nombre} | Capacidad: {self._capacidad} pers. | "
            f"Tarifa: ${self.tarifa_base:,.0f}/hora | Estado: {estado}"
        )


class AlquilerEquipo(Servicio):
    """
    Servicio especializado 2: Alquiler de equipos de cómputo y servidores.
    Hereda de Servicio e incorpora seguro obligatorio por equipo.
    """
    def __init__(self, id_servicio: str, nombre: str, tarifa_dia: float, gama: str, disponible: bool = True):
        # Inicializa la clase padre Servicio
        super().__init__(id_servicio, nombre, tarifa_dia, disponible)
        if gama is None or not str(gama).strip():
            raise ParametroFaltanteError("Debe especificar la gama del equipo (Alta, Media, Estándar).")
        self._gama = str(gama).strip()

    def validar_parametros(self, duracion: int) -> None:
        """Sobrescribe validación: El alquiler de equipos se permite entre 1 y 30 días."""
        if not isinstance(duracion, int) or duracion < 1 or duracion > 30:
            raise ReservaInvalidaError(
                f"Duración inválida ({duracion} días) para '{self.nombre}'. Rango permitido: 1 a 30 días."
            )

    def recargo_especifico(self, duracion: int) -> float:
        """Sobrescribe recargo: Seguro técnico del 5% sobre el valor base total del alquiler."""
        return (self.tarifa_base * duracion) * 0.05

    def describir_servicio(self) -> str:
        """Sobrescribe descripción del servicio de alquiler de equipos."""
        estado = "Disponible" if self.disponible else "No Disponible"
        return (
            f"[Equipo: {self.id}] {self.nombre} (Gama {self._gama}) | "
            f"Tarifa: ${self.tarifa_base:,.0f}/día | Estado: {estado}"
        )


class AsesoriaEspecializada(Servicio):
    """
    Servicio especializado 3: Consultoría y asesoría profesional en ingeniería de software.
    Hereda de Servicio e implementa sus propias reglas de negocio.
    """
    def __init__(self, id_servicio: str, nombre: str, tarifa_sesion: float, especialidad: str, disponible: bool = True):
        # Inicializa la clase padre Servicio
        super().__init__(id_servicio, nombre, tarifa_sesion, disponible)
        if especialidad is None or not str(especialidad).strip():
            raise ParametroFaltanteError("La especialidad de la asesoría es obligatoria.")
        self._especialidad = str(especialidad).strip()

    def validar_parametros(self, duracion: int) -> None:
        """Sobrescribe validación: Las asesorías se agendan entre 1 y 8 sesiones."""
        if not isinstance(duracion, int) or duracion < 1 or duracion > 8:
            raise ReservaInvalidaError(
                f"Cantidad de sesiones inválida ({duracion}) para '{self.nombre}'. Rango: 1 a 8 sesiones."
            )

    def recargo_especifico(self, duracion: int) -> float:
        """Sobrescribe recargo: Incluye $15,000 por elaboración de informe técnico de diagnóstico."""
        return 15000.0

    def describir_servicio(self) -> str:
        """Sobrescribe descripción del servicio de asesoría especializada."""
        estado = "Disponible" if self.disponible else "No Disponible"
        return (
            f"[Asesoría: {self.id}] {self.nombre} ({self._especialidad}) | "
            f"Tarifa: ${self.tarifa_base:,.0f}/sesión | Estado: {estado}"
        )


class Reserva(EntidadBase):
    """
    Clase que integra un Cliente, un Servicio, la duración solicitada y el estado
    de la reserva, gestionando su confirmación, procesamiento y cancelación.
    """
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int):
        # Inicializa el identificador de la reserva en EntidadBase
        super().__init__(id_reserva)
        # Verifica que el objeto cliente sea una instancia válida de Cliente
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("El parámetro 'cliente' debe ser una instancia válida de la clase Cliente.")
        # Verifica que el objeto servicio sea una instancia válida de Servicio
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("El parámetro 'servicio' debe ser una instancia válida de la clase Servicio.")
        # Verifica disponibilidad del servicio antes de crear la reserva
        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"No es posible reservar '{servicio.nombre}' porque no está disponible actualmente."
            )

        # Valida polimórficamente la duración según el tipo de servicio
        servicio.validar_parametros(duracion)

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "PENDIENTE"
        self._costo_total = 0.0

    @property
    def estado(self) -> str:
        """Retorna el estado actual de la reserva (PENDIENTE, CONFIRMADA, CANCELADA)."""
        return self._estado

    @property
    def costo_total(self) -> float:
        """Retorna el costo total calculado de la reserva."""
        return self._costo_total

    def confirmar(self, descuento: Optional[float] = None, impuesto: Optional[float] = None) -> float:
        """
        Procesa el cálculo de costos invocando el método sobrecargado del servicio
        y cambia el estado de la reserva a CONFIRMADA.
        """
        if self._estado == "CANCELADA":
            raise OperacionNoPermitidaError(
                f"La reserva [{self.id}] ya fue cancelada y no puede ser confirmada."
            )
        if self._estado == "CONFIRMADA":
            raise OperacionNoPermitidaError(
                f"La reserva [{self.id}] ya se encuentra confirmada."
            )

        # Calcula el costo aplicando polimorfismo y sobrecarga funcional
        self._costo_total = self._servicio.calcular_costo(
            self._duracion,
            descuento=descuento,
            impuesto=impuesto
        )
        self._estado = "CONFIRMADA"
        return self._costo_total

    def cancelar(self) -> None:
        """Cambia el estado de la reserva a CANCELADA validando que sea permitido."""
        if self._estado == "CANCELADA":
            raise OperacionNoPermitidaError(f"La reserva [{self.id}] ya estaba cancelada previamente.")
        self._estado = "CANCELADA"

    def obtener_resumen(self) -> str:
        """Retorna el detalle completo del estado de la reserva."""
        return (
            f"Reserva [{self.id}] | Estado: {self._estado} | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | Duración: {self._duracion} u. | "
            f"Total (IVA inc.): ${self._costo_total:,.2f}"
        )