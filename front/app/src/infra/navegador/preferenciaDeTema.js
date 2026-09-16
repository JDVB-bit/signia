/** 🌗 Preferencia de tema claro/oscuro: se lee, se guarda y se aplica al documento. */

import { guardarLocal, leerLocal } from './almacenamientoSeguro.js'

// Se conserva la clave historica para no perder la preferencia de quien ya la eligio
const CLAVE_TEMA = 'signia-theme'
const VALOR_OSCURO = 'dark'
const VALOR_CLARO = 'light'

/** Clase que activa la paleta oscura en `index.css`. */
const CLASE_TEMA_OSCURO = 'dark'
const CONSULTA_SISTEMA_OSCURO = '(prefers-color-scheme: dark)'

/** ¿Debe arrancar en oscuro? La eleccion guardada gana a la del sistema operativo. */
export function temaOscuroPreferido() {
    const guardado = leerLocal(CLAVE_TEMA)
    if (guardado) return guardado === VALOR_OSCURO
    if (typeof window === 'undefined') return false
    return window.matchMedia?.(CONSULTA_SISTEMA_OSCURO).matches ?? false
}

/** Recuerda la eleccion del usuario para la proxima visita. */
export function guardarTemaOscuro(oscuro) {
    guardarLocal(CLAVE_TEMA, oscuro ? VALOR_OSCURO : VALOR_CLARO)
}

/** Aplica (o quita) la paleta oscura en <html>. */
export function aplicarTemaOscuro(oscuro) {
    document.documentElement.classList.toggle(CLASE_TEMA_OSCURO, oscuro)
}

/** Se llama antes de montar React para que nada nazca con los colores equivocados. */
export function aplicarTemaInicial() {
    const oscuro = temaOscuroPreferido()
    aplicarTemaOscuro(oscuro)
    return oscuro
}
