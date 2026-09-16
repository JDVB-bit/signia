import { useEffect, useRef, useState } from 'react'

export const CAMERA_PERMISO_KEY = 'signia-camera-permiso'

/** Rectangulo reutilizable que pide y muestra el video en vivo de la
 * camara del dispositivo (lo usan tanto Entrenamiento como Traduccion).
 * Guarda en sessionStorage si el usuario ya concedio el permiso en esta
 * misma visita, para activar la camara sola al alternar entre paginas sin
 * mostrarle el boton de nuevo; se olvida solo al cerrar la pestaña, asi que
 * en una visita nueva siempre vuelve a pedirse con el boton. El permiso
 * real lo sigue controlando el navegador. */
export default function CameraFeed({
    className = '',
    mirrored = true,
    videoRef: videoRefExterno = null,
    onEstado = null,
    resaltado = false,
    children = null,
}) {
    const videoRefInterno = useRef(null)
    // Quien necesite el <video> (el bucle de captura) pasa su propia ref; si
    // no, el componente usa la suya y se comporta como antes.
    const videoRef = videoRefExterno ?? videoRefInterno
    const streamRef = useRef(null)
    const [estado, setEstado] = useState('inicial') // inicial | solicitando | activa | denegada | no-soportada

    const activarCamara = async () => {
        if (!navigator.mediaDevices?.getUserMedia) {
            setEstado('no-soportada')
            return
        }

        setEstado('solicitando')
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true })
            streamRef.current = stream
            if (videoRef.current) videoRef.current.srcObject = stream
            setEstado('activa')
            sessionStorage.setItem(CAMERA_PERMISO_KEY, 'concedido')
        } catch {
            setEstado('denegada')
            sessionStorage.setItem(CAMERA_PERMISO_KEY, 'denegado')
        }
    }

    useEffect(() => {
        if (sessionStorage.getItem(CAMERA_PERMISO_KEY) === 'concedido') activarCamara()

        return () => streamRef.current?.getTracks().forEach((track) => track.stop())
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    useEffect(() => {
        onEstado?.(estado)
    }, [estado, onEstado])

    return (
        <div
            className={`relative flex items-center justify-center overflow-hidden rounded-lg bg-surface transition-shadow ${resaltado ? 'ring-4 ring-secondary' : ''} ${className}`}
        >
            <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className={`h-full w-full object-cover ${mirrored ? '-scale-x-100' : ''} ${estado === 'activa' ? '' : 'hidden'}`}
            />

            {/* Capa para pintar encima del video (el esqueleto de la mano).
                No intercepta clicks: el video sigue siendo el que manda. */}
            {estado === 'activa' && children && (
                <div className="pointer-events-none absolute inset-0">{children}</div>
            )}

            {estado !== 'activa' && (
                <div className="flex flex-col items-center gap-3 p-6 text-center">
                    {estado === 'no-soportada' && (
                        <p className="text-sm opacity-80">
                            Este navegador no permite acceder a la camara.
                        </p>
                    )}
                    {estado === 'denegada' && (
                        <p className="text-sm opacity-80">
                            Se denego el acceso a la camara. Habilitalo desde los permisos
                            del navegador para el sitio y volve a intentar.
                        </p>
                    )}
                    {estado === 'solicitando' && (
                        <p className="text-sm opacity-80">Solicitando acceso a la camara...</p>
                    )}
                    {(estado === 'inicial' || estado === 'denegada') && (
                        <button
                            type="button"
                            onClick={activarCamara}
                            className="rounded-md bg-brand px-4 py-2 text-sm font-semibold text-white transition-opacity hover:opacity-90"
                        >
                            Activar camara
                        </button>
                    )}
                </div>
            )}
        </div>
    )
}
