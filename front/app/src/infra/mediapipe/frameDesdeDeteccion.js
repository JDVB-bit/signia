/** 🎞️ Resultado de `detectForVideo` -> un frame del contrato (`model/contrato.md`). */

import { N_LANDMARKS, SCORE_MAXIMO } from '../../dominio/contrato.js'
import { INVERTIR_LADO, ladoDesdeCategoria } from './ladoDesdeCategoria.js'

/** Decimales por coordenada: MediaPipe no es mas preciso y el JSON ocupa la mitad.
 * Sigue muy por encima del 1e-5 que exige el test de conformidad. */
export const DECIMALES_COORDENADA = 6

/** Profundidad asumida si MediaPipe no reporta `z`. */
const Z_POR_DEFECTO = 0

const redondear = (valor) => Number(valor.toFixed(DECIMALES_COORDENADA))

/** Convierte la deteccion de un instante en `{ t, manos }`.
 *
 * Un frame puede quedarse con 0, 1 o 2 manos: la ausencia es informacion y no
 * se rellena. Las manos con handedness desconocido o landmarks incompletos se
 * ignoran en vez de inventarles datos.
 */
export function frameDesdeResultado(resultado, t, { invertirLado = INVERTIR_LADO } = {}) {
    const landmarks = resultado?.landmarks ?? []
    // Segun la version de tasks-vision el campo viene en singular o en plural
    const handedness = resultado?.handedness ?? resultado?.handednesses ?? []

    const manos = []
    landmarks.forEach((puntos, indice) => {
        const categoria = handedness[indice]?.[0]
        const lado = ladoDesdeCategoria(categoria?.categoryName, invertirLado)
        if (lado === null || puntos.length !== N_LANDMARKS) return

        manos.push({
            lado,
            score: redondear(categoria.score ?? SCORE_MAXIMO),
            lm: puntos.map((punto) => [
                redondear(punto.x),
                redondear(punto.y),
                redondear(punto.z ?? Z_POR_DEFECTO),
            ]),
        })
    })

    return { t, manos }
}
