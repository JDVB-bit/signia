"""Constantes del contrato de datos (Fase 0).

Fuente de verdad en prosa: `model/contrato.md`.

Este modulo es **python puro**: no importa numpy, torch ni nada de infra.
Cualquier capa puede depender de el; el no depende de ninguna.
Cambiar un valor de aqui invalida los artefactos entrenados (hay que
reentrenar), pero nunca el dataset crudo ya grabado.
"""

from typing import Final

#: Version del formato de transporte/almacenamiento (campo `schema` del JSON).
SCHEMA: Final[int] = 1

#: Version del preprocesado. Viaja en `manifest.json` del artefacto: si cambia,
#: un modelo entrenado con la anterior ya no es comparable.
VERSION_PREPROCESADO: Final[str] = "1"

#: Landmarks por mano que devuelve MediaPipe HandLandmarker.
N_LANDMARKS: Final[int] = 21
#: Coordenadas por landmark (x, y, z).
N_DIMS: Final[int] = 3
#: Ranuras fijas de mano: izquierda y derecha. La ausencia NO se rellena.
N_MANOS: Final[int] = 2

#: Longitud temporal fija tras el remuestreo (~1.6 s a 30 fps).
T: Final[int] = 48

#: Indice del landmark de la muneca (origen de la forma y de la escala).
IDX_MUNECA: Final[int] = 0
#: Indice del nudillo medio (MCP del dedo corazon), extremo de la escala.
IDX_NUDILLO_MEDIO: Final[int] = 9

#: Desglose de los 64 valores que describen una mano en un frame.
VALORES_PRESENCIA: Final[int] = 1
VALORES_POSICION: Final[int] = 2          # x, y de la muneca en el encuadre
VALORES_ESCALA: Final[int] = 1            # muneca -> nudillo medio
VALORES_FORMA: Final[int] = (N_LANDMARKS - 1) * N_DIMS   # 20 puntos x 3 = 60

VALORES_POR_MANO: Final[int] = (
    VALORES_PRESENCIA + VALORES_POSICION + VALORES_ESCALA + VALORES_FORMA
)  # 64

#: Features por frame que ve el modelo. Tensor de entrada: (T, F) = (48, 128).
F: Final[int] = VALORES_POR_MANO * N_MANOS

#: Evita dividir por cero cuando la escala de una mano degenera.
EPS_ESCALA: Final[float] = 1e-6

#: Orden canonico de las ranuras de mano. NO se deriva del orden de deteccion
#: de MediaPipe, sino de su `handedness`.
LADOS_CANONICOS: Final[tuple[str, str]] = ("izquierda", "derecha")

#: Tipos de muestra del dataset.
TIPO_AISLADA: Final[str] = "aislada"
TIPO_FRASE: Final[str] = "frase"
