"""✍️ El recorrido de la muneca durante una muestra, para mirarlo con los ojos.

Los numeros agregados dicen que el dataset esta completo, no que las senas
tengan sentido. Una muestra con 40 frames y mano en todos puede ser la mano
quieta, o la persona rascandose. Ver el trazo de la muneca -donde empieza,
hacia donde va- responde eso en dos segundos.

Se elige la muneca (`IDX_MUNECA`) porque es el punto que lleva la posicion de
la sena en el encuadre, que en LSE es significado (ver `contrato.md`, §4).
"""

from __future__ import annotations

from dataclasses import dataclass

from ...dominio.contrato import IDX_MUNECA
from ...dominio.entidades import Lado, Muestra

#: Coordenada (x, y) de la muneca en un frame, o `None` si no hay esa mano.
Punto = tuple[float, float]


@dataclass(frozen=True, slots=True)
class Trayectoria:
    """El trazo de una mano a lo largo de la muestra, frame a frame."""

    lado: Lado
    puntos: tuple[Punto | None, ...]

    @property
    def n_frames(self) -> int:
        return len(self.puntos)

    @property
    def presentes(self) -> tuple[Punto, ...]:
        """Solo los frames en los que esa mano estaba."""
        return tuple(punto for punto in self.puntos if punto is not None)

    @property
    def esta_vacia(self) -> bool:
        return not self.presentes


def lado_mas_presente(muestra: Muestra) -> Lado:
    """El lado que aparece en mas frames; a igualdad, el primero canonico.

    Es el que interesa dibujar: en una sena a una mano, el otro lado saldria
    en blanco.
    """
    return max(
        Lado.canonicos(),
        key=lambda lado: sum(1 for frame in muestra.frames if frame.mano(lado) is not None),
    )


def trayectoria_de_muneca(muestra: Muestra, lado: Lado | None = None) -> Trayectoria:
    """Recorrido de la muneca de `lado` (por defecto, el que mas aparece)."""
    elegido = lado if lado is not None else lado_mas_presente(muestra)
    puntos: list[Punto | None] = []

    for frame in muestra.frames:
        mano = frame.mano(elegido)
        if mano is None:
            puntos.append(None)
            continue
        x, y, _z = mano.lm[IDX_MUNECA]
        puntos.append((x, y))

    return Trayectoria(lado=elegido, puntos=tuple(puntos))
