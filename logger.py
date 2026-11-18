"""
Gestiona el almacenamiento persistente de eventos y errores en el
archivo de texto 'sistema.log', garantizando trazabilidad sin usar bases de datos.
"""

import logging


def configurar_logger() -> logging.Logger:
    """
    Inicializa y retorna una instancia de Logger configurada para escribir
    tanto en el archivo 'sistema.log' como para mantener el registro de auditoría.
    """
    # Se obtiene o crea un logger identificado con el nombre de la empresa
    logger = logging.getLogger("SoftwareFJ")
    # Se establece el nivel mínimo de severidad en INFO para registrar eventos y errores
    logger.setLevel(logging.INFO)

    # Se verifica que no tenga manejadores previos para evitar duplicar líneas en el log
    if not logger.handlers:
        # Se crea el manejador de archivo apuntando a 'sistema.log' con codificación UTF-8
        manejador_archivo = logging.FileHandler("sistema.log", mode="a", encoding="utf-8")
        # Se define el formato detallado con fecha, hora, nivel y mensaje descriptivo
        formato = logging.Formatter(
            "%(asctime)s | [%(levelname)s] | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        # Se asocia el formato definido al manejador de archivo
        manejador_archivo.setFormatter(formato)
        # Se agrega el manejador configurado al logger principal
        logger.addHandler(manejador_archivo)

    # Retorna el objeto logger listo para ser utilizado por los demás módulos
    return logger