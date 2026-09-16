/** 🔁 Bucle `requestAnimationFrame` que pasa cada frame NUEVO del video por el detector. */

import { useEffect, useRef } from 'react'

/** `HTMLMediaElement.HAVE_CURRENT_DATA`: el video ya tiene un frame que se puede leer. */
const VIDEO_CON_FRAME_DISPONIBLE = 2

/** Llama a `alDetectar(resultado)` por cada frame nuevo mientras haya `detector`.
 *
 * El callback se guarda en una ref: cambiarlo en cada render no reinicia el
 * bucle ni lo deja leyendo valores viejos.
 */
export default function useBucleDeDeteccion({ videoRef, detector, alDetectar }) {
    const alDetectarRef = useRef(alDetectar)

    useEffect(() => {
        alDetectarRef.current = alDetectar
    }, [alDetectar])

    useEffect(() => {
        if (!detector) return undefined

        let animacion = 0
        let ultimoTiempoDeVideo = -1

        const paso = () => {
            const video = videoRef.current
            // rAF va a ~60 Hz y la camara a ~30: solo se procesa si el video avanzo
            const hayFrameNuevo =
                video &&
                video.readyState >= VIDEO_CON_FRAME_DISPONIBLE &&
                video.currentTime !== ultimoTiempoDeVideo

            if (hayFrameNuevo) {
                ultimoTiempoDeVideo = video.currentTime
                alDetectarRef.current(detector.detectForVideo(video, performance.now()))
            }
            animacion = requestAnimationFrame(paso)
        }

        animacion = requestAnimationFrame(paso)
        return () => cancelAnimationFrame(animacion)
    }, [detector, videoRef])
}
