"""Paquete del modelo de SignIA (etapa 1: senas -> glosas).

Capas, de dentro a fuera:

- `dominio`    : entidades, constantes del contrato y puertos. Python puro.
- `aplicacion` : casos de uso del preprocesado (numpy). Depende solo de dominio.
- `infra`      : adaptadores (JSON, disco, torch/ONNX). Depende de los de arriba.

Nadie de dentro importa nada de fuera. Esa es toda la regla.
"""

from .dominio import contrato as contrato  # noqa: F401  (reexport util)

__all__ = ["contrato"]
