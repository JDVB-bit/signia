/** 📷 Recuerda, solo durante esta visita, si el usuario concedio la camara.
 *
 * Asi se puede activar sola al cambiar de pagina sin volver a mostrar el boton.
 * Se usa sessionStorage a proposito: en una visita nueva se vuelve a preguntar.
 * El permiso real lo sigue controlando el navegador.
 */

import { guardarEnSesion, leerDeSesion } from './almacenamientoSeguro.js'

const CLAVE_PERMISO = 'signia-camera-permiso'
const VALOR_CONCEDIDO = 'concedido'
const VALOR_DENEGADO = 'denegado'

export function permisoConcedidoEnEstaVisita() {
    return leerDeSesion(CLAVE_PERMISO) === VALOR_CONCEDIDO
}

export function recordarPermisoDeCamara(concedido) {
    guardarEnSesion(CLAVE_PERMISO, concedido ? VALOR_CONCEDIDO : VALOR_DENEGADO)
}
