/** 💬 Como se le cuenta al usuario en que acabo el envio del lote. */

import { RESULTADOS_DE_ENVIO } from '../../aplicacion/envioDeMuestras.js'

/** Plural del sustantivo, para que la frase no diga "1 muestras". */
function muestras(cuantas) {
    return cuantas === 1 ? '1 muestra' : `${cuantas} muestras`
}

/** Frase para cada desenlace del envio.
 *
 * El respaldo no se cuenta como un error: se dice que el servidor no respondio
 * y que el fichero se descargo, que es justo lo que el usuario tiene que saber
 * para no volver a grabarlo todo.
 */
export function textoDeEnvio({ resultado, cuantas, motivo }) {
    if (resultado === RESULTADOS_DE_ENVIO.SUBIDO) {
        return `Se enviaron ${muestras(cuantas)} al servidor.`
    }
    if (resultado === RESULTADOS_DE_ENVIO.RESPALDADO) {
        return `El servidor no respondio (${motivo}). Se descargaron ${muestras(cuantas)} como respaldo.`
    }
    return 'Todavía no hay muestras que enviar.'
}

/** Texto del boton mientras la peticion esta en marcha. */
export const ENVIANDO = 'Enviando...'
