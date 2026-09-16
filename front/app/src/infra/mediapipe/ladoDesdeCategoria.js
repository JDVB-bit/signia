/** ✋ Traduce el `handedness` de MediaPipe ("Left"/"Right") al lado del contrato. */

import { LADO_DERECHA, LADO_IZQUIERDA } from '../../dominio/contrato.js'

/** ⚠️ Riesgo del plan: el video se PINTA espejado, pero al detector llega el frame tal cual.
 * Si al levantar la mano derecha el rotulo del overlay dice "izquierda", pon
 * esto a `true` ANTES de grabar el dataset: despues habria que corregirlo entero. */
export const INVERTIR_LADO = false

const LADO_POR_CATEGORIA = {
    Left: LADO_IZQUIERDA,
    Right: LADO_DERECHA,
}

const LADO_OPUESTO = {
    [LADO_IZQUIERDA]: LADO_DERECHA,
    [LADO_DERECHA]: LADO_IZQUIERDA,
}

/** "Left"/"Right" -> lado del contrato, o null si la categoria es desconocida. */
export function ladoDesdeCategoria(categoria, invertir = INVERTIR_LADO) {
    const lado = LADO_POR_CATEGORIA[categoria]
    if (lado === undefined) return null
    return invertir ? LADO_OPUESTO[lado] : lado
}
