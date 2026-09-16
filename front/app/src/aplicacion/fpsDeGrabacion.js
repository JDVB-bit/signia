/** 🎞️ Frames por segundo reales de una grabacion, para dejarlo anotado en la muestra. */

import { MS_POR_SEGUNDO } from '../dominio/unidadesDeTiempo.js'

/** fps de `nFrames` capturados en `duracionMs`, o null si la duracion no es valida. */
export function fpsDe(nFrames, duracionMs) {
    if (duracionMs <= 0) return null
    return (nFrames * MS_POR_SEGUNDO) / duracionMs
}
