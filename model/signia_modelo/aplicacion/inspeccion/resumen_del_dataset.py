"""📊 El dataset entero, agregado por clase y por tipo de muestra.

Recibe muestras ya validadas y devuelve numeros. **No juzga**: aqui no hay
ningun umbral. Los criterios viven en `dominio/criterios_dataset.py` y los
aplica `diagnostico_del_dataset`, para poder subirlos sin tocar el recuento.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from ...dominio.contrato import TIPO_AISLADA, TIPO_FRASE
from ...dominio.entidades import Muestra
from ...dominio.errores import ErrorDeContrato
from ...dominio.etiquetas import normalizar_etiqueta
from .metricas_de_muestra import MetricasDeMuestra, medir


@dataclass(frozen=True, slots=True)
class MuestraMedida:
    """Una muestra reducida a lo que el resumen necesita: origen y medidas."""

    sesion: str
    metricas: MetricasDeMuestra


@dataclass(frozen=True, slots=True)
class ResumenDeClase:
    """Todas las muestras de una sena, en el orden en que se leyeron.

    Guarda las medidas una por una en vez de solo los promedios: el
    diagnostico necesita senalar *que* muestra esta mal, no solo que la media
    se desvio.
    """

    etiqueta: str
    medidas: tuple[MuestraMedida, ...]

    @property
    def n_muestras(self) -> int:
        return len(self.medidas)

    @property
    def sesiones(self) -> tuple[str, ...]:
        """Sesiones distintas que contribuyeron a esta clase, ordenadas."""
        return tuple(sorted({medida.sesion for medida in self.medidas}))

    @property
    def media_de_frames(self) -> float:
        return _media([medida.metricas.n_frames for medida in self.medidas])

    @property
    def media_de_segundos(self) -> float | None:
        """Duracion media, o `None` si ninguna muestra reporto fps."""
        duraciones = [
            medida.metricas.segundos
            for medida in self.medidas
            if medida.metricas.segundos is not None
        ]
        return _media(duraciones) if duraciones else None

    @property
    def proporcion_con_mano(self) -> float:
        """Frames con mano sobre frames totales, en toda la clase."""
        con_mano = sum(medida.metricas.frames_con_alguna_mano for medida in self.medidas)
        totales = sum(medida.metricas.n_frames for medida in self.medidas)
        return con_mano / totales if totales else 0.0

    @property
    def muestras_bimanuales(self) -> int:
        """Cuantas muestras se hacen mayoritariamente con las dos manos."""
        return sum(1 for medida in self.medidas if medida.metricas.usa_las_dos_manos)


@dataclass(frozen=True, slots=True)
class ResumenDeFrases:
    """El conjunto de evaluacion: frases seguidas con su secuencia de glosas."""

    medidas: tuple[MuestraMedida, ...]
    secuencias: tuple[tuple[str, ...], ...]

    @property
    def n_frases(self) -> int:
        return len(self.medidas)

    @property
    def sesiones(self) -> tuple[str, ...]:
        return tuple(sorted({medida.sesion for medida in self.medidas}))

    @property
    def glosas_usadas(self) -> tuple[str, ...]:
        """Vocabulario que aparece en las frases, ordenado."""
        return tuple(sorted({glosa for secuencia in self.secuencias for glosa in secuencia}))

    @property
    def ordenes_distintos(self) -> int:
        """Secuencias distintas. Veinte veces la misma frase no mide nada."""
        return len(set(self.secuencias))

    @property
    def media_de_glosas(self) -> float:
        return _media([len(secuencia) for secuencia in self.secuencias])


@dataclass(frozen=True, slots=True)
class ResumenDelDataset:
    """Lo aislado (entrenamiento) y lo corrido (evaluacion), por separado."""

    clases: tuple[ResumenDeClase, ...]
    frases: ResumenDeFrases

    @property
    def etiquetas(self) -> tuple[str, ...]:
        return tuple(clase.etiqueta for clase in self.clases)

    @property
    def n_clases(self) -> int:
        """Sale del dataset. **Nunca** de una constante del codigo."""
        return len(self.clases)

    @property
    def n_muestras(self) -> int:
        return sum(clase.n_muestras for clase in self.clases)

    @property
    def sesiones(self) -> tuple[str, ...]:
        """Todas las sesiones del dataset, aisladas y frases."""
        de_clases = {sesion for clase in self.clases for sesion in clase.sesiones}
        return tuple(sorted(de_clases | set(self.frases.sesiones)))

    @property
    def esta_vacio(self) -> bool:
        return not self.clases and not self.frases.n_frases

    def clase(self, etiqueta: str) -> ResumenDeClase | None:
        """Resumen de una sena concreta, o `None` si no esta en el dataset."""
        buscada = normalizar_etiqueta(etiqueta)
        return next((clase for clase in self.clases if clase.etiqueta == buscada), None)

    def clases_salvo(self, etiqueta: str) -> tuple[ResumenDeClase, ...]:
        """Las demas clases. Se usa para comparar `reposo` con el resto."""
        excluida = normalizar_etiqueta(etiqueta)
        return tuple(clase for clase in self.clases if clase.etiqueta != excluida)


def resumir(muestras: Iterable[Muestra]) -> ResumenDelDataset:
    """Agrupa las muestras por clase (aisladas) y recoge las frases aparte.

    Las aisladas se agrupan por la **etiqueta normalizada**: si alguien grabo
    "Hola" y "hola" son la misma clase, no dos con la mitad de muestras cada
    una. Las clases salen ordenadas alfabeticamente, igual que en disco, para
    que el informe sea estable entre ejecuciones.
    """
    por_etiqueta: dict[str, list[MuestraMedida]] = {}
    frases: list[MuestraMedida] = []
    secuencias: list[tuple[str, ...]] = []

    for muestra in muestras:
        medida = MuestraMedida(sesion=muestra.sesion, metricas=medir(muestra))
        if muestra.tipo == TIPO_AISLADA:
            etiqueta = normalizar_etiqueta(muestra.glosas[0])
            por_etiqueta.setdefault(etiqueta, []).append(medida)
        elif muestra.tipo == TIPO_FRASE:
            frases.append(medida)
            secuencias.append(tuple(normalizar_etiqueta(g) for g in muestra.glosas))
        else:  # pragma: no cover - el contrato solo define dos tipos
            raise ErrorDeContrato(f"tipo de muestra desconocido: {muestra.tipo!r}")

    return ResumenDelDataset(
        clases=tuple(
            ResumenDeClase(etiqueta=etiqueta, medidas=tuple(por_etiqueta[etiqueta]))
            for etiqueta in sorted(por_etiqueta)
        ),
        frases=ResumenDeFrases(medidas=tuple(frases), secuencias=tuple(secuencias)),
    )


def _media(valores: list[float] | list[int]) -> float:
    """Media aritmetica; 0.0 si no hay valores (evita el ZeroDivisionError)."""
    return sum(valores) / len(valores) if valores else 0.0
