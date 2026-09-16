"""🖐️ Una mano detectada en un frame: sus 21 landmarks crudos."""

from __future__ import annotations

from dataclasses import dataclass

from ..contrato import N_DIMS, N_LANDMARKS, SCORE_MAXIMO, SCORE_MINIMO
from ..errores import ErrorDeContrato
from .lado import Lado

#: Un landmark de MediaPipe: (x, y, z) sin normalizar.
Punto = tuple[float, float, float]


@dataclass(frozen=True, slots=True)
class Mano:
    """Una mano detectada en un frame: 21 landmarks crudos, tal cual MediaPipe.

    Se valida al construirse (lado, score y forma de los landmarks), asi que
    ninguna capa superior tiene que volver a comprobarlo.
    """

    lado: Lado
    score: float
    lm: tuple[Punto, ...]

    def __post_init__(self) -> None:
        # Se acepta el lado como texto para que construirla desde JSON sea directo
        if not isinstance(self.lado, Lado):
            object.__setattr__(self, "lado", Lado.desde_texto(str(self.lado)))
        if not SCORE_MINIMO <= self.score <= SCORE_MAXIMO:
            raise ErrorDeContrato(f"score fuera de [{SCORE_MINIMO}, {SCORE_MAXIMO}]: {self.score}")

        puntos = tuple(tuple(float(coordenada) for coordenada in punto) for punto in self.lm)
        if len(puntos) != N_LANDMARKS:
            raise ErrorDeContrato(f"se esperaban {N_LANDMARKS} landmarks, llegaron {len(puntos)}")
        for indice, punto in enumerate(puntos):
            if len(punto) != N_DIMS:
                raise ErrorDeContrato(
                    f"el landmark {indice} tiene {len(punto)} coordenadas, se esperaban {N_DIMS}"
                )
        object.__setattr__(self, "lm", puntos)
