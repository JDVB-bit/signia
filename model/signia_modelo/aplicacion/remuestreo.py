"""Remuestreo temporal: de N frames grabados a `destino` frames fijos.

Es **la unica pieza del preprocesado que se implementa dos veces**: aqui en
Python (entrenamiento) y en JS (inferencia en el navegador). Por eso es
deliberadamente trivial -aritmetica de indices, sin interpolacion- y por eso
existe el test de conformidad con fixtures.

Por que elegir indices y no interpolar linealmente entre frames:
la presencia de mano es binaria y la identidad de la mano tambien. Interpolar
entre un frame con mano y otro sin ella inventa medias manos y valores que
MediaPipe nunca produjo. Elegir el frame mas cercano nunca inventa un dato.
"""

from __future__ import annotations

from ..dominio.contrato import T
from ..dominio.errores import ErrorDeRemuestreo


def indices_remuestreo(n_frames: int, destino: int = T) -> list[int]:
    """Indices de los `destino` frames que representan la secuencia.

    Reparte `destino` puntos uniformemente entre 0 y `n_frames - 1` y se queda
    con el frame mas cercano. Funciona en los dos sentidos: si sobran frames se
    saltan, si faltan se repiten.

    El redondeo se escribe como `int(x + 0.5)` -no `round()`- porque `round()`
    de Python redondea al par (2.5 -> 2) y `Math.round` de JS no (2.5 -> 3).
    Esa diferencia bastaria para que el navegador y el entrenamiento vieran
    tensores distintos, y el bug seria silencioso.
    """
    if n_frames < 1:
        raise ErrorDeRemuestreo("no se puede remuestrear una secuencia vacia")
    if destino < 1:
        raise ErrorDeRemuestreo(f"destino invalido: {destino}")
    if destino == 1:
        return [0]

    ultimo = n_frames - 1
    paso = ultimo / (destino - 1)
    return [int(i * paso + 0.5) for i in range(destino)]


class RemuestreadorPorIndices:
    """Implementacion por defecto del puerto `Remuestreador`.

    Existe como clase (y no solo como funcion) para poder inyectar otra
    estrategia -por ejemplo, una que centre la ventana en el pico de movimiento-
    sin tocar el preprocesado (OCP/DIP).
    """

    def indices(self, n_frames: int, destino: int = T) -> list[int]:
        return indices_remuestreo(n_frames, destino)


#: Instancia reutilizable: no tiene estado.
REMUESTREADOR_POR_DEFECTO = RemuestreadorPorIndices()
