/** Bucle de captura de muestras (Fase 1 del plan).
 *
 * camara -> HandLandmarker -> buffer de frames -> muestra del contrato.
 *
 * El hook solo orquesta: cada decision (que es un frame, cuando una muestra es
 * mala, como se llama el fichero) vive en `muestras.js`, que se prueba sin
 * navegador. Las muestras se acumulan en memoria; en esta fase "Enviar"
 * descarga un JSON y en la Fase 5 pasara a llamar al endpoint sin tocar nada
 * de aqui.
 */

import { useCallback, useEffect, useRef, useState } from 'react'

import { dibujarManos } from './dibujarMano.js'
import { getHandLandmarker } from './handLandmarker.js'
import {
    crearMuestra,
    debeCerrarPorTiempo,
    fpsDe,
    frameDesdeResultado,
    idSesion,
    motivoDeDescarte,
    nombreDeFichero,
    paqueteDeMuestras,
} from './muestras.js'

/** Descarga un objeto como fichero JSON. Unico efecto sobre el DOM que sale
 * del hook; se deja aparte para poder sustituirlo en una prueba. */
export function descargarJSON(nombre, contenido) {
    const url = URL.createObjectURL(
        new Blob([JSON.stringify(contenido)], { type: 'application/json' }),
    )
    const enlace = document.createElement('a')
    enlace.href = url
    enlace.download = nombre
    enlace.click()
    URL.revokeObjectURL(url)
}

export default function useCapturaSenas({ videoRef, canvasRef, etiqueta, activo = false }) {
    const [estado, setEstado] = useState('inactivo') // inactivo | cargando | listo | error
    const [grabando, setGrabando] = useState(false)
    const [muestras, setMuestras] = useState([])
    const [manosDetectadas, setManosDetectadas] = useState(0)
    const [segundos, setSegundos] = useState(0)
    const [aviso, setAviso] = useState(null)

    // Refs para lo que lee el bucle: cambiar la etiqueta o empezar a grabar no
    // puede obligar a reiniciar el rAF ni dejarlo con valores viejos.
    const etiquetaRef = useRef(etiqueta)
    const grabandoRef = useRef(false)
    const bufferRef = useRef([])
    const inicioRef = useRef(0)
    const sesionRef = useRef(idSesion())

    useEffect(() => {
        etiquetaRef.current = etiqueta
    }, [etiqueta])

    const cerrarMuestra = useCallback(() => {
        grabandoRef.current = false
        setGrabando(false)
        setSegundos(0)

        const frames = bufferRef.current
        const duracion = performance.now() - inicioRef.current
        bufferRef.current = []

        const motivo = motivoDeDescarte(frames)
        if (motivo !== null) {
            setAviso(motivo)
            return
        }

        try {
            const muestra = crearMuestra({
                etiqueta: etiquetaRef.current,
                sesion: sesionRef.current,
                frames,
                fpsAprox: fpsDe(frames.length, duracion),
            })
            setMuestras((previas) => [...previas, muestra])
            setAviso(null)
        } catch (error) {
            setAviso(error.message)
        }
    }, [])

    const abortarGrabacion = useCallback((motivo) => {
        grabandoRef.current = false
        bufferRef.current = []
        setGrabando(false)
        setSegundos(0)
        setAviso(motivo)
    }, [])

    const alternarGrabacion = useCallback(() => {
        if (grabandoRef.current) {
            cerrarMuestra()
            return
        }
        if (!etiquetaRef.current?.trim()) {
            setAviso('Escribe el nombre de la sena antes de grabar.')
            return
        }
        setAviso(null)
        bufferRef.current = []
        inicioRef.current = performance.now()
        grabandoRef.current = true
        setGrabando(true)
    }, [cerrarMuestra])

    const borrarUltima = useCallback(() => {
        setMuestras((previas) => previas.slice(0, -1))
    }, [])

    const limpiar = useCallback(() => setMuestras([]), [])

    const exportar = useCallback(
        (descargar = descargarJSON) => {
            if (muestras.length === 0) {
                setAviso('No hay muestras que enviar todavia.')
                return null
            }
            const paquete = paqueteDeMuestras(muestras)
            descargar(nombreDeFichero(muestras), paquete)
            return paquete
        },
        [muestras],
    )

    // Si la pestana se oculta, el navegador congela requestAnimationFrame: la
    // grabacion se queda a medias y al volver el contador de tiempo ya ha
    // pasado el tope, cerrando una muestra con cuatro frames sueltos. Ademas,
    // una sena que no se estaba mirando no es dato bueno. Se descarta.
    useEffect(() => {
        if (!grabando) return undefined

        const alCambiarVisibilidad = () => {
            if (document.hidden) {
                abortarGrabacion('La grabacion se descarto al salir de la pestana.')
            }
        }

        document.addEventListener('visibilitychange', alCambiarVisibilidad)
        return () => document.removeEventListener('visibilitychange', alCambiarVisibilidad)
    }, [abortarGrabacion, grabando])

    // El bucle de video. Arranca cuando la camara esta activa y vive hasta que
    // se desmonta la pagina o se apaga la camara.
    useEffect(() => {
        if (!activo) {
            setEstado('inactivo')
            return undefined
        }

        let animacion = 0
        let cancelado = false
        let ultimoTiempo = -1
        let landmarker = null

        const pintar = (manos) => {
            const canvas = canvasRef?.current
            const video = videoRef.current
            if (!canvas || !video) return
            if (canvas.width !== video.videoWidth || canvas.height !== video.videoHeight) {
                canvas.width = video.videoWidth
                canvas.height = video.videoHeight
            }
            const ctx = canvas.getContext('2d')
            if (ctx) {
                dibujarManos(ctx, manos, {
                    ancho: canvas.width,
                    alto: canvas.height,
                    espejado: true,
                })
            }
        }

        const paso = () => {
            if (cancelado) return
            const video = videoRef.current

            if (landmarker && video && video.readyState >= 2 && video.currentTime !== ultimoTiempo) {
                ultimoTiempo = video.currentTime
                const resultado = landmarker.detectForVideo(video, performance.now())
                const frame = frameDesdeResultado(resultado, bufferRef.current.length)

                pintar(frame.manos)
                setManosDetectadas(frame.manos.length)

                if (grabandoRef.current) {
                    bufferRef.current.push(frame)
                    const transcurrido = performance.now() - inicioRef.current
                    setSegundos(transcurrido / 1000)
                    if (debeCerrarPorTiempo(transcurrido)) cerrarMuestra()
                }
            }

            animacion = requestAnimationFrame(paso)
        }

        setEstado('cargando')
        getHandLandmarker()
            .then((instancia) => {
                if (cancelado) return
                landmarker = instancia
                setEstado('listo')
            })
            .catch(() => {
                if (!cancelado) setEstado('error')
            })

        animacion = requestAnimationFrame(paso)

        return () => {
            cancelado = true
            cancelAnimationFrame(animacion)
            grabandoRef.current = false
        }
    }, [activo, canvasRef, cerrarMuestra, videoRef])

    return {
        estado,
        grabando,
        muestras,
        manosDetectadas,
        segundos,
        aviso,
        sesion: sesionRef.current,
        alternarGrabacion,
        borrarUltima,
        limpiar,
        exportar,
    }
}
