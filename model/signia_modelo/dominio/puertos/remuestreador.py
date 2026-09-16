"""⏱️ Puerto del remuestreo temporal: que frames forman la ventana fija."""

from __future__ import annotations

from typing import Protocol, Sequence, runtime_checkable


@runtime_checkable
class Remuestreador(Protocol):
    """Decide que frames de la grabacion componen la ventana de longitud fija.

    Es la unica pieza del preprocesado que se escribe dos veces (Python y JS);
    por eso esta detras de una interfaz y se somete a un test de conformidad.
    """

    def indices(self, n_frames: int, destino: int) -> Sequence[int]:
        """Indices (0-based) de los `destino` frames elegidos entre `n_frames`."""
        ...
