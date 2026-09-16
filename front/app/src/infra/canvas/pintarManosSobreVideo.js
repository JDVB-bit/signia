/** 🖼️ Ajusta el canvas del overlay a la resolucion del video y repinta las manos. */

import { dibujarManos } from './dibujarManos.js'

const CONTEXTO_2D = '2d'

/** Pinta `manos` sobre `canvas`; no hace nada si aun no existen canvas o video. */
export function pintarManosSobreVideo(canvas, video, manos, { espejado = true } = {}) {
    if (!canvas || !video) return

    // 📐 Misma resolucion que el video: asi los landmarks (0..1) caen justo encima de la mano
    if (canvas.width !== video.videoWidth || canvas.height !== video.videoHeight) {
        canvas.width = video.videoWidth
        canvas.height = video.videoHeight
    }

    const contexto = canvas.getContext(CONTEXTO_2D)
    if (!contexto) return
    dibujarManos(contexto, manos, { ancho: canvas.width, alto: canvas.height, espejado })
}
