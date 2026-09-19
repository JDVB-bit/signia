"""📥 `POST /muestras` — recibe un lote grabado en Entrenamiento y lo guarda.

Es el endpoint que cierra el bucle del producto: grabar deja de producir una
descarga que alguien tiene que mover a mano.

La ruta no valida el contrato ni sabe escribir ficheros. Traduce HTTP a dos
llamadas del paquete del modelo -validar el lote y ejecutar el caso de uso- y
devuelve lo que entro. Es exactamente lo que hace `scripts/importar_lote.py`,
y por eso los dos caminos no pueden divergir.
"""

from __future__ import annotations

from fastapi import APIRouter, status
from signia_modelo.aplicacion.importacion_de_lote import importar_lote
from signia_modelo.infra.json_lote import muestras_desde_lote

from ..dominio.esquemas import LoteEntrante, RespuestaDeImportacion
from .dependencias import RepositorioInyectado

RUTA = "/muestras"

enrutador = APIRouter(tags=["muestras"])


@enrutador.post(
    RUTA,
    status_code=status.HTTP_201_CREATED,
    response_model=RespuestaDeImportacion,
    summary="Guarda un lote de muestras crudas en el dataset",
)
def recibir_lote(lote: LoteEntrante, repositorio: RepositorioInyectado):
    """Valida el lote entero y lo guarda; si algo falla, no entra nada.

    `muestras_desde_lote` levanta `ErrorDeContrato` antes de tocar el disco,
    asi que un lote con una muestra mala se rechaza completo. Media tanda
    guardada seria peor que ninguna: nadie sabria cual falta.
    """
    muestras = muestras_desde_lote(lote.como_dict())
    resultado = importar_lote(muestras, repositorio)
    return RespuestaDeImportacion(
        guardadas=resultado.n_muestras,
        identificadores=list(resultado.identificadores),
        por_etiqueta=resultado.por_etiqueta,
    )
