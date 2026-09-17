"""🧾 Convierte el resumen y los avisos del dataset en lineas de texto.

Esta es la capa de presentacion del inspector: **el unico sitio donde un codigo
de aviso se vuelve una frase en castellano**. El diagnostico devuelve codigos
justo para eso — el mismo criterio podra pintarse manana en el front o
devolverse por la API sin reescribir la regla.

Devuelve `list[str]` y no imprime: asi se puede testear sin capturar stdout y
el script decide donde va (consola, fichero, log).

Texto plano ASCII a proposito: esto se lee en la consola de Windows, donde un
emoji mal codificado rompe la ejecucion entera.
"""

from __future__ import annotations

from typing import Iterable, Sequence

from ..aplicacion.inspeccion import (
    Aviso,
    CodigoDeAviso,
    Gravedad,
    ResumenDeClase,
    ResumenDelDataset,
)

#: Que dice cada codigo de aviso, con el numero medido y el exigido.
TEXTOS_DE_AVISO: dict[CodigoDeAviso, str] = {
    CodigoDeAviso.DATASET_VACIO: (
        "No hay ninguna muestra grabada todavia."
    ),
    CodigoDeAviso.SIN_REPOSO: (
        "Falta la clase '{sujeto}': es el segmentador del modo continuo, "
        "sin ella no hay frontera entre una sena y la siguiente."
    ),
    CodigoDeAviso.CLASE_CON_POCAS_MUESTRAS: (
        "'{sujeto}' tiene {medido:.0f} muestras; hacen falta {exigido:.0f}."
    ),
    CodigoDeAviso.REPOSO_NO_SOBRERREPRESENTADO: (
        "'{sujeto}' tiene {medido:.0f} muestras y deberia tener {exigido:.0f} "
        "(el doble de la clase mas poblada): es el separador entre senas."
    ),
    CodigoDeAviso.POCAS_SESIONES: (
        "Todo el dataset sale de {medido:.0f} sesion(es); hacen falta {exigido:.0f} "
        "para que el modelo no aprenda la luz y la ropa de una sola tarde."
    ),
    CodigoDeAviso.CLASE_DE_UNA_SOLA_SESION: (
        "'{sujeto}' se grabo en {medido:.0f} sesion(es) de las {exigido:.0f} recomendadas."
    ),
    CodigoDeAviso.MUESTRA_DEMASIADO_CORTA: (
        "{sujeto} tiene {medido:.0f} frames; por debajo de {exigido:.0f} el "
        "remuestreo repite cada frame y la muestra queda casi estatica."
    ),
    CodigoDeAviso.MUESTRA_CON_POCA_MANO: (
        "{sujeto} solo tiene mano detectada en el {medido:.0%} de los frames "
        "(minimo {exigido:.0%})."
    ),
    CodigoDeAviso.POCAS_FRASES: (
        "Hay {medido:.0f} frases completas; hacen falta {exigido:.0f} para medir WER."
    ),
    CodigoDeAviso.FRASES_POCO_VARIADAS: (
        "Solo hay {medido:.0f} secuencias distintas y se esperaban {exigido:.0f}: "
        "repetir la misma frase no mide la segmentacion."
    ),
    CodigoDeAviso.FRASE_DEMASIADO_CORTA: (
        "{sujeto} tiene {medido:.0f} glosa(s); con menos de {exigido:.0f} no hay "
        "transicion entre senas que medir."
    ),
    CodigoDeAviso.GLOSA_DE_FRASE_SIN_CLASE: (
        "La glosa '{sujeto}' aparece en las frases pero no tiene clase entrenada: "
        "seria un error de WER que no es culpa del modelo."
    ),
    CodigoDeAviso.CLASE_SIN_FRASES: (
        "La clase '{sujeto}' se entrena pero no aparece en ninguna frase: "
        "nunca se llega a evaluar en continuo."
    ),
}

#: Etiqueta con la que se marca cada aviso en el informe.
MARCAS = {Gravedad.BLOQUEA: "[BLOQUEA ]", Gravedad.ATENCION: "[atencion]"}

#: Sangria de todo lo que cuelga de un titulo de seccion.
SANGRIA = "  "

#: Ancho minimo de la columna de etiquetas (crece con la etiqueta mas larga).
ANCHO_MINIMO_DE_ETIQUETA = 12

#: Cabeceras de la tabla de clases y el ancho de cada columna numerica.
COLUMNAS = (
    ("muestras", 9),
    ("sesiones", 9),
    ("frames", 8),
    ("segundos", 9),
    ("con mano", 9),
    ("2 manos", 8),
)

