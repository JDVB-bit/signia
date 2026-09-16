"""Entidades del dominio: lo que es una muestra, un frame y una mano.

Python puro y sin dependencias externas (ni numpy, ni torch, ni pydantic).
Las entidades son **inmutables** y se validan a si mismas al construirse: si
existe una instancia, cumple el contrato. Eso permite que las capas de arriba
no vuelvan a comprobar lo mismo.

Los landmarks se guardan **crudos**, tal como los devuelve MediaPipe. Ninguna
normalizacion vive aqui (principio 1 del plan).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .contrato import N_DIMS, N_LANDMARKS, SCHEMA, TIPO_AISLADA, TIPO_FRASE
from .errores import ErrorDeContrato


class Lado(str, Enum):
    """Mano real del usuario, derivada del `handedness` de MediaPipe.

    Cuidado: el video se muestra espejado en pantalla; `Lado` se refiere a la
    mano real, no a la que aparece a la izquierda de la imagen.
    """

    IZQUIERDA = "izquierda"
    DERECHA = "derecha"

    @classmethod
    def desde_texto(cls, valor: str) -> "Lado":
        try:
            return cls(valor)
        except ValueError as exc:
            validos = ", ".join(l.value for l in cls)
            raise ErrorDeContrato(
                f"lado invalido: {valor!r} (validos: {validos})"
            ) from exc


Punto = tuple[float, float, float]


@dataclass(frozen=True, slots=True)
class Mano:
    """Una mano detectada en un frame: 21 landmarks crudos."""

    lado: Lado
    score: float
    lm: tuple[Punto, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.lado, Lado):
            object.__setattr__(self, "lado", Lado.desde_texto(str(self.lado)))
        if not 0.0 <= self.score <= 1.0:
            raise ErrorDeContrato(f"score fuera de [0, 1]: {self.score}")
        puntos = tuple(tuple(float(c) for c in p) for p in self.lm)
        if len(puntos) != N_LANDMARKS:
            raise ErrorDeContrato(
                f"se esperaban {N_LANDMARKS} landmarks, llegaron {len(puntos)}"
            )
        for i, punto in enumerate(puntos):
            if len(punto) != N_DIMS:
                raise ErrorDeContrato(
                    f"el landmark {i} tiene {len(punto)} coordenadas, "
                    f"se esperaban {N_DIMS}"
                )
        object.__setattr__(self, "lm", puntos)


@dataclass(frozen=True, slots=True)
class Frame:
    """Un instante de la grabacion: 0, 1 o 2 manos.

    La ausencia de mano es informacion y no se rellena con ceros aqui; el
    relleno solo ocurre al construir el tensor (capa de aplicacion).
    """

    t: int
    manos: tuple[Mano, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "manos", tuple(self.manos))
        if self.t < 0:
            raise ErrorDeContrato(f"t negativo: {self.t}")

    def mano(self, lado: Lado) -> Mano | None:
        """Mano de ese lado, o `None` si no la hay.

        MediaPipe puede reportar dos manos con el mismo `handedness` (falso
        positivo). La regla, deterministica y unica en todo el proyecto: gana
        la de mayor `score`; a igualdad, la primera en aparecer.
        """
        candidatas = [m for m in self.manos if m.lado is lado]
        if not candidatas:
            return None
        return max(candidatas, key=lambda m: m.score)


@dataclass(frozen=True, slots=True)
class Muestra:
    """Secuencia de frames crudos grabada de una vez.

    Base comun de `MuestraAislada` (unidad de ENTRENAMIENTO) y `MuestraFrase`
    (conjunto de EVALUACION). El preprocesado solo necesita esta parte: por eso
    trabaja sobre `Muestra` y no sobre las subclases.
    """

    frames: tuple[Frame, ...]
    sesion: str
    fps_aprox: float | None = None
    schema: int = SCHEMA

    def __post_init__(self) -> None:
        object.__setattr__(self, "frames", tuple(self.frames))
        if self.schema != SCHEMA:
            raise ErrorDeContrato(
                f"schema {self.schema} no soportado (esperado {SCHEMA})"
            )
        if not self.frames:
            raise ErrorDeContrato("una muestra necesita al menos un frame")
        if not self.sesion:
            raise ErrorDeContrato("la muestra necesita una sesion identificada")
        if self.fps_aprox is not None and self.fps_aprox <= 0:
            raise ErrorDeContrato(f"fps_aprox invalido: {self.fps_aprox}")

    @property
    def tipo(self) -> str:  # pragma: no cover - lo redefinen las subclases
        raise NotImplementedError

    @property
    def n_frames(self) -> int:
        return len(self.frames)

    @property
    def glosas(self) -> tuple[str, ...]:
        """Etiquetas de la muestra, siempre como secuencia.

        Permite tratar aisladas y frases con el mismo codigo (LSP) sin
        preguntar por el tipo.
        """
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class MuestraAislada(Muestra):
    """Una sola sena. **Es la unica unidad de entrenamiento** (principio 6)."""

    etiqueta: str = ""

    def __post_init__(self) -> None:
        super().__post_init__()
        if not self.etiqueta:
            raise ErrorDeContrato("una muestra aislada necesita etiqueta")

    @property
    def tipo(self) -> str:
        return TIPO_AISLADA

    @property
    def glosas(self) -> tuple[str, ...]:
        return (self.etiqueta,)


@dataclass(frozen=True, slots=True)
class MuestraFrase(Muestra):
    """Varias senas seguidas. **Nunca entrena**: mide WER y calibra umbrales."""

    etiquetas: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        super().__post_init__()
        object.__setattr__(self, "etiquetas", tuple(self.etiquetas))
        if not self.etiquetas:
            raise ErrorDeContrato("una frase necesita su secuencia de etiquetas")
        if any(not e for e in self.etiquetas):
            raise ErrorDeContrato("hay una etiqueta vacia en la frase")

    @property
    def tipo(self) -> str:
        return TIPO_FRASE

    @property
    def glosas(self) -> tuple[str, ...]:
        return self.etiquetas
