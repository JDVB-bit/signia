/** 📼 Frames grabados -> muestra aislada del contrato (`model/contrato.md`). */

import { SCHEMA, TIPO_AISLADA } from '../dominio/contrato.js'
import { normalizarEtiqueta } from '../dominio/etiquetaDeSena.js'

/** Decimales con los que se anota el fps real; mas precision no aporta nada. */
const DECIMALES_FPS = 1

/** Construye una muestra aislada validando lo minimo que exige el contrato.
 *
 * `t` se reindexa desde 0: la muestra es una grabacion nueva, no un trozo del
 * bucle de video. Lanza un Error si falta etiqueta, sesion o frames.
 */
export function crearMuestra({ etiqueta, sesion, frames, fpsAprox = null }) {
    const etiquetaLimpia = normalizarEtiqueta(etiqueta)
    if (!etiquetaLimpia) throw new Error('la muestra necesita una etiqueta')
    if (!sesion) throw new Error('la muestra necesita una sesion')
    if (!frames?.length) throw new Error('la muestra necesita al menos un frame')

    return {
        schema: SCHEMA,
        tipo: TIPO_AISLADA,
        etiqueta: etiquetaLimpia,
        sesion,
        fps_aprox: fpsAprox === null ? null : Number(fpsAprox.toFixed(DECIMALES_FPS)),
        frames: frames.map((frame, indice) => ({ t: indice, manos: frame.manos })),
    }
}
