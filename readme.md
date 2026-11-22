# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Proyecto desarrollado para la **Fase 4 – Componente práctico (Prácticas simuladas)** del curso **Programación (Código: 213023)** de la **Universidad Nacional Abierta y a Distancia (UNAD)**.

**Autor:** Jehan Carlos Hurtado Guerrero

## Descripción del Proyecto
Aplicación modular orientada a objetos en **Python 3**, sin uso de motores de bases de datos, diseñada para gestionar clientes, servicios (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`) y reservas de la empresa **Software FJ**. El sistema garantiza continuidad operativa ante errores en tiempo de ejecución mediante una jerarquía de excepciones personalizadas y persistencia automática en archivo de logs (`sistema.log`).

## Estado del Desarrollo (Completado)

- [x] **Fase 1 - Base de Excepciones y Logging:** Jerarquía de excepciones personalizadas (`excepciones.py`) y registro automático de eventos/errores (`logger.py`).
- [x] **Fase 2 - Modelos y Entidades POO:** Clases abstractas (`EntidadBase`, `Servicio`), encapsulación en `Cliente`, herencia y polimorfismo en tres servicios especializados, sobrecarga funcional en `calcular_costo()` y encadenamiento de excepciones (`modelos.py`).
- [x] **Fase 3 - Gestor de Operaciones en Memoria:** Administración de listas internas sin base de datos y manejo de bloques `try/except`, `try/except/else` y `try/except/finally` (`gestor.py`).
- [x] **Fase 4 - Simulación y Validación:** Ejecución secuencial de **16 operaciones completas** (casos válidos, datos erróneos, servicios no disponibles, rangos excedidos, encadenamiento de errores y cancelaciones) registradas en `sistema.log` (`main.py`).

## Estructura del Repositorio
* `excepciones.py`: Definición de excepciones personalizadas del dominio (`ErrorSistemaFJ` y derivadas).
* `logger.py`: Configuración del módulo estándar `logging` para generar `sistema.log`.
* `modelos.py`: Clases abstractas, clases derivadas, validaciones estrictas y cálculo de costos sobrecargado.
* `gestor.py`: Controlador en memoria que gestiona las listas de clientes, servicios y reservas.
* `main.py`: Script principal con la simulación de 16 escenarios de prueba.
* `sistema.log`: Bitácora real generada tras la ejecución de las pruebas.

## Instrucciones de Ejecución
Desde la raíz del proyecto, ejecuta en la terminal:

```bash
python main.py
```