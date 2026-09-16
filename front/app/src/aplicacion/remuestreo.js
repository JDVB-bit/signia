/** ⏱️ Remuestreo temporal: de N frames grabados a una ventana fija de `destino` frames.
 *
 * Es el gemelo de `model/signia_modelo/aplicacion/remuestreo.py` y la UNICA
 * parte del preprocesado que existe dos veces; el resto viaja dentro del grafo
 * ONNX. Que ambos lados coincidan se comprueba en `__tests__/conformidad.test.js`.
 */

import { T } from '../dominio/contrato.js'

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
    // Con un unico destino no hay paso que calcular (evita dividir por cero)
    if (destino === 1) return [0]

    const ultimoIndice = nFrames - 1
    const paso = ultimoIndice / (destino - 1)
    return Array.from({ length: destino }, (_, posicion) => Math.round(posicion * paso))
}
