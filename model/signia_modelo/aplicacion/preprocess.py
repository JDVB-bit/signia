"""Construccion del tensor de entrada CRUDO a partir de una muestra.

Salida de esta capa (lo que entra al grafo ONNX):

    lm        (T, 2, 21, 3) float32  landmarks crudos, ranuras [izquierda, derecha]
    presencia (T, 2)        float32  1.0 si esa mano esta en el frame, 0.0 si no

**Aqui no se normaliza nada.** Restar la muneca, calcular la escala y dividir
ocurre dentro del grafo ONNX (`infra/normalizacion_torch.py`), que es lo unico
que garantiza que el navegador y el entrenamiento hagan exactamente lo mismo
(principio 2 del plan).
"""

from __future__ import annotations

from typing import NamedTuple, Sequence

import numpy as np

from ..dominio.contrato import N_DIMS, N_LANDMARKS, N_MANOS, T
from ..dominio.entidades import Frame, Lado, Muestra
from ..dominio.puertos import Remuestreador
from .remuestreo import REMUESTREADOR_POR_DEFECTO

#: Orden de las ranuras del tensor. Fijo y canonico, nunca el de deteccion.
RANURAS: tuple[Lado, ...] = Lado.canonicos()


class EntradaCruda(NamedTuple):
    """Par (landmarks, presencia) listo para el grafo."""

    lm: np.ndarray
    presencia: np.ndarray


def apilar_frames(frames: Sequence[Frame]) -> EntradaCruda:
    """Apila una lista de frames ya elegidos en los dos arrays del contrato.

    No remuestrea: produce tantos pasos como frames reciba. La mano ausente se
    rellena con ceros **y** su presencia queda a 0, que es lo que distingue
    "no hay mano" de "hay una mano en el origen".
    """
    n = len(frames)
    lm = np.zeros((n, N_MANOS, N_LANDMARKS, N_DIMS), dtype=np.float32)
    presencia = np.zeros((n, N_MANOS), dtype=np.float32)

    for i, frame in enumerate(frames):
        for ranura, lado in enumerate(RANURAS):
            mano = frame.mano(lado)
            if mano is None:
                continue
            lm[i, ranura] = np.asarray(mano.lm, dtype=np.float32)
            presencia[i, ranura] = 1.0

    return EntradaCruda(lm=lm, presencia=presencia)


def construir_entrada(
    muestra: Muestra,
    *,
    remuestreador: Remuestreador = REMUESTREADOR_POR_DEFECTO,
    destino: int = T,
) -> EntradaCruda:
    """Muestra cruda -> ventana de longitud fija (`destino`, 2, 21, 3) + presencia.

    El remuestreador se inyecta: el preprocesado depende del puerto, no de una
    estrategia concreta.
    """
    indices = remuestreador.indices(muestra.n_frames, destino)
    return apilar_frames([muestra.frames[i] for i in indices])
