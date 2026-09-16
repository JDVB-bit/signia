/** 🧱 Construccion del tensor crudo `(T, 2, 21, 3)` + presencia `(T, 2)` a partir de una muestra.
 *
 * Aqui no se normaliza nada: restar la muñeca, escalar y calcular la forma
 * ocurre dentro del grafo ONNX, para que navegador y entrenamiento ejecuten
 * literalmente el mismo codigo (principio 2 del plan).
 */

import { LADOS, N_DIMS, N_LANDMARKS, N_MANOS, T } from '../dominio/contrato.js'
import { manoDelFrame } from '../dominio/manoDelFrame.js'
import { indicesRemuestreo } from './remuestreo.js'

/** Presencia de una mano en su ranura. */
const PRESENTE = 1

/** Apila frames ya elegidos en los dos arrays planos del contrato.
 *
 * Se devuelven planos (y no anidados) porque es lo que espera `ort.Tensor` de
 * onnxruntime-web, y en orden C, igual que numpy.
 */
export function apilarFrames(frames) {
    const nFrames = frames.length
    const valoresPorMano = N_LANDMARKS * N_DIMS
    const lm = new Float32Array(nFrames * N_MANOS * valoresPorMano)
    const presencia = new Float32Array(nFrames * N_MANOS)

    frames.forEach((frame, indiceFrame) => {
        LADOS.forEach((lado, ranura) => {
            const mano = manoDelFrame(frame, lado)
            // Ausencia: se quedan los ceros y presencia 0, que tambien es informacion
            if (mano === null) return

            const posicionRanura = indiceFrame * N_MANOS + ranura
            presencia[posicionRanura] = PRESENTE
            const base = posicionRanura * valoresPorMano
            for (let punto = 0; punto < N_LANDMARKS; punto += 1) {
                for (let dimension = 0; dimension < N_DIMS; dimension += 1) {
                    lm[base + punto * N_DIMS + dimension] = mano.lm[punto][dimension]
                }
            }
        })
    })

    return {
        lm,
        presencia,
        dims: {
            lm: [nFrames, N_MANOS, N_LANDMARKS, N_DIMS],
            presencia: [nFrames, N_MANOS],
        },
    }
}

/** Muestra cruda -> ventana de longitud fija lista para el grafo. */
export function construirEntrada(muestra, destino = T) {
    const indices = indicesRemuestreo(muestra.frames.length, destino)
    return apilarFrames(indices.map((indice) => muestra.frames[indice]))
}
