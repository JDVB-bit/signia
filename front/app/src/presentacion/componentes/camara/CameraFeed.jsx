import { useEffect, useRef } from 'react'

import useCamara, { ESTADOS_CAMARA } from '../../hooks/useCamara'
import AvisoEstadoCamara from './AvisoEstadoCamara'

/** Recuadro reutilizable con el video en vivo de la camara (Entrenamiento y Traduccion).
 *
 * - `videoRef`: ref externa al <video> para quien necesite leer sus frames.
 * - `onEstado`: se notifica cada cambio de estado de la camara.
 * - `resaltado`: marca el borde (por ejemplo, mientras se graba).
 * - `children`: capa superpuesta al video (el esqueleto de la mano).
 */
export default function CameraFeed({
    className = '',
    mirrored = true,
    videoRef: videoRefExterno = null,
    onEstado = null,
    resaltado = false,
    children = null,
}) {
    const videoRefInterno = useRef(null)
    const videoRef = videoRefExterno ?? videoRefInterno
    const { estado, activar } = useCamara(videoRef)
    const activa = estado === ESTADOS_CAMARA.ACTIVA

    useEffect(() => {
        onEstado?.(estado)
    }, [estado, onEstado])

    return (
        <div
            className={`relative flex items-center justify-center overflow-hidden rounded-lg bg-surface transition-shadow ${resaltado ? 'ring-4 ring-secondary' : ''} ${className}`}
        >
            {/* El <video> existe siempre (oculto si hace falta) para que la ref este lista al activar */}
            <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className={`h-full w-full object-cover ${mirrored ? '-scale-x-100' : ''} ${activa ? '' : 'hidden'}`}
            />

            {/* Capa superpuesta: no intercepta clicks, el video sigue mandando */}
            {activa && children && <div className="pointer-events-none absolute inset-0">{children}</div>}

            {!activa && <AvisoEstadoCamara estado={estado} alActivar={activar} />}
        </div>
    )
}
