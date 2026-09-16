/** 🎞️ Recuerda si el usuario ya vio la pantalla de carga inicial. */

import { guardarLocal, leerLocal } from './almacenamientoSeguro.js'

const CLAVE_INTRO = 'signia-intro-vista'
const VALOR_VISTA = '1'

export function introYaVista() {
    return leerLocal(CLAVE_INTRO) === VALOR_VISTA
}

export function marcarIntroVista() {
    guardarLocal(CLAVE_INTRO, VALOR_VISTA)
}
