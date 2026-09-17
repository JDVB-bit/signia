"""🩺 Contrasta el resumen del dataset con los criterios de la Fase 2.

Devuelve **codigos**, no frases: el texto lo pone la presentacion
(`infra/informe_de_dataset.py`), igual que en el front. Asi el mismo
diagnostico sirve para un informe por consola, para un endpoint del backend o
para un CI, sin reescribir la regla.

Cada criterio es una funcion propia. Anadir uno nuevo es anadir una funcion a
`REVISIONES`, sin tocar las demas (OCP).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Iterable

from ...dominio.criterios_dataset import (
    FACTOR_MINIMO_DE_REPOSO,
    FRACCION_MINIMA_DE_SECUENCIAS_DISTINTAS,
    FRAMES_MINIMOS_POR_MUESTRA,
    FRASES_MINIMAS,
    GLOSAS_MINIMAS_POR_FRASE,
    MUESTRAS_MINIMAS_POR_CLASE,
    PROPORCION_MINIMA_DE_FRAMES_CON_MANO,
    SESIONES_MINIMAS,
)
from ...dominio.reposo import ETIQUETA_REPOSO, es_reposo
from .resumen_del_dataset import ResumenDeClase, ResumenDelDataset

#: Sujeto de los avisos que hablan del dataset completo y no de una clase.
SUJETO_DATASET = "dataset"

#: Sujeto de los avisos sobre el conjunto de frases.
SUJETO_FRASES = "frases"


class Gravedad(str, Enum):
    """Si el aviso impide dar la Fase 2 por hecha o solo pide una mirada."""

    BLOQUEA = "bloquea"
    ATENCION = "atencion"


class CodigoDeAviso(str, Enum):
    """Todo lo que el inspector sabe detectar. El texto lo pone la infra."""

    DATASET_VACIO = "dataset-vacio"
    SIN_REPOSO = "sin-reposo"
    CLASE_CON_POCAS_MUESTRAS = "clase-con-pocas-muestras"
    REPOSO_NO_SOBRERREPRESENTADO = "reposo-no-sobrerrepresentado"
    POCAS_SESIONES = "pocas-sesiones"
    CLASE_DE_UNA_SOLA_SESION = "clase-de-una-sola-sesion"
    MUESTRA_DEMASIADO_CORTA = "muestra-demasiado-corta"
    MUESTRA_CON_POCA_MANO = "muestra-con-poca-mano"
    POCAS_FRASES = "pocas-frases"
    FRASES_POCO_VARIADAS = "frases-poco-variadas"
    FRASE_DEMASIADO_CORTA = "frase-demasiado-corta"
    GLOSA_DE_FRASE_SIN_CLASE = "glosa-de-frase-sin-clase"
    CLASE_SIN_FRASES = "clase-sin-frases"


@dataclass(frozen=True, slots=True)
class Aviso:
    """Un problema detectado, con el numero que lo delata y el exigido."""

    codigo: CodigoDeAviso
    gravedad: Gravedad
    sujeto: str
    medido: float | None = None
    exigido: float | None = None


def identificador(clase: ResumenDeClase, posicion: int) -> str:
    """Nombre con el que se senala una muestra concreta de una clase.

    `posicion` es 0-based; se muestra 1-based porque coincide con el orden
    alfabetico de los ficheros de esa carpeta, que es como se van a buscar.
    """
    return f"{clase.etiqueta} #{posicion + 1}"


# --- 🔬 Un criterio por funcion -------------------------------------------------


def _dataset_vacio(resumen: ResumenDelDataset) -> Iterable[Aviso]:
    if resumen.esta_vacio:
        yield Aviso(CodigoDeAviso.DATASET_VACIO, Gravedad.BLOQUEA, SUJETO_DATASET)


def _muestras_por_clase(resumen: ResumenDelDataset) -> Iterable[Aviso]:
    for clase in resumen.clases:
        if clase.n_muestras < MUESTRAS_MINIMAS_POR_CLASE:
            yield Aviso(
                CodigoDeAviso.CLASE_CON_POCAS_MUESTRAS,
                Gravedad.BLOQUEA,
                clase.etiqueta,
                clase.n_muestras,
                MUESTRAS_MINIMAS_POR_CLASE,
            )


def _reposo(resumen: ResumenDelDataset) -> Iterable[Aviso]:
    """`reposo` es el segmentador: sin el no hay modo continuo (Fase 2b)."""
    if resumen.esta_vacio:
        return
    reposo = resumen.clase(ETIQUETA_REPOSO)
    if reposo is None:
        yield Aviso(CodigoDeAviso.SIN_REPOSO, Gravedad.BLOQUEA, ETIQUETA_REPOSO)
        return

    otras = resumen.clases_salvo(ETIQUETA_REPOSO)
    if not otras:
        return
    # Se compara con la clase mas grande, no con la media: con la media, una
    # clase muy poblada podria seguir teniendo mas muestras que el separador
    mayor = max(clase.n_muestras for clase in otras)
    exigido = mayor * FACTOR_MINIMO_DE_REPOSO
    if reposo.n_muestras < exigido:
        yield Aviso(
            CodigoDeAviso.REPOSO_NO_SOBRERREPRESENTADO,
            Gravedad.BLOQUEA,
            ETIQUETA_REPOSO,
            reposo.n_muestras,
            exigido,
        )


def _variedad_de_sesiones(resumen: ResumenDelDataset) -> Iterable[Aviso]:
    """Un dataset de una sola sesion produce un modelo de una sola tarde."""
    if resumen.esta_vacio:
        return
    if len(resumen.sesiones) < SESIONES_MINIMAS:
        yield Aviso(
            CodigoDeAviso.POCAS_SESIONES,
            Gravedad.BLOQUEA,
            SUJETO_DATASET,
            len(resumen.sesiones),
            SESIONES_MINIMAS,
        )
    for clase in resumen.clases:
        if len(clase.sesiones) < SESIONES_MINIMAS:
            yield Aviso(
                CodigoDeAviso.CLASE_DE_UNA_SOLA_SESION,
                Gravedad.ATENCION,
                clase.etiqueta,
                len(clase.sesiones),
                SESIONES_MINIMAS,
            )


def _calidad_de_cada_muestra(resumen: ResumenDelDataset) -> Iterable[Aviso]:
    for clase in resumen.clases:
        for posicion, medida in enumerate(clase.medidas):
            sujeto = identificador(clase, posicion)
            metricas = medida.metricas
            if metricas.n_frames < FRAMES_MINIMOS_POR_MUESTRA:
                yield Aviso(
                    CodigoDeAviso.MUESTRA_DEMASIADO_CORTA,
                    Gravedad.ATENCION,
                    sujeto,
                    metricas.n_frames,
                    FRAMES_MINIMOS_POR_MUESTRA,
                )
            # En `reposo` las manos bajadas son dato bueno, no un fallo de deteccion
            if es_reposo(clase.etiqueta):
                continue
            if metricas.proporcion_con_mano < PROPORCION_MINIMA_DE_FRAMES_CON_MANO:
                yield Aviso(
                    CodigoDeAviso.MUESTRA_CON_POCA_MANO,
                    Gravedad.ATENCION,
                    sujeto,
                    metricas.proporcion_con_mano,
                    PROPORCION_MINIMA_DE_FRAMES_CON_MANO,
                )


def _cantidad_de_frases(resumen: ResumenDelDataset) -> Iterable[Aviso]:
    """Sin frases no hay WER, y sin WER no se sabe si el sistema traduce."""
    frases = resumen.frases
    if frases.n_frases < FRASES_MINIMAS:
        yield Aviso(
            CodigoDeAviso.POCAS_FRASES,
            Gravedad.BLOQUEA,
            SUJETO_FRASES,
            frases.n_frases,
            FRASES_MINIMAS,
        )


def _variedad_de_frases(resumen: ResumenDelDataset) -> Iterable[Aviso]:
    """Veinte veces la misma frase no mide la segmentacion."""
    frases = resumen.frases
    if not frases.n_frases:
        return
    exigidas = frases.n_frases * FRACCION_MINIMA_DE_SECUENCIAS_DISTINTAS
    if frases.ordenes_distintos < exigidas:
        yield Aviso(
            CodigoDeAviso.FRASES_POCO_VARIADAS,
            Gravedad.ATENCION,
            SUJETO_FRASES,
            frases.ordenes_distintos,
            exigidas,
        )
    for posicion, secuencia in enumerate(frases.secuencias):
        if len(secuencia) < GLOSAS_MINIMAS_POR_FRASE:
            yield Aviso(
                CodigoDeAviso.FRASE_DEMASIADO_CORTA,
                Gravedad.ATENCION,
                f"{SUJETO_FRASES} #{posicion + 1}",
                len(secuencia),
                GLOSAS_MINIMAS_POR_FRASE,
            )


def _cobertura_entre_frases_y_clases(resumen: ResumenDelDataset) -> Iterable[Aviso]:
    """Los dos conjuntos tienen que hablar del mismo vocabulario.

    Una glosa que aparece en una frase pero no tiene clase entrenada es un
    error garantizado en el WER que no se puede achacar al modelo. Y una clase
    que no aparece en ninguna frase se entrena sin llegar a evaluarse nunca.
    """
    etiquetas = set(resumen.etiquetas)
    glosas = set(resumen.frases.glosas_usadas)
    if not resumen.frases.n_frases:
        return

    for glosa in sorted(glosas - etiquetas):
        yield Aviso(CodigoDeAviso.GLOSA_DE_FRASE_SIN_CLASE, Gravedad.BLOQUEA, glosa)
    for etiqueta in sorted(etiquetas - glosas - {ETIQUETA_REPOSO}):
        yield Aviso(CodigoDeAviso.CLASE_SIN_FRASES, Gravedad.ATENCION, etiqueta)


#: Firma de una revision: mira el resumen y va soltando avisos.
Revision = Callable[[ResumenDelDataset], Iterable[Aviso]]

#: Las revisiones, en el orden en que se reportan. Anadir un criterio es
#: anadir una funcion a esta lista, sin tocar ninguna de las existentes.
REVISIONES: tuple[Revision, ...] = (
    _dataset_vacio,
    _muestras_por_clase,
    _reposo,
    _variedad_de_sesiones,
    _calidad_de_cada_muestra,
    _cantidad_de_frases,
    _variedad_de_frases,
    _cobertura_entre_frases_y_clases,
)


#: Solo lo que se puede juzgar de una muestra por si sola. Es el alcance de
#: una vista filtrada: sobre media clase no se puede decir si falta `reposo`
#: ni si hay frases suficientes, y afirmarlo seria un falso bloqueo.
REVISIONES_DE_CADA_MUESTRA: tuple[Revision, ...] = (_calidad_de_cada_muestra,)


def diagnosticar(
    resumen: ResumenDelDataset,
    *,
    revisiones: tuple[Revision, ...] = REVISIONES,
) -> tuple[Aviso, ...]:
    """Avisos del dataset, en orden estable.

    `revisiones` se inyecta para poder acotar el alcance sin que el criterio
    cambie: quien mira una sola clase pasa `REVISIONES_DE_CADA_MUESTRA`.
    """
    return tuple(aviso for revision in revisiones for aviso in revision(resumen))


def hay_bloqueos(avisos: Iterable[Aviso]) -> bool:
    """¿Queda algo que impida dar la Fase 2 por hecha?"""
    return any(aviso.gravedad is Gravedad.BLOQUEA for aviso in avisos)
