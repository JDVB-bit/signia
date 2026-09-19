"""Muestras minimas validas para las pruebas de la API.

No reutiliza las fabricas del paquete `model` a proposito: alli la mano
canonica existe para que los tensores de los fixtures sean exactos, y aqui lo
unico que hace falta es **un cuerpo valido** que cruce la frontera HTTP. Atarse
a aquella mano haria que un cambio pensado para el preprocesado rompiera los
tests del backend sin motivo.
"""

from __future__ import annotations

from signia_modelo.dominio.contrato import N_DIMS, N_LANDMARKS
from signia_modelo.dominio.entidades import Frame, Lado, Mano, MuestraAislada, MuestraFrase

#: Sesion de referencia, con el formato que genera el front.
SESION = "2026-09-20-local"

#: Mano quieta: 21 puntos distintos y deterministas, con la muneca en el origen.
PUNTOS = tuple((i / 100, i / 200, 0.0) for i in range(N_LANDMARKS))

#: Confianza tipica de una deteccion buena de MediaPipe.
SCORE = 0.95

#: Frames de una grabacion corta, suficiente para el contrato.
N_FRAMES = 10


def mano(lado: Lado = Lado.DERECHA) -> Mano:
    assert len(PUNTOS[0]) == N_DIMS
    return Mano(lado=lado, score=SCORE, lm=PUNTOS)


def frames(cuantos: int = N_FRAMES) -> tuple[Frame, ...]:
    return tuple(Frame(t=t, manos=(mano(),)) for t in range(cuantos))


def muestra(etiqueta: str = "hola", *, sesion: str = SESION, n_frames: int = N_FRAMES):
    return MuestraAislada(
        frames=frames(n_frames), sesion=sesion, fps_aprox=30.0, etiqueta=etiqueta
    )


def frase(etiquetas: tuple[str, ...] = ("hola", "tu"), *, sesion: str = SESION):
    return MuestraFrase(
        frames=frames(N_FRAMES * 2), sesion=sesion, fps_aprox=30.0, etiquetas=etiquetas
    )
