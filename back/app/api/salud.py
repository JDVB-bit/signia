"""🩺 `GET /salud` — responde, y con que version del contrato habla.

Un backend vivo que habla otro `schema` es peor que uno caido: acepta las
muestras y las guarda mal. Por eso la version viaja aqui y el front puede
comprobarla antes de subir nada.

Tambien dice si el dataset es escribible: un permiso mal puesto o un disco
lleno tiene que aparecer aqui, no al subir la primera tanda de 40 muestras.
"""

from __future__ import annotations

from fastapi import APIRouter
from signia_modelo.dominio.contrato import SCHEMA, VERSION_PREPROCESADO
from signia_modelo.infra.configuracion_datos import raiz_de_datos

from ..dominio.esquemas import EstadoDelServicio
from ..infra.repositorio_en_disco import es_escribible
from .dependencias import AjustesInyectados

RUTA = "/salud"

#: Valor de `estado` cuando el servicio responde.
ESTADO_OK = "ok"

enrutador = APIRouter(tags=["salud"])


@enrutador.get(RUTA, response_model=EstadoDelServicio, summary="Estado y version del contrato")
def salud(configuracion: AjustesInyectados):
    """Estado del servicio, version del contrato y si el dataset se puede escribir."""
    return EstadoDelServicio(
        estado=ESTADO_OK,
        schema_de_datos=SCHEMA,
        version_preprocesado=VERSION_PREPROCESADO,
        dataset_escribible=es_escribible(raiz_de_datos(configuracion.datos_dir)),
    )
