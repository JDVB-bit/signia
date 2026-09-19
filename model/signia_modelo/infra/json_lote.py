"""📦 El sobre que envuelve varias muestras: lo que el front manda de una vez.

Formato (`schema` 1), identico en el fichero que descarga el boton *Enviar* y
en el cuerpo de `POST /muestras`:

    {"schema": 1, "muestras": [ {muestra}, {muestra}, ... ]}

Una muestra suelta se valida en `json_contrato`; aqui solo se valida **el
sobre** y se delega cada elemento. Separar las dos cosas evita que el mensaje
de error diga "muestra invalida" cuando lo que falta es el `schema` del lote.
"""

from __future__ import annotations

from typing import Any, Mapping

from ..dominio.contrato import SCHEMA
from ..dominio.entidades import Muestra
from ..dominio.errores import ErrorDeContrato
from .json_contrato import muestra_a_dict, muestra_desde_dict

#: Claves del sobre.
CLAVE_SCHEMA = "schema"
CLAVE_MUESTRAS = "muestras"


def muestras_desde_lote(datos: Any) -> list[Muestra]:
    """Valida el sobre y devuelve sus muestras como entidades.

    Los errores mencionan **la posicion** de la muestra dentro del lote: con
    40 muestras en un fichero, "muestra invalida" no serviria de nada.
    """
    if not isinstance(datos, Mapping):
        raise ErrorDeContrato("el lote debe ser un objeto JSON")

    schema = datos.get(CLAVE_SCHEMA)
    if schema != SCHEMA:
        raise ErrorDeContrato(f"schema de lote {schema!r} no soportado (esperado {SCHEMA})")

    crudas = datos.get(CLAVE_MUESTRAS)
    if not isinstance(crudas, list):
        raise ErrorDeContrato(f"falta la lista '{CLAVE_MUESTRAS}'")
    if not crudas:
        raise ErrorDeContrato("el lote no trae ninguna muestra")

    muestras: list[Muestra] = []
    for posicion, cruda in enumerate(crudas):
        try:
            muestras.append(muestra_desde_dict(cruda))
        except ErrorDeContrato as exc:
            raise ErrorDeContrato(f"muestra {posicion} del lote: {exc}") from exc
    return muestras


def lote_desde_muestras(muestras: list[Muestra]) -> dict[str, Any]:
    """Entidades -> sobre. Inverso exacto de `muestras_desde_lote`."""
    return {
        CLAVE_SCHEMA: SCHEMA,
        CLAVE_MUESTRAS: [muestra_a_dict(muestra) for muestra in muestras],
    }
