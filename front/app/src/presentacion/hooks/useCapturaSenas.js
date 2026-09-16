/** 📸 Captura de muestras de señas (Fase 1): compone detector, bucle, grabacion y lote.
 *
 * camara -> HandLandmarker -> frame del contrato -> overlay + grabacion -> muestra.
 * Cada pieza es un hook o modulo con una sola responsabilidad; este solo las
 * conecta y ofrece a la pagina una API estable.
 */

import { useCallback, useEffect, useState } from 'react'

import { nombreDeFichero, paqueteDeMuestras } from '../../aplicacion/paqueteDeMuestras.js'
import { idSesion } from '../../aplicacion/sesionDeGrabacion.js'
import { pintarManosSobreVideo } from '../../infra/canvas/pintarManosSobreVideo.js'
import { frameDesdeResultado } from '../../infra/mediapipe/frameDesdeDeteccion.js'
import { descargarJson } from '../../infra/navegador/descargarJson.js'
import { AVISOS_DE_CAPTURA } from '../textos/textosDeCaptura.js'
import useBucleDeDeteccion from './useBucleDeDeteccion.js'
import useDetectorDeManos from './useDetectorDeManos.js'
import useGrabacionDeMuestra from './useGrabacionDeMuestra.js'
import useMuestrasCapturadas from './useMuestrasCapturadas.js'

/** `t` provisional del frame en vivo: `crearMuestra` lo reindexa al cerrar la grabacion. */
const T_PROVISIONAL = 0

export default function useCapturaSenas({ videoRef, canvasRef, etiqueta, activo = false }) {
    const [sesion] = useState(idSesion)
    const [aviso, setAviso] = useState(null)
    const [manosDetectadas, setManosDetectadas] = useState(0)

    const { estado, detector } = useDetectorDeManos(activo)
    const { muestras, agregar, borrarUltima, limpiar } = useMuestrasCapturadas()
    const { grabando, segundos, alternar, registrarFrame, abortar } = useGrabacionDeMuestra({
        etiqueta,
        sesion,
        alGuardar: agregar,
        alAvisar: setAviso,
    })

    const alDetectar = useCallback(
        (resultado) => {
            const frame = frameDesdeResultado(resultado, T_PROVISIONAL)
            pintarManosSobreVideo(canvasRef?.current, videoRef.current, frame.manos)
            setManosDetectadas(frame.manos.length)
            registrarFrame(frame)
        },
        [canvasRef, registrarFrame, videoRef],
    )

    useBucleDeDeteccion({ videoRef, detector: activo ? detector : null, alDetectar })

    // Si la camara se apaga a mitad de una grabacion, esa grabacion ya no es valida
    useEffect(() => {
        if (!activo) abortar()
    }, [activo, abortar])

    const exportar = useCallback(
        (descargar = descargarJson) => {
            if (muestras.length === 0) {
                setAviso(AVISOS_DE_CAPTURA.SIN_MUESTRAS)
                return null
            }
            const paquete = paqueteDeMuestras(muestras)
            descargar(nombreDeFichero(muestras), paquete)
            return paquete
        },
        [muestras],
    )

    return {
        estado,
        grabando,
        muestras,
        manosDetectadas,
        segundos,
        aviso,
        sesion,
        alternarGrabacion: alternar,
        borrarUltima,
        limpiar,
        exportar,
    }
}
