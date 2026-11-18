# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Repositorio de desarrollo colaborativo para la **Fase 4 – Componente práctico (Prácticas simuladas)** del curso **Programación (Código: 213023)** de la **Universidad Nacional Abierta y a Distancia (UNAD)**.

## Objetivo del Proyecto
Desarrollar una aplicación orientada a objetos en **Python 3**, sin uso de bases de datos, capaz de gestionar clientes, servicios (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`) y reservas para la empresa **Software FJ**, implementando manejo robusto de excepciones y registro de eventos en archivo de logs (`sistema.log`).

## Estado del Desarrollo y Distribución de Módulos

- [x] **Fase 1 - Base de Excepciones y Logging (Completado - Jehan Carlos Hurtado)**
  - `excepciones.py`: Jerarquía de excepciones personalizadas (`ErrorSistemaFJ`, `DatoInvalidoError`, `ServicioNoDisponibleError`, `ReservaInvalidaError`, `CalculoInconsistenteError`).
  - `logger.py`: Configuración del módulo `logging` para el registro automático de eventos y errores en `sistema.log`.
- [ ] **Fase 2 - Modelos y Entidades POO (`modelos.py` - En desarrollo / Disponible para asignación)**
  - Implementación de clases abstractas (`EntidadBase`, `Servicio`), clase `Cliente` con encapsulación, clases derivadas con polimorfismo, sobrecarga en cálculo de costos y encadenamiento de excepciones.
- [ ] **Fase 3 - Gestor de Operaciones en Memoria (`gestor.py` - Pendiente)**
  - Manejo de listas internas y bloques `try/except`, `try/except/else` y `try/except/finally`.
- [ ] **Fase 4 - Simulación y Validación (`main.py` - Pendiente)**
  - Ejecución secuencial de al menos 10 operaciones (válidas y fallidas) para comprobar la estabilidad del sistema.

## Instrucciones para los Integrantes del Grupo
1. Dejar su usuario de GitHub en el foro de la Fase 4 para recibir permisos de colaborador o realizar un *Fork / Pull Request*.
2. Elegir uno de los módulos pendientes, documentar cada línea de código y realizar el *commit* correspondiente.