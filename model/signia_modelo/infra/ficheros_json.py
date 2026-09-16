"""💾 Lectura y escritura de una muestra del contrato en un fichero `.json`."""

from __future__ import annotations

import json
from pathlib import Path

from ..dominio.entidades import Muestra
from ..dominio.errores import ErrorDeContrato
from .json_contrato import muestra_a_dict, muestra_desde_dict

#: Codificacion de los ficheros del dataset (las etiquetas pueden llevar tildes).
CODIFICACION = "utf-8"


def cargar_muestra(ruta: Path | str) -> Muestra:
    """Lee y valida la muestra de `ruta`; los errores mencionan el fichero."""
    ruta = Path(ruta)
    with ruta.open("r", encoding=CODIFICACION) as fichero:
        try:
            crudo = json.load(fichero)
        except json.JSONDecodeError as exc:
            raise ErrorDeContrato(f"{ruta}: JSON invalido ({exc})") from exc
    try:
        return muestra_desde_dict(crudo)
    except ErrorDeContrato as exc:
        raise ErrorDeContrato(f"{ruta}: {exc}") from exc


def guardar_muestra(ruta: Path | str, muestra: Muestra) -> None:
    """Escribe la muestra en `ruta`, creando las carpetas que falten."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding=CODIFICACION) as fichero:
        json.dump(muestra_a_dict(muestra), fichero, ensure_ascii=False)
