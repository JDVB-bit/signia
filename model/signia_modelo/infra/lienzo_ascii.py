"""🖼️ Dibuja puntos 2D en una cuadricula de texto, sin dependencias graficas.

Por que ASCII y no matplotlib: la inspeccion del dataset se hace mientras se
graba, en la misma consola, y a veces por SSH en la maquina donde viven los
datos. Una figura que hay que abrir en otra ventana se deja de mirar; un dibujo
que aparece en la misma linea del informe, no. Y no anade dependencias al
paquete que luego hay que instalar en el servidor.

El dominio del dibujo es fijo, `[0, 1] x [0, 1]`: son las coordenadas de
MediaPipe, o sea **el encuadre de la camara**. Asi la misma sena sale en el
mismo sitio en dos muestras distintas, y se ve si se hizo alta, baja o pegada
al borde. Con auto-zoom eso se perderia.
"""

from __future__ import annotations

from typing import Sequence

#: Tamano por defecto: cabe en cualquier terminal y no deforma el encuadre.
ANCHO_POR_DEFECTO = 48
ALTO_POR_DEFECTO = 18

#: El caracter cuenta el tiempo: los primeros frames son tenues y los ultimos
#: densos, asi que el trazo muestra la DIRECCION del movimiento, no solo su forma.
CARACTERES_DEL_TIEMPO = ".:-=+*#@"

#: Relleno y marco del encuadre de la camara.
VACIO = " "
BORDE_HORIZONTAL = "-"
BORDE_VERTICAL = "|"
ESQUINA = "+"

#: Limites del dominio dibujable (coordenadas normalizadas de MediaPipe).
MINIMO = 0.0
MAXIMO = 1.0


def _acotar(valor: float) -> float:
    """Mete el valor en [0, 1]: MediaPipe puede salirse un poco del encuadre."""
    return min(max(valor, MINIMO), MAXIMO)


def _caracter(indice: int, total: int) -> str:
    """Caracter que le toca a un punto segun lo avanzada que este la muestra."""
    if total <= 1:
        return CARACTERES_DEL_TIEMPO[-1]
    posicion = indice * (len(CARACTERES_DEL_TIEMPO) - 1) // (total - 1)
    return CARACTERES_DEL_TIEMPO[posicion]


def dibujar(
    puntos: Sequence[tuple[float, float] | None],
    *,
    ancho: int = ANCHO_POR_DEFECTO,
    alto: int = ALTO_POR_DEFECTO,
) -> list[str]:
    """Cuadricula de texto con los puntos, en orden temporal y con marco.

    Los `None` (frames sin esa mano) simplemente no se dibujan: el hueco en el
    trazo es la informacion. Si dos puntos caen en la misma celda, gana el mas
    tardio, que es el que dice hacia donde iba la mano.
    """
    if ancho < 1 or alto < 1:
        raise ValueError(f"lienzo invalido: {ancho}x{alto}")

    celdas = [[VACIO] * ancho for _ in range(alto)]
    total = len(puntos)

    for indice, punto in enumerate(puntos):
        if punto is None:
            continue
        x, y = punto
        # y crece hacia abajo en coordenadas de imagen, y la fila tambien
        columna = round(_acotar(x) * (ancho - 1))
        fila = round(_acotar(y) * (alto - 1))
        celdas[fila][columna] = _caracter(indice, total)

    marco = ESQUINA + BORDE_HORIZONTAL * ancho + ESQUINA
    cuerpo = [BORDE_VERTICAL + "".join(fila) + BORDE_VERTICAL for fila in celdas]
    return [marco, *cuerpo, marco]


def leyenda() -> str:
    """Una linea que explica que significa el gradiente de caracteres."""
    return f"tiempo: {CARACTERES_DEL_TIEMPO[0]} inicio -> {CARACTERES_DEL_TIEMPO[-1]} final"
