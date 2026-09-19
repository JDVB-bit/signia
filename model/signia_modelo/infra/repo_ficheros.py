"""🗂️ Repositorio del dataset crudo sobre el sistema de ficheros.

Implementa los puertos `LectorMuestras` / `EscritorMuestras` del dominio. Es la
unica pieza que sabe que existen carpetas: cambiar disco por GCS es escribir
otro adaptador, sin tocar dominio ni aplicacion.

Distribucion en disco (ver plan, Fase 2):

    <raiz>/crudo/aisladas/<etiqueta>/<sesion>-<n>.json
    <raiz>/crudo/frases/<sesion>-<n>.json
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterator

from ..dominio.contrato import TIPO_AISLADA, TIPO_FRASE
from ..dominio.entidades import Muestra
from ..dominio.errores import ErrorDeContrato
from .configuracion_datos import raiz_de_datos
from .ficheros_json import cargar_muestra, guardar_muestra
from .nombres_de_ruta import sanear

#: Subcarpetas del dataset crudo.
CARPETA_CRUDO = "crudo"
CARPETA_AISLADAS = "aisladas"
CARPETA_FRASES = "frases"

#: Extension y numero de digitos del consecutivo de cada fichero.
EXTENSION = ".json"
DIGITOS_CONSECUTIVO = 4


class RepositorioMuestrasEnDisco:
    """Dataset crudo en carpetas. Implementa `RepositorioMuestras`."""

    def __init__(self, raiz: Path | str | None = None) -> None:
        self.raiz = raiz_de_datos(raiz)

    # --- 📁 Rutas ---------------------------------------------------------------

    @property
    def _crudo(self) -> Path:
        return self.raiz / CARPETA_CRUDO

    def carpeta_de(self, tipo: str, etiqueta: str | None = None) -> Path:
        """Carpeta donde se guarda una muestra de ese tipo (y etiqueta)."""
        if tipo == TIPO_FRASE:
            return self._crudo / CARPETA_FRASES
        if tipo == TIPO_AISLADA:
            if not etiqueta:
                raise ErrorDeContrato("las aisladas se agrupan por etiqueta")
            return self._crudo / CARPETA_AISLADAS / sanear(etiqueta)
        raise ErrorDeContrato(f"tipo de muestra desconocido: {tipo!r}")

    # --- ✍️ Puerto de escritura -------------------------------------------------

    def guardar(self, muestra: Muestra) -> str:
        """Guarda la muestra y devuelve su identificador (nombre sin extension)."""
        etiqueta = muestra.glosas[0] if muestra.tipo == TIPO_AISLADA else None
        carpeta = self.carpeta_de(muestra.tipo, etiqueta)
        carpeta.mkdir(parents=True, exist_ok=True)

        prefijo = sanear(muestra.sesion)
        consecutivo = len(list(carpeta.glob(f"{prefijo}-*{EXTENSION}")))
        # Si se borro algun fichero intermedio, el conteo choca: se avanza hasta un hueco libre
        while (carpeta / self._nombre(prefijo, consecutivo)).exists():
            consecutivo += 1

        nombre = self._nombre(prefijo, consecutivo)
        guardar_muestra(carpeta / nombre, muestra)
        return Path(nombre).stem

    @staticmethod
    def _nombre(prefijo: str, consecutivo: int) -> str:
        return f"{prefijo}-{consecutivo:0{DIGITOS_CONSECUTIVO}d}{EXTENSION}"

    # --- 📖 Puerto de lectura ---------------------------------------------------

    def listar(self, *, tipo: str | None = None, etiqueta: str | None = None) -> Iterator[Muestra]:
        """Recorre el dataset en orden estable (alfabetico por ruta)."""
        for ruta in self.rutas(tipo=tipo, etiqueta=etiqueta):
            yield cargar_muestra(ruta)

    def rutas(self, *, tipo: str | None = None, etiqueta: str | None = None) -> list[Path]:
        """Rutas de las muestras que cumplen el filtro, ordenadas."""
        # Una etiqueta nombra una clase de aisladas: las frases no tienen carpeta
        # por etiqueta, asi que pedir una etiqueta acota tambien el tipo
        if etiqueta and tipo is None:
            tipo = TIPO_AISLADA

        carpetas: list[Path] = []
        if tipo in (None, TIPO_AISLADA):
            base = self._crudo / CARPETA_AISLADAS
            if etiqueta:
                carpetas.append(base / sanear(etiqueta))
            elif base.is_dir():
                carpetas.extend(sorted(p for p in base.iterdir() if p.is_dir()))
        if tipo in (None, TIPO_FRASE):
            carpetas.append(self._crudo / CARPETA_FRASES)

        rutas: list[Path] = []
        for carpeta in carpetas:
            if carpeta.is_dir():
                rutas.extend(sorted(carpeta.glob(f"*{EXTENSION}")))
        return rutas

    def etiquetas(self) -> list[str]:
        """Etiquetas presentes en el dataset, en orden alfabetico.

        `n_clases` sale de aqui: **nunca se escribe en el codigo** (plan,
        seccion "Escalar a n senas").
        """
        base = self._crudo / CARPETA_AISLADAS
        if not base.is_dir():
            return []
        return sorted(p.name for p in base.iterdir() if p.is_dir())

    def contar(self) -> dict[str, int]:
        """Muestras por etiqueta. Insumo de `inspeccionar.py` (Fase 2)."""
        return {
            etiqueta: len(self.rutas(tipo=TIPO_AISLADA, etiqueta=etiqueta))
            for etiqueta in self.etiquetas()
        }
