/** 📤 Que hacer con el lote grabado: subirlo, y si no se puede, no perderlo.
 *
 * El backend puede estar apagado -en el portatil de casa lo estara casi
 * siempre-, y una tanda de 40 muestras grabadas es media hora de trabajo que no
 * se puede tirar por un `ECONNREFUSED`. Por eso el fallo **no es un error**: es
 * el camino de respaldo, que descarga el mismo JSON que antes y lo deja listo
 * para `scripts/importar_lote.py`.
 *
 * Vive en aplicacion y no en el hook porque es una decision de producto, no de
 * React: se prueba sin montar un componente.
 */

/** Como acabo el envio. La presentacion decide que texto le pone a cada uno. */
export const RESULTADOS_DE_ENVIO = Object.freeze({
    SUBIDO: 'subido',
    RESPALDADO: 'respaldado',
    SIN_MUESTRAS: 'sin-muestras',
})

/** Sube el paquete; si la subida falla, lo descarga como respaldo.
 *
 * Devuelve siempre un resultado -nunca lanza- porque la interfaz tiene que
 * poder contar lo que paso en los tres casos.
 */
export async function enviarMuestras({ paquete, subir, descargar }) {
    const cuantas = paquete?.muestras?.length ?? 0
    if (cuantas === 0) return { resultado: RESULTADOS_DE_ENVIO.SIN_MUESTRAS, cuantas }

    try {
        const respuesta = await subir(paquete)
        return {
            resultado: RESULTADOS_DE_ENVIO.SUBIDO,
            // El backend manda lo que REALMENTE guardo; no se asume que sea todo
            cuantas: respuesta?.guardadas ?? cuantas,
            porEtiqueta: respuesta?.por_etiqueta ?? {},
        }
    } catch (error) {
        descargar(paquete)
        return { resultado: RESULTADOS_DE_ENVIO.RESPALDADO, cuantas, motivo: error.message }
    }
}
