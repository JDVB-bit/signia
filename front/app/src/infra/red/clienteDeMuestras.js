/** 📡 Sube un lote de muestras al backend (`POST /muestras`).
 *
 * Solo transporte: construye la peticion, interpreta la respuesta y traduce el
 * fallo a un Error con un mensaje que se pueda enseñar. Ni valida el contrato
 * -de eso ya se encarga el backend con el mismo codigo que el entrenamiento-
 * ni decide que hacer si falla; eso es del caso de uso.
 */

import { ENDPOINTS, urlDe } from './urlDeLaApi.js'

/** Cabeceras de un envio JSON. */
const CABECERAS = { 'Content-Type': 'application/json' }

/** Clave del motivo en los errores de FastAPI. */
const CLAVE_DETALLE = 'detail'

/** Mensaje cuando el servidor falla sin explicar por que. */
const MOTIVO_DESCONOCIDO = 'el servidor rechazo el lote'

/** Lee el motivo que devuelve el backend, sin romperse si no es JSON. */
async function motivoDelFallo(respuesta) {
    try {
        const cuerpo = await respuesta.json()
        return cuerpo?.[CLAVE_DETALLE] ?? MOTIVO_DESCONOCIDO
    } catch {
        return MOTIVO_DESCONOCIDO
    }
}

/** Envia el paquete y devuelve lo que guardo el backend.
 *
 * Lanza un Error si la red falla o si el backend responde con un codigo de
 * error; el mensaje ya viene listo para enseñarlo.
 */
export async function subirLote(paquete, { peticion = fetch, entorno } = {}) {
    const respuesta = await peticion(urlDe(ENDPOINTS.MUESTRAS, entorno), {
        method: 'POST',
        headers: CABECERAS,
        body: JSON.stringify(paquete),
    })

    if (!respuesta.ok) throw new Error(await motivoDelFallo(respuesta))
    return respuesta.json()
}
