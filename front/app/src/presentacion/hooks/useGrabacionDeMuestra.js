/** 🎬 Maquina de estados de UNA grabacion: iniciar, acumular frames, cerrar o abortar.
 *
 * Las decisiones (cuando cerrar, cuando descartar) son del dominio; este hook
 * solo las aplica y avisa a quien lo usa mediante `alGuardar` y `alAvisar`.
 */

import { useCallback, useEffect, useRef, useState } from 'react'

import { crearMuestra } from '../../aplicacion/crearMuestra.js'
import { fpsDe } from '../../aplicacion/fpsDeGrabacion.js'
import { normalizarEtiqueta } from '../../dominio/etiquetaDeSena.js'
import { debeCerrarPorTiempo, motivoDeDescarte } from '../../dominio/reglasDeGrabacion.js'
import { MS_POR_SEGUNDO } from '../../dominio/unidadesDeTiempo.js'
import { AVISOS_DE_CAPTURA, TEXTO_POR_MOTIVO_DE_DESCARTE } from '../textos/textosDeCaptura.js'

const SIN_AVISO = null

export default function useGrabacionDeMuestra({ etiqueta, sesion, alGuardar, alAvisar }) {
    const [grabando, setGrabando] = useState(false)
    const [segundos, setSegundos] = useState(0)

    // Refs: el bucle de video las lee a 30 Hz y no debe reiniciarse por cada cambio
    const etiquetaRef = useRef(etiqueta)
    const alGuardarRef = useRef(alGuardar)
    const alAvisarRef = useRef(alAvisar)
    const grabandoRef = useRef(false)
    const bufferRef = useRef([])
    const inicioRef = useRef(0)

    useEffect(() => {
        etiquetaRef.current = etiqueta
        alGuardarRef.current = alGuardar
        alAvisarRef.current = alAvisar
    }, [etiqueta, alGuardar, alAvisar])

    const reiniciar = useCallback(() => {
        grabandoRef.current = false
        bufferRef.current = []
        setGrabando(false)
        setSegundos(0)
    }, [])

    const cerrar = useCallback(() => {
        const frames = bufferRef.current
        const duracionMs = performance.now() - inicioRef.current
        reiniciar()

        const motivo = motivoDeDescarte(frames)
        if (motivo !== null) {
            alAvisarRef.current(TEXTO_POR_MOTIVO_DE_DESCARTE[motivo])
            return
        }

        try {
            alGuardarRef.current(
                crearMuestra({
                    etiqueta: etiquetaRef.current,
                    sesion,
                    frames,
                    fpsAprox: fpsDe(frames.length, duracionMs),
                }),
            )
            alAvisarRef.current(SIN_AVISO)
        } catch (error) {
            alAvisarRef.current(error.message)
        }
    }, [reiniciar, sesion])

    const abortar = useCallback(
        (aviso = SIN_AVISO) => {
            reiniciar()
            alAvisarRef.current(aviso)
        },
        [reiniciar],
    )

    const alternar = useCallback(() => {
        if (grabandoRef.current) {
            cerrar()
            return
        }
        if (!normalizarEtiqueta(etiquetaRef.current)) {
            alAvisarRef.current(AVISOS_DE_CAPTURA.FALTA_ETIQUETA)
            return
        }
        alAvisarRef.current(SIN_AVISO)
        bufferRef.current = []
        inicioRef.current = performance.now()
        grabandoRef.current = true
        setGrabando(true)
    }, [cerrar])

    const registrarFrame = useCallback(
        (frame) => {
            if (!grabandoRef.current) return
            bufferRef.current.push(frame)

            const transcurridoMs = performance.now() - inicioRef.current
            setSegundos(transcurridoMs / MS_POR_SEGUNDO)
            if (debeCerrarPorTiempo(transcurridoMs)) cerrar()
        },
        [cerrar],
    )

    // 🙈 Con la pestaña oculta el navegador congela rAF y la grabacion quedaria rota: se descarta
    useEffect(() => {
        if (!grabando) return undefined

        const alCambiarVisibilidad = () => {
            if (document.hidden) abortar(AVISOS_DE_CAPTURA.PESTANA_OCULTA)
        }
        document.addEventListener('visibilitychange', alCambiarVisibilidad)
        return () => document.removeEventListener('visibilitychange', alCambiarVisibilidad)
    }, [abortar, grabando])

    return { grabando, segundos, alternar, registrarFrame, abortar }
}
