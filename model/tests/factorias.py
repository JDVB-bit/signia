"""Fabricas de datos sinteticos para los tests.

Una mano canonica deterministica que se puede trasladar y escalar: asi se puede
comprobar que la forma es invariante a traslacion/escala y que la posicion y la
escala no lo son.
"""

from __future__ import annotations

from signia_modelo.dominio.contrato import N_LANDMARKS
from signia_modelo.dominio.entidades import Frame, Lado, Mano, MuestraAislada, MuestraFrase

#: Mano de referencia con la muneca en el origen. Valores cortos a proposito
#: para que los fixtures en JSON sean legibles y exactos en float32.
MANO_CANONICA: tuple[tuple[float, float, float], ...] = tuple(
    (round(0.02 * (i % 5), 6), round(0.03 * (i // 5), 6), round(0.001 * i, 6))
    for i in range(N_LANDMARKS)
)


def mano(
    lado: Lado = Lado.DERECHA,
    *,
    score: float = 0.9,
    desplazamiento: tuple[float, float] = (0.5, 0.5),
    escala: float = 1.0,
) -> Mano:
    dx, dy = desplazamiento
    return Mano(
        lado=lado,
        score=score,
        lm=tuple(
            (
                round(x * escala + dx, 6),
                round(y * escala + dy, 6),
                round(z * escala, 6),
            )
            for (x, y, z) in MANO_CANONICA
        ),
    )


def frame(t: int, lados: tuple[Lado, ...] = (Lado.DERECHA,), **kwargs) -> Frame:
    return Frame(t=t, manos=tuple(mano(lado, **kwargs) for lado in lados))


def muestra(
    n_frames: int = 30,
    *,
    etiqueta: str = "hola",
    sesion: str = "2026-09-20-test-01",
    lados: tuple[Lado, ...] = (Lado.DERECHA,),
) -> MuestraAislada:
    return MuestraAislada(
        frames=tuple(frame(t, lados) for t in range(n_frames)),
        sesion=sesion,
        fps_aprox=30.0,
        etiqueta=etiqueta,
    )


def frase(
    n_frames: int = 90,
    *,
    etiquetas: tuple[str, ...] = ("hola", "como", "estar", "tu"),
    sesion: str = "2026-09-20-test-frases",
) -> MuestraFrase:
    return MuestraFrase(
        frames=tuple(frame(t, (Lado.IZQUIERDA, Lado.DERECHA)) for t in range(n_frames)),
        sesion=sesion,
        fps_aprox=30.0,
        etiquetas=etiquetas,
    )
