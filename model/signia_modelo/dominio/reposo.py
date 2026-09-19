"""😴 La etiqueta `reposo`: la unica glosa que el codigo conoce por su nombre.

El vocabulario sale del dataset y `n_clases` nunca se escribe en el codigo
(plan, seccion "Escalar a n senas"). `reposo` es la excepcion deliberada: en
modo continuo **no es una clase mas, es el segmentador** — lo que marca la
frontera entre una sena y la siguiente. Por eso el diagnostico del dataset
tiene que poder preguntar por ella, y por eso necesita mas muestras que las
demas (plan, Fase 2b).
"""

from typing import Final

from .etiquetas import normalizar_etiqueta

#: Glosa de la clase que separa senas. En minusculas, como todas: "Reposo" y
#: "reposo" son la misma clase (ver `etiquetas.normalizar_etiqueta`).
ETIQUETA_REPOSO: Final[str] = "reposo"


def es_reposo(etiqueta: str) -> bool:
    """¿Esta etiqueta es la clase separadora, sea como se haya escrito?"""
    return normalizar_etiqueta(etiqueta) == ETIQUETA_REPOSO
