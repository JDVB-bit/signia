"""🔬 Inspeccion del dataset crudo: medir, resumir, diagnosticar y mirar.

Cuatro modulos con una responsabilidad cada uno:

| Modulo | Responde a |
|---|---|
| `metricas_de_muestra` | ¿Que hay dentro de ESTA muestra? |
| `resumen_del_dataset` | ¿Cuanto hay de cada clase, y de que sesiones? |
| `diagnostico_del_dataset` | ¿Cumple los criterios de la Fase 2? |
| `trayectoria_de_muneca` | ¿La sena tiene pinta de sena? |

Ninguno toca disco ni imprime nada: reciben entidades y devuelven datos. El
informe por consola es `infra/informe_de_dataset.py` y el punto de entrada es
`scripts/inspeccionar.py`.
"""

from .diagnostico_del_dataset import (
    REVISIONES,
    REVISIONES_DE_CADA_MUESTRA,
    Aviso,
    CodigoDeAviso,
    Gravedad,
    diagnosticar,
    hay_bloqueos,
    identificador,
)
from .metricas_de_muestra import MetricasDeMuestra, medir
from .resumen_del_dataset import (
    MuestraMedida,
    ResumenDeClase,
    ResumenDeFrases,
    ResumenDelDataset,
    resumir,
)
from .trayectoria_de_muneca import Trayectoria, lado_mas_presente, trayectoria_de_muneca

__all__ = [
    "REVISIONES",
    "REVISIONES_DE_CADA_MUESTRA",
    "Aviso",
    "CodigoDeAviso",
    "Gravedad",
    "MetricasDeMuestra",
    "MuestraMedida",
    "ResumenDeClase",
    "ResumenDeFrases",
    "ResumenDelDataset",
    "Trayectoria",
    "diagnosticar",
    "hay_bloqueos",
    "identificador",
    "lado_mas_presente",
    "medir",
    "resumir",
    "trayectoria_de_muneca",
]
