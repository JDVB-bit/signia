/** 🖐️ Carga el detector de manos cuando hace falta y expone en que estado esta. */

import { useEffect, useState } from 'react'

import { obtenerDetectorDeManos } from '../../infra/mediapipe/detectorDeManos.js'

export const ESTADOS_DETECTOR = Object.freeze({
    INACTIVO: 'inactivo',
    CARGANDO: 'cargando',
    LISTO: 'listo',
    ERROR: 'error',
})

/** Mientras `activo` sea false no se descarga nada (el modelo pesa varios MB). */
export default function useDetectorDeManos(activo) {
    const [estado, setEstado] = useState(ESTADOS_DETECTOR.INACTIVO)
    const [detector, setDetector] = useState(null)

    useEffect(() => {
        if (!activo) {
            setEstado(ESTADOS_DETECTOR.INACTIVO)
            setDetector(null)
            return undefined
        }

        // Si la pagina se desmonta mientras carga, la respuesta tardia se ignora
        let cancelado = false
        setEstado(ESTADOS_DETECTOR.CARGANDO)
        obtenerDetectorDeManos()
            .then((instancia) => {
                if (cancelado) return
                setDetector(instancia)
                setEstado(ESTADOS_DETECTOR.LISTO)
            })
            .catch(() => {
                if (!cancelado) setEstado(ESTADOS_DETECTOR.ERROR)
            })

        return () => {
            cancelado = true
        }
    }, [activo])

    return { estado, detector }
}
