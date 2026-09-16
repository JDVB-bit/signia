"""Repositorio del dataset crudo sobre el sistema de ficheros.

Implementa los puertos `LectorMuestras` / `EscritorMuestras` del dominio. Es la
unica pieza que sabe que existen carpetas y rutas: cambiar disco por GCS es
escribir otro adaptador, sin tocar dominio ni aplicacion.

Distribucion en disco (ver plan, Fase 2):

    <raiz>/crudo/aisladas/<etiqueta>/<sesion>-<n>.json
    <raiz>/crudo/frases/<sesion>-<n>.json
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Iterator

from ..dominio.contrato import TIPO_AISLADA, TIPO_FRASE
from ..dominio.entidades import Muestra
from ..dominio.errores import ErrorDeContrato
from .json_contrato import cargar_muestra, guardar_muestra

#: Solo estos caracteres pasan a formar parte de una ruta.
_SEGURO = re.compile(r"[^a-zA-Z0-9_-]+")

#: Variable de entorno con la raiz de datos (default local, ver plan).
ENV_DATOS_DIR = "DATOS_DIR"
RAIZ_POR_DEFECTO = Path("data")


def sanear(texto: str) -> str:
    """Convierte una etiqueta o sesion en un segmento de ruta seguro.

    Cierra el paso a `../` y a separadores: la etiqueta viene del usuario y
    acaba siendo un nombre de carpeta.
    """
    limpio = _SEGURO.sub("_", texto.strip().lower()).strip("_")
    if not limpio:
        raise ErrorDeContrato(f"nombre no utilizable como ruta: {texto!r}")
    return limpio


class RepositorioMuestrasEnDisco:
    """Dataset crudo en carpetas. Implementa `RepositorioMuestras`."""

    def __init__(self, raiz: Path | str | None = None) -> None:
        if raiz is None:
            raiz = os.environ.get(ENV_DATOS_DIR, RAIZ_POR_DEFECTO)
        self.raiz = Path(raiz)

    # -- rutas -----------------------------------------------------------
    @property
    def _crudo(self) -> Path:
        return self.raiz / "crudo"

    def carpeta_de(self, tipo: str, etiqueta: str | None = None) -> Path:
        if tipo == TIPO_FRASE:
            return self._crudo / "frases"
        if tipo == TIPO_AISLADA:
            if not etiqueta:
                raise ErrorDeContrato("las aisladas se agrupan por etiqueta")
            return self._crudo / "aisladas" / sanear(etiqueta)
        raise ErrorDeContrato(f"tipo de muestra desconocido: {tipo!r}")

    # -- puerto de escritura ---------------------------------------------
    def guardar(self, muestra: Muestra) -> str:
        """Guarda la muestra y devuelve su identificador (nombre sin extension)."""
        etiqueta = muestra.glosas[0] if muestra.tipo == TIPO_AISLADA else None
        carpeta = self.carpeta_de(muestra.tipo, etiqueta)
        carpeta.mkdir(parents=True, exist_ok=True)

        prefijo = sanear(muestra.sesion)
        n = len(list(carpeta.glob(f"{prefijo}-*.json")))
        while (carpeta / f"{prefijo}-{n:04d}.json").exists():
            n += 1

        identificador = f"{prefijo}-{n:04d}"
        guardar_muestra(carpeta / f"{identificador}.json", muestra)
        return identificador

    # -- puerto de lectura -----------------------------------------------
    def listar(
        self, *, tipo: str | None = None, etiqueta: str | None = None
    ) -> Iterator[Muestra]:
        """Recorre el dataset en orden estable (alfabetico por ruta)."""
        for ruta in self.rutas(tipo=tipo, etiqueta=etiqueta):
            yield cargar_muestra(ruta)

    def rutas(
        self, *, tipo: str | None = None, etiqueta: str | None = None
    ) -> list[Path]:
        carpetas: list[Path] = []
        if tipo in (None, TIPO_AISLADA):
            base = self._crudo / "aisladas"
            if etiqueta:
                carpetas.append(base / sanear(etiqueta))
            elif base.is_dir():
                carpetas.extend(sorted(p for p in base.iterdir() if p.is_dir()))
        if tipo in (None, TIPO_FRASE):
            carpetas.append(self._crudo / "frases")

        rutas: list[Path] = []
        for carpeta in carpetas:
            if carpeta.is_dir():
                rutas.extend(sorted(carpeta.glob("*.json")))
        return rutas

    def etiquetas(self) -> list[str]:
        """Etiquetas presentes en el dataset, en orden alfabetico.

        `n_clases` sale de aqui: **nunca se escribe en el codigo** (plan,
        seccion "Escalar a n senas").
        """
        base = self._crudo / "aisladas"
        if not base.is_dir():
            return []
        return sorted(p.name for p in base.iterdir() if p.is_dir())

    def contar(self) -> dict[str, int]:
        """Muestras por etiqueta. Insumo de `inspeccionar.py` (Fase 2)."""
        return {
            etiqueta: len(self.rutas(tipo=TIPO_AISLADA, etiqueta=etiqueta))
            for etiqueta in self.etiquetas()
        }
