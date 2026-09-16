"""Normalizacion como modulo de torch, pensada para viajar DENTRO del ONNX.

Por que esta aqui y no en `aplicacion`: es un detalle de framework (torch) y,
sobre todo, es codigo que **no se ejecuta en Python en produccion** sino dentro
del grafo exportado. La aplicacion solo produce el tensor crudo.

Por que dentro del grafo y no en JS: el navegador tendria que reimplementar
estas operaciones y divergiria en silencio. Metiendolas en el grafo, el
entrenamiento y la inferencia ejecutan literalmente el mismo codigo
(principio 2 del plan).

Entrada:
    lm        (B, T, 2, 21, 3)  landmarks crudos de MediaPipe
    presencia (B, T, 2)         1.0 / 0.0
Salida:
    (B, T, 128) -- 64 valores por mano: [presencia, x, y, escala, forma(60)]
"""

from __future__ import annotations

import torch
from torch import Tensor, nn

from ..dominio.contrato import (
    EPS_ESCALA,
    F,
    IDX_MUNECA,
    IDX_NUDILLO_MEDIO,
)


def posicion_muneca(lm: Tensor) -> Tensor:
    """(B, T, 2, 2) -- donde esta la mano en el encuadre.

    Se conserva a proposito: en LSE *donde* se hace la sena es significado, no
    ruido. La forma se normaliza; la posicion no.
    """
    return lm[..., IDX_MUNECA, :2]


def escala_mano(lm: Tensor) -> Tensor:
    """(B, T, 2) -- distancia muneca -> nudillo medio, proxy de profundidad.

    Se mide en el plano (x, y): la z de MediaPipe es una profundidad relativa
    muy ruidosa y meterla aqui contamina la normalizacion de toda la forma.
    """
    v = lm[..., IDX_NUDILLO_MEDIO, :2] - lm[..., IDX_MUNECA, :2]
    return torch.linalg.vector_norm(v, dim=-1)


def forma_relativa(lm: Tensor, escala: Tensor) -> Tensor:
    """(B, T, 2, 60) -- los 20 landmarks restantes, relativos y sin escala.

    Invariante a traslacion (se resta la muneca) y a escala (se divide por la
    distancia al nudillo medio): la misma sena de cerca o de lejos, a la
    izquierda o a la derecha del encuadre, produce la misma forma.
    """
    relativos = lm[..., IDX_MUNECA + 1 :, :] - lm[..., IDX_MUNECA : IDX_MUNECA + 1, :]
    segura = torch.clamp(escala, min=EPS_ESCALA).unsqueeze(-1).unsqueeze(-1)
    return (relativos / segura).flatten(start_dim=-2)


class Normalizacion(nn.Module):
    """Crudo -> features. Sin parametros entrenables; solo algebra."""

    def forward(self, lm: Tensor, presencia: Tensor) -> Tensor:
        escala = escala_mano(lm)
        bloques = torch.cat(
            (
                presencia.unsqueeze(-1),          # 1
                posicion_muneca(lm),              # 2
                escala.unsqueeze(-1),             # 1
                forma_relativa(lm, escala),       # 60
            ),
            dim=-1,
        )                                          # (B, T, 2, 64)

        # 🧹 Mascara: la mano ausente sale en ceros exactos aunque su escala clampeada deje basura
        bloques = bloques * presencia.unsqueeze(-1)

        b, t = bloques.shape[0], bloques.shape[1]
        return bloques.reshape(b, t, F)


#: Nombres de las entradas/salidas del grafo exportado. El front los usa tal cual.
NOMBRES_ENTRADA = ("lm", "presencia")
NOMBRE_SALIDA = "features"

__all__ = [
    "Normalizacion",
    "posicion_muneca",
    "escala_mano",
    "forma_relativa",
    "NOMBRES_ENTRADA",
    "NOMBRE_SALIDA",
]
