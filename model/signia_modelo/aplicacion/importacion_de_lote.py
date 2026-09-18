"""📥 Caso de uso: meter un lote de muestras en el dataset.

Es el paso que faltaba entre el front y el entrenamiento: grabar produce un
lote, y el dataset espera una muestra por fichero. Aqui vive esa traduccion,
**una sola vez**, para que el script de linea de comandos y el endpoint
`POST /muestras` del backend hagan exactamente lo mismo.

Depende del puerto `EscritorMuestras`, no del disco: el dia que el dataset viva
en almacenamiento de objetos, este modulo no cambia (DIP).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from ..dominio.entidades import Muestra
from ..dominio.etiquetas import normalizar_etiqueta
from ..dominio.puertos import EscritorMuestras


@dataclass(frozen=True, slots=True)
class ResultadoDeImportacion:
    """Que se guardo, para poder informar de ello sin volver a leer el disco."""

    identificadores: tuple[str, ...]
    glosas: tuple[tuple[str, ...], ...]

    @property
    def n_muestras(self) -> int:
        return len(self.identificadores)

    @property
    def por_etiqueta(self) -> dict[str, int]:
        """Cuantas muestras entraron de cada clase, en orden alfabetico.

        Una frase aporta a **todas** sus glosas: es lo que permite ver de un
        vistazo que el lote traia lo que se pretendia grabar.
        """
        conteo: dict[str, int] = {}
        for secuencia in self.glosas:
            for glosa in secuencia:
                conteo[glosa] = conteo.get(glosa, 0) + 1
        return dict(sorted(conteo.items()))


def importar_lote(
    muestras: Sequence[Muestra],
    escritor: EscritorMuestras,
) -> ResultadoDeImportacion:
    """Guarda las muestras en el orden recibido y devuelve lo que entro.

    No valida nada: las entidades ya se validaron al construirse (si existe la
    instancia, cumple el contrato). Tampoco descarta duplicados — dos
    grabaciones de la misma sena en la misma sesion son dato legitimo, y el
    repositorio les da identificadores distintos.
    """
    identificadores = []
    glosas = []
    for muestra in muestras:
        identificadores.append(escritor.guardar(muestra))
        glosas.append(tuple(normalizar_etiqueta(glosa) for glosa in muestra.glosas))

    return ResultadoDeImportacion(
        identificadores=tuple(identificadores),
        glosas=tuple(glosas),
    )
