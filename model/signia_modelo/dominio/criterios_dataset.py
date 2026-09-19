"""📏 Cuando un dataset esta listo para entrenar (criterios de la Fase 2).

Son los numeros del plan, escritos una sola vez y con nombre. El inspector los
aplica y devuelve avisos; no decide nada por su cuenta.

Ninguno de estos valores describe el formato de los datos, asi que **no forman
parte del contrato** (`contrato.py`) y no viajan a JS: son criterios de calidad
del dataset y pueden subir sin invalidar nada de lo ya grabado.
"""

from typing import Final

from .contrato import T

# --- Cantidad -------------------------------------------------------------------

#: Muestras por sena antes de empezar a entrenar (plan, Fase 2a).
MUESTRAS_MINIMAS_POR_CLASE: Final[int] = 30

#: `reposo` es el segmentador: necesita 2-3x mas muestras que una sena normal.
FACTOR_MINIMO_DE_REPOSO: Final[float] = 2.0

#: Frases completas del conjunto de EVALUACION (plan, Fase 2c).
FRASES_MINIMAS: Final[int] = 20

#: Glosas que tiene que combinar una frase para medir segmentacion.
GLOSAS_MINIMAS_POR_FRASE: Final[int] = 2

#: Fraccion de las frases que tiene que ser una secuencia unica. Repetir una
#: frase en otra sesion es dato bueno; grabar veinte veces la misma no mide la
#: segmentacion, solo esa frase.
FRACCION_MINIMA_DE_SECUENCIAS_DISTINTAS: Final[float] = 0.5

# --- Variedad -------------------------------------------------------------------

#: Sesiones distintas exigidas. Con una sola sesion, el modelo aprende la luz y
#: la ropa de esa tarde: la evaluacion sale bien y el producto no funciona.
SESIONES_MINIMAS: Final[int] = 2

# --- Calidad de cada muestra ----------------------------------------------------

#: Fraccion de T por debajo de la cual el remuestreo repite cada frame 4 veces
#: o mas: la muestra queda casi estatica y no ensena el movimiento de la sena.
FRACCION_MINIMA_DE_T: Final[float] = 0.25

#: Frames grabados minimos para que la muestra aporte movimiento (12 con T=48).
#: Derivado del contrato a proposito, para no repetir el numero del front.
FRAMES_MINIMOS_POR_MUESTRA: Final[int] = int(T * FRACCION_MINIMA_DE_T)

#: Proporcion minima de frames con alguna mano detectada. Por debajo, MediaPipe
#: perdio la mano medio clip y la muestra es mayoritariamente ceros.
#:
#: No se le aplica a `reposo`: ahi los frames sin mano son dato legitimo
#: (manos bajadas, fuera del encuadre), no un fallo de deteccion.
PROPORCION_MINIMA_DE_FRAMES_CON_MANO: Final[float] = 0.5
