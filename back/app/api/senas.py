"""🔤 `GET /senas` — el vocabulario que hay grabado ahora mismo.

Sirve para dos cosas: confirmar desde el front que la subida llego, y saber
que clases existen sin tener que abrir el disco. `n_clases` se cuenta aqui,
nunca se escribe en el codigo (plan, "Escalar a n senas").
"""

from __future__ import annotations

from fastapi import APIRouter

from ..dominio.esquemas import SenaDelVocabulario, VocabularioDelDataset
from .dependencias import RepositorioInyectado

RUTA = "/senas"

enrutador = APIRouter(tags=["senas"])


@enrutador.get(RUTA, response_model=VocabularioDelDataset, summary="Vocabulario del dataset")
def listar_senas(repositorio: RepositorioInyectado):
    """Cada sena grabada y cuantas muestras tiene, en orden alfabetico."""
    conteo = repositorio.contar()
    return VocabularioDelDataset(
        n_clases=len(conteo),
        senas=[
            SenaDelVocabulario(etiqueta=etiqueta, muestras=muestras)
            for etiqueta, muestras in conteo.items()
        ],
    )
