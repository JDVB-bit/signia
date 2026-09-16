/** Etiqueta de una seña tal y como se guarda: sin espacios de mas y en minusculas.
 *
 * Asi "Hola", " hola " y "HOLA" son la misma clase para el modelo.
 */
export function normalizarEtiqueta(texto) {
    return (texto ?? '').trim().toLowerCase()
}
