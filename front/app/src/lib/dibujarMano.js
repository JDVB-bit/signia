/** Esqueleto de la mano dibujado sobre el video (Fase 1).
 *
 * No es decoracion: es lo que permite descartar una muestra mala ANTES de
 * guardarla -- y en la Fase 2 se graban cientos. Ademas rotula el `lado` que
 * reporta MediaPipe, que es como se verifica empiricamente el handedness con
 * el video espejado (riesgo listado en el plan).
 */

import { N_LANDMARKS } from './preprocess.js'

/** Conexiones entre landmarks de MediaPipe: palma y los cinco dedos. */
export const CONEXIONES = [
    [0, 1], [1, 2], [2, 3], [3, 4],           // pulgar
    [0, 5], [5, 6], [6, 7], [7, 8],           // indice
    [5, 9], [9, 10], [10, 11], [11, 12],      // corazon
    [9, 13], [13, 14], [14, 15], [15, 16],    // anular
    [13, 17], [17, 18], [18, 19], [19, 20],   // menique
    [0, 17],                                  // base de la palma
]

/** Un color por lado, para ver de un vistazo si MediaPipe se equivoca de mano. */
export const COLOR_POR_LADO = {
    izquierda: '#E68825',
    derecha: '#4FA3D1',
}

const COLOR_HUESO = 'rgba(255, 255, 255, 0.85)'
const GROSOR_HUESO = 3
const RADIO_PUNTO = 4

/** Landmark normalizado (0..1) -> pixel del canvas.
 *
 * Si el video se pinta espejado, el overlay tiene que espejarse igual o el
 * esqueleto aparece en la mano contraria. Se invierte la coordenada en vez de
 * voltear el canvas entero para que los rotulos sigan leyendose.
 */
export function puntoEnCanvas(landmark, { ancho, alto, espejado = true }) {
    const x = espejado ? 1 - landmark.x : landmark.x
    return { x: x * ancho, y: landmark.y * alto }
}

function dibujarMano(ctx, mano, opciones) {
    const puntos = mano.lm.map(([x, y]) => puntoEnCanvas({ x, y }, opciones))
    const color = COLOR_POR_LADO[mano.lado] ?? COLOR_HUESO

    ctx.lineWidth = GROSOR_HUESO
    ctx.strokeStyle = COLOR_HUESO
    ctx.beginPath()
    for (const [a, b] of CONEXIONES) {
        ctx.moveTo(puntos[a].x, puntos[a].y)
        ctx.lineTo(puntos[b].x, puntos[b].y)
    }
    ctx.stroke()

    ctx.fillStyle = color
    for (const punto of puntos) {
        ctx.beginPath()
        ctx.arc(punto.x, punto.y, RADIO_PUNTO, 0, Math.PI * 2)
        ctx.fill()
    }

    // Rotulo junto a la muneca: es la verificacion del handedness.
    const muneca = puntos[0]
    ctx.font = '600 14px system-ui, sans-serif'
    ctx.textBaseline = 'top'
    ctx.fillStyle = color
    ctx.fillText(mano.lado, muneca.x + 8, muneca.y + 8)
}

/** Repinta el overlay entero con las manos del frame actual. */
export function dibujarManos(ctx, manos, opciones) {
    const { ancho, alto } = opciones
    ctx.clearRect(0, 0, ancho, alto)
    for (const mano of manos) {
        if (mano.lm?.length === N_LANDMARKS) dibujarMano(ctx, mano, opciones)
    }
}
