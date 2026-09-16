"""📜 Constantes del contrato de datos (Fase 0).

Fuente de verdad en prosa: `model/contrato.md`. Este modulo es python puro:
cualquier capa puede depender de el y el no depende de ninguna. Cambiar un
valor de aqui obliga a reentrenar, pero nunca invalida el dataset crudo.
"""

from typing import Final

# --- Versionado ----------------------------------------------------------------

#: Version del formato de transporte/almacenamiento (campo `schema` del JSON).
SCHEMA: Final[int] = 1

#: Version del preprocesado; viaja en `manifest.json` para comparar artefactos.
VERSION_PREPROCESADO: Final[str] = "1"

# --- Geometria de MediaPipe HandLandmarker -------------------------------------

#: Landmarks por mano.
N_LANDMARKS: Final[int] = 21
#: Coordenadas por landmark (x, y, z).
N_DIMS: Final[int] = 3
#: Ranuras fijas de mano: izquierda y derecha. La ausencia NO se rellena.
N_MANOS: Final[int] = 2

#: Indice del landmark de la muneca (origen de la forma y de la escala).
IDX_MUNECA: Final[int] = 0
#: Indice del nudillo medio (MCP del dedo corazon), extremo de la escala.
IDX_NUDILLO_MEDIO: Final[int] = 9

#: Rango valido de la confianza (`score`) que MediaPipe da a cada mano.
SCORE_MINIMO: Final[float] = 0.0
SCORE_MAXIMO: Final[float] = 1.0

# --- Ventana temporal ----------------------------------------------------------

#: Longitud temporal fija tras el remuestreo (~1.6 s a 30 fps).
T: Final[int] = 48

# --- Features que ve el modelo -------------------------------------------------

VALORES_PRESENCIA: Final[int] = 1
VALORES_POSICION: Final[int] = 2  # x, y de la muneca en el encuadre
VALORES_ESCALA: Final[int] = 1  # distancia muneca -> nudillo medio
VALORES_FORMA: Final[int] = (N_LANDMARKS - 1) * N_DIMS  # 20 puntos x 3 = 60

#: Valores que describen una mano en un frame (64).
VALORES_POR_MANO: Final[int] = VALORES_PRESENCIA + VALORES_POSICION + VALORES_ESCALA + VALORES_FORMA

#: Features por frame. Tensor de entrada del modelo: (T, F) = (48, 128).
F: Final[int] = VALORES_POR_MANO * N_MANOS

#: Evita dividir por cero cuando la escala de una mano degenera.
EPS_ESCALA: Final[float] = 1e-6

# --- Vocabulario del contrato --------------------------------------------------

#: Orden canonico de las ranuras de mano (por `handedness`, nunca por deteccion).
LADOS_CANONICOS: Final[tuple[str, str]] = ("izquierda", "derecha")

#: Tipos de muestra del dataset.
TIPO_AISLADA: Final[str] = "aislada"
TIPO_FRASE: Final[str] = "frase"
