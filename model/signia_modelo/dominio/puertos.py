"""Puertos (interfaces) del dominio.

Son `Protocol`: quien los implementa no necesita heredar de nada, y el dominio
no depende de ninguna implementacion concreta (DIP). Se mantienen pequenos a
proposito (ISP): quien solo lee muestras no arrastra la firma de guardarlas.
"""

from __future__ import annotations

from typing import Iterator, Protocol, Sequence, runtime_checkable

from .entidades import Muestra


@runtime_checkable
class Remuestreador(Protocol):
    """Decide que frames de la grabacion componen la ventana de longitud fija.

    Es la unica pieza del preprocesado que se escribe dos veces (Python y JS);
    por eso esta detras de una interfaz y se somete a un test de conformidad.
    """

    def indices(self, n_frames: int, destino: int) -> Sequence[int]:
        """Indices (0-based) de los `destino` frames elegidos entre `n_frames`."""
        ...


@runtime_checkable
class LectorMuestras(Protocol):
    """Lectura del dataset crudo, sin saber donde vive."""

    def listar(
        self, *, tipo: str | None = None, etiqueta: str | None = None
    ) -> Iterator[Muestra]:
        ...


@runtime_checkable
class EscritorMuestras(Protocol):
    """Escritura del dataset crudo, sin saber donde vive."""

    def guardar(self, muestra: Muestra) -> str:
        """Persiste la muestra y devuelve su identificador estable."""
        ...


@runtime_checkable
class RepositorioMuestras(LectorMuestras, EscritorMuestras, Protocol):
    """Puerto completo, para quien necesita las dos mitades."""
