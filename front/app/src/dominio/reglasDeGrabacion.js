/** 🎬 Reglas que deciden cuando una grabacion termina y cuando no sirve como muestra.
 *
 * Viven aqui y en ningun otro sitio: el hook solo las aplica y la interfaz solo
 * traduce el motivo a texto. Descartar en el momento es mucho mas barato que
 * descubrir el dataset sucio despues de grabar cientos de muestras.
 */

/** Tope de una grabacion: holgado sobre la ventana del modelo (~1.6 s) pero sin
 * dejar que una pulsacion olvidada genere una muestra de dos minutos. */
export const DURACION_MAXIMA_MS = 4000

/** Por debajo de esto no hay seña que valga. */
export const FRAMES_MINIMOS = 5

/** Motivos por los que una grabacion se descarta (la presentacion pone el texto). */
export const MOTIVOS_DE_DESCARTE = Object.freeze({
    DEMASIADO_CORTA: 'demasiado-corta',
    SIN_MANOS: 'sin-manos',
})

/** Cuantos frames de la grabacion llevan al menos una mano. */
export function framesConMano(frames) {
    return frames.filter((frame) => frame.manos.length > 0).length
}

/** ¿Toca cerrar la grabacion por haber alcanzado el tope de duracion? */
export function debeCerrarPorTiempo(transcurridoMs) {
    return transcurridoMs >= DURACION_MAXIMA_MS
}

/** Motivo por el que NO sirve esta grabacion, o null si sirve. */
export function motivoDeDescarte(frames) {
    if (frames.length < FRAMES_MINIMOS) return MOTIVOS_DE_DESCARTE.DEMASIADO_CORTA
    // Si la mano nunca aparecio, la muestra no enseña nada y ensucia el dataset
    if (framesConMano(frames) === 0) return MOTIVOS_DE_DESCARTE.SIN_MANOS
    return null
}
