/** 🦴 Esqueleto de las manos dibujado sobre el video.
 *
 * No es decoracion: permite descartar una muestra mala ANTES de guardarla, y el
 * rotulo del lado junto a la muñeca es la verificacion empirica del handedness
 * con el video espejado (riesgo listado en el plan).
 */

import { IDX_MUNECA, LADO_DERECHA, LADO_IZQUIERDA, N_LANDMARKS } from '../../dominio/contrato.js'

/** Conexiones entre landmarks de MediaPipe: palma y los cinco dedos. */
export const CONEXIONES = [
    [0, 1], [1, 2], [2, 3], [3, 4], // pulgar
    [0, 5], [5, 6], [6, 7], [7, 8], // indice
    [5, 9], [9, 10], [10, 11], [11, 12], // corazon
    [9, 13], [13, 14], [14, 15], [15, 16], // anular
    [13, 17], [17, 18], [18, 19], [19, 20], // meñique
    [0, 17], // base de la palma
]

/** Un color por lado, para ver de un vistazo si MediaPipe se equivoca de mano. */
export const COLOR_POR_LADO = {
    [LADO_IZQUIERDA]: '#E68825',
    [LADO_DERECHA]: '#4FA3D1',
}

const COLOR_HUESO = 'rgba(255, 255, 255, 0.85)'
const GROSOR_HUESO_PX = 3
const RADIO_PUNTO_PX = 4
const VUELTA_COMPLETA_RAD = Math.PI * 2
const FUENTE_ROTULO = '600 14px system-ui, sans-serif'
const SEPARACION_ROTULO_PX = 8

/** Landmark normalizado (0..1) -> pixel del canvas.
 *
 * Si el video se pinta espejado, el overlay se espeja igual o el esqueleto
 * aparece en la mano contraria. Se invierte la coordenada en vez de voltear el
 * canvas entero para que los rotulos sigan leyendose.
 */
export function puntoEnCanvas(landmark, { ancho, alto, espejado = true }) {
    const x = espejado ? 1 - landmark.x : landmark.x
    return { x: x * ancho, y: landmark.y * alto }
}

/** Dibuja los huesos (lineas entre conexiones) de una mano. */
function dibujarHuesos(contexto, puntos) {
    contexto.lineWidth = GROSOR_HUESO_PX
    contexto.strokeStyle = COLOR_HUESO
    contexto.beginPath()
    for (const [desde, hasta] of CONEXIONES) {
        contexto.moveTo(puntos[desde].x, puntos[desde].y)
        contexto.lineTo(puntos[hasta].x, puntos[hasta].y)
    }
    contexto.stroke()
}

/** Dibuja un punto por landmark con el color de su lado. */
function dibujarArticulaciones(contexto, puntos, color) {
    contexto.fillStyle = color
    for (const punto of puntos) {
        contexto.beginPath()
        contexto.arc(punto.x, punto.y, RADIO_PUNTO_PX, 0, VUELTA_COMPLETA_RAD)
        contexto.fill()
    }
}

/** Escribe el lado junto a la muñeca: es la verificacion del handedness. */
function rotularLado(contexto, puntos, lado, color) {
    const muneca = puntos[IDX_MUNECA]
    contexto.font = FUENTE_ROTULO
    contexto.textBaseline = 'top'
    contexto.fillStyle = color
    contexto.fillText(lado, muneca.x + SEPARACION_ROTULO_PX, muneca.y + SEPARACION_ROTULO_PX)
}

/** Repinta el overlay entero con las manos del frame actual. */
export function dibujarManos(contexto, manos, opciones) {
    const { ancho, alto } = opciones
    contexto.clearRect(0, 0, ancho, alto)

    for (const mano of manos) {
        // Una mano incompleta se ignora: reventar aqui pararia el bucle de video
        if (mano.lm?.length !== N_LANDMARKS) continue

        const puntos = mano.lm.map(([x, y]) => puntoEnCanvas({ x, y }, opciones))
        const color = COLOR_POR_LADO[mano.lado] ?? COLOR_HUESO
        dibujarHuesos(contexto, puntos)
        dibujarArticulaciones(contexto, puntos, color)
        rotularLado(contexto, puntos, mano.lado, color)
    }
}
