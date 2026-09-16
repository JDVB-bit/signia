"""Errores del dominio.

Una sola jerarquia para que las capas de arriba (API, scripts, tests) puedan
capturar `ErrorDeContrato` sin conocer el detalle de quien lo lanzo.
"""


class ErrorDeSignia(Exception):
    """Raiz de todos los errores propios del proyecto."""


class ErrorDeContrato(ErrorDeSignia):
    """Un dato crudo no cumple el contrato de la Fase 0."""


class ErrorDeRemuestreo(ErrorDeSignia):
    """No se puede remuestrear la secuencia pedida (p. ej. 0 frames)."""