#: Texto de una duracion que no se puede calcular (la muestra no traia fps).
SIN_DATO = "-"

#: Nota del informe cuando se esta mirando solo una parte del dataset.
NOTA_VISTA_FILTRADA = (
    "Vista filtrada: solo se revisa la calidad de cada muestra. "
    "Para la puerta de la Fase 2, ejecutar el inspector sin --etiqueta."
)


def contar(cantidad: int, singular: str, plural: str) -> str:
    """"1 clase" / "3 clases": el informe se lee, no se parsea."""
    return f"{cantidad} {singular if cantidad == 1 else plural}"


def describir(aviso: Aviso) -> str:
    """Un aviso como frase, con su marca de gravedad delante."""
    plantilla = TEXTOS_DE_AVISO[aviso.codigo]
    cuerpo = plantilla.format(
        sujeto=aviso.sujeto,
        medido=aviso.medido if aviso.medido is not None else 0,
        exigido=aviso.exigido if aviso.exigido is not None else 0,
    )
    return f"{MARCAS[aviso.gravedad]} {cuerpo}"


def _fila_de_clase(clase: ResumenDeClase, ancho_etiqueta: int) -> str:
    """Una linea de la tabla de clases, con las columnas alineadas."""
    segundos = clase.media_de_segundos
    valores = (
        f"{clase.n_muestras}",
        f"{len(clase.sesiones)}",
        f"{clase.media_de_frames:.1f}",
        f"{segundos:.2f}" if segundos is not None else SIN_DATO,
        f"{clase.proporcion_con_mano:.0%}",
        f"{clase.muestras_bimanuales}",
    )
    celdas = "".join(valor.rjust(ancho) for valor, (_, ancho) in zip(valores, COLUMNAS))
    return f"{SANGRIA}{clase.etiqueta.ljust(ancho_etiqueta)}{celdas}"


def lineas_de_clases(resumen: ResumenDelDataset) -> list[str]:
    """Tabla de senas aisladas: lo que se va a entrenar."""
    if not resumen.clases:
        return [f"{SANGRIA}(no hay ninguna sena aislada grabada)"]

    ancho = max(ANCHO_MINIMO_DE_ETIQUETA, *(len(c.etiqueta) + 2 for c in resumen.clases))
    cabecera = "".join(nombre.rjust(ancho_columna) for nombre, ancho_columna in COLUMNAS)
    return [
        f"{SANGRIA}{'clase'.ljust(ancho)}{cabecera}",
        *[_fila_de_clase(clase, ancho) for clase in resumen.clases],
    ]


def lineas_de_frases(resumen: ResumenDelDataset) -> list[str]:
    """Estado del conjunto de evaluacion (que nunca entrena)."""
    frases = resumen.frases
    if not frases.n_frases:
        return [f"{SANGRIA}(no hay ninguna frase grabada)"]

    return [
        f"{SANGRIA}frases: {frases.n_frases}"
        f" | secuencias distintas: {frases.ordenes_distintos}"
        f" | glosas por frase: {frases.media_de_glosas:.1f}"
        f" | sesiones: {len(frases.sesiones)}",
        f"{SANGRIA}glosario usado: {', '.join(frases.glosas_usadas)}",
    ]


def lineas_de_diagnostico(avisos: Sequence[Aviso]) -> list[str]:
    """Los avisos, los que bloquean primero."""
    if not avisos:
        return [f"{SANGRIA}Sin avisos: el dataset cumple los criterios de la Fase 2."]

    ordenados = sorted(avisos, key=lambda aviso: aviso.gravedad is not Gravedad.BLOQUEA)
    return [f"{SANGRIA}{describir(aviso)}" for aviso in ordenados]


def informe(
    resumen: ResumenDelDataset,
    avisos: Iterable[Aviso],
    *,
    encabezado: str,
    nota: str | None = None,
) -> list[str]:
    """El informe completo, listo para imprimir linea a linea."""
    avisos = list(avisos)
    return [
        encabezado,
        *([nota] if nota else []),
        "",
        "Senas aisladas (entrenamiento): "
        + ", ".join(
            (
                contar(resumen.n_clases, "clase", "clases"),
                contar(resumen.n_muestras, "muestra", "muestras"),
                contar(len(resumen.sesiones), "sesion", "sesiones"),
            )
        ),
        *lineas_de_clases(resumen),
        "",
        "Frases completas (evaluacion, nunca entrenan)",
        *lineas_de_frases(resumen),
        "",
        f"Diagnostico ({contar(len(avisos), 'aviso', 'avisos')})",
        *lineas_de_diagnostico(avisos),
    ]
