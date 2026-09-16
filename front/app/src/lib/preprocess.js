/** Remuestreo temporal y construccion del tensor crudo, en el navegador.
 *
 * Es el gemelo de `model/signia_modelo/aplicacion/` y la UNICA parte del
 * preprocesado que existe dos veces (Python para entrenar, JS para inferir).
 * Todo lo demas -restar la muneca, la escala, la forma- viaja dentro del grafo
 * ONNX justamente para no duplicarlo.
 *
 * Que los dos lados calculen lo mismo no se confia: se comprueba en
 * `__tests__/conformidad.test.js` contra los fixtures generados por Python.
 *
 * Contrato completo en `model/contrato.md`.
 */

export const SCHEMA = 1
export const T = 48
export const N_LANDMARKS = 21
export const N_DIMS = 3
export const N_MANOS = 2

/** Ranuras fijas del tensor. Nunca el orden de deteccion de MediaPipe. */
export const LADOS = ['izquierda', 'derecha']

/** Mano de ese lado en el frame, o null.
 *
 * MediaPipe puede reportar dos manos con el mismo lado (falso positivo). La
 * regla, identica a la de `Frame.mano()` en Python: gana la de mayor score; a
 * igualdad, la primera.
 */
export function manoDelFrame(frame, lado) {
    let elegida = null
    for (const mano of frame.manos ?? []) {
        if (mano.lado !== lado) continue
        if (elegida === null || mano.score > elegida.score) elegida = mano
    }
    return elegida
}

/** Indices de los `destino` frames que representan la secuencia.
 *
 * `Math.round` equivale al `int(x + 0.5)` de Python: NO se puede sustituir por
 * el `round()` de Python (que redondea al par) ni al reves. Ver contrato.md.
 */
export function indicesRemuestreo(nFrames, destino = T) {
    if (!Number.isInteger(nFrames) || nFrames < 1) {
        throw new Error(`no se puede remuestrear una secuencia de ${nFrames} frames`)
    }
    if (!Number.isInteger(destino) || destino < 1) {
        throw new Error(`destino invalido: ${destino}`)
    }
    if (destino === 1) return [0]

    const paso = (nFrames - 1) / (destino - 1)
    return Array.from({ length: destino }, (_, i) => Math.round(i * paso))
}

/** Apila frames ya elegidos en los dos arrays planos del contrato.
 *
 * Se devuelven planos (y no anidados) porque es lo que espera `ort.Tensor` de
 * onnxruntime-web, y en orden C, igual que numpy.
 */
export function apilarFrames(frames) {
    const n = frames.length
    const lm = new Float32Array(n * N_MANOS * N_LANDMARKS * N_DIMS)
    const presencia = new Float32Array(n * N_MANOS)

    frames.forEach((frame, i) => {
        LADOS.forEach((lado, ranura) => {
            const mano = manoDelFrame(frame, lado)
            if (mano === null) return // ausencia: ceros y presencia 0, es informacion

            presencia[i * N_MANOS + ranura] = 1
            const base = (i * N_MANOS + ranura) * N_LANDMARKS * N_DIMS
            for (let p = 0; p < N_LANDMARKS; p += 1) {
                for (let d = 0; d < N_DIMS; d += 1) {
                    lm[base + p * N_DIMS + d] = mano.lm[p][d]
                }
            }
        })
    })

    return {
        lm,
        presencia,
        dims: {
            lm: [n, N_MANOS, N_LANDMARKS, N_DIMS],
            presencia: [n, N_MANOS],
        },
    }
}

/** Muestra cruda -> ventana de longitud fija lista para el grafo. */
export function construirEntrada(muestra, destino = T) {
    const indices = indicesRemuestreo(muestra.frames.length, destino)
    return apilarFrames(indices.map((i) => muestra.frames[i]))
}
