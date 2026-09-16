import { useCallback, useRef, useState } from 'react'

import CameraFeed from '../componentes/camara/CameraFeed'
import ContadorDeMuestras from '../componentes/captura/ContadorDeMuestras'
import IndicadorDeGrabacion from '../componentes/captura/IndicadorDeGrabacion'
import IndicadorDeManos from '../componentes/captura/IndicadorDeManos'
import Button from '../componentes/comunes/Button'
import PageLayout from '../componentes/layout/PageLayout'
import TituloPagina from '../componentes/layout/TituloPagina'
import { ESTADOS_CAMARA } from '../estados/estadosDeCamara'
import { ESTADOS_DETECTOR } from '../estados/estadosDelDetector'
import useCapturaSenas from '../hooks/useCapturaSenas'
import { mensajeDeEstadoDeCaptura } from '../textos/mensajeDeEstadoDeCaptura'

/** Modo AISLADO: el camino de captura de dato para entrenar (Fase 1 del plan).
 *
 * "Entrenar" graba UNA muestra de UNA seña (pulsar inicia; pulsar otra vez o el
 * tope de tiempo la cierra) y sube el contador. "Enviar" descarga el lote como
 * JSON; en la Fase 5 pasara a llamar al endpoint. Traducir es el modo continuo.
 */
export default function Entrenamiento() {
    const [nombreSena, setNombreSena] = useState('')
    const [camaraActiva, setCamaraActiva] = useState(false)
    const videoRef = useRef(null)
    const canvasRef = useRef(null)

    const alCambiarEstadoCamara = useCallback((estado) => setCamaraActiva(estado === ESTADOS_CAMARA.ACTIVA), [])

    const captura = useCapturaSenas({ videoRef, canvasRef, etiqueta: nombreSena, activo: camaraActiva })
    const detectorListo = captura.estado === ESTADOS_DETECTOR.LISTO
    const hayMuestras = captura.muestras.length > 0

    return (
        <PageLayout>
            <TituloPagina>Entrenamiento</TituloPagina>

            {/* Dos bloques del mismo tamaño: la camara y el panel de captura */}
            <div className="grid w-full grid-cols-1 gap-8 sm:grid-cols-2">
                <div className="h-[27rem] w-full">
                    {/* El esqueleto sobre el video permite descartar una muestra mala antes de guardarla */}
                    <CameraFeed
                        className="h-full w-full"
                        videoRef={videoRef}
                        onEstado={alCambiarEstadoCamara}
                        resaltado={captura.grabando}
                    >
                        <canvas ref={canvasRef} className="h-full w-full object-cover" />

                        <div className="absolute inset-x-0 top-0 flex items-center justify-between gap-2 p-3 text-xs font-semibold">
                            <IndicadorDeManos cantidad={captura.manosDetectadas} />
                            {captura.grabando && <IndicadorDeGrabacion segundos={captura.segundos} />}
                        </div>
                    </CameraFeed>
                </div>

                <div className="flex h-[27rem] w-full flex-col justify-between gap-6 rounded-2xl bg-surface p-8">
                    <div>
                        <label htmlFor="nombre-sena" className="block text-sm font-medium text-brand">
                            Nombre de la seña
                        </label>
                        <input
                            id="nombre-sena"
                            type="text"
                            value={nombreSena}
                            onChange={(evento) => setNombreSena(evento.target.value)}
                            placeholder="Escribe el nombre de la seña que vas a realizar"
                            className="mt-1 w-full rounded-md border border-secondary/40 bg-bg px-3 py-2 text-sm placeholder:text-brand"
                        />
                    </div>

                    <ContadorDeMuestras cantidad={captura.muestras.length} />

                    {/* min-h fijo: el texto cambia sin mover el resto del bloque */}
                    <p className="min-h-[1.5rem] text-center text-sm text-brand" aria-live="polite">
                        {mensajeDeEstadoDeCaptura({
                            aviso: captura.aviso,
                            camaraActiva,
                            estadoDetector: captura.estado,
                            sesion: captura.sesion,
                        })}
                    </p>

                    <div className="flex flex-col items-center gap-3">
                        <div className="flex justify-center gap-4">
                            <Button variant="primary" onClick={captura.alternarGrabacion} disabled={!detectorListo}>
                                {captura.grabando ? 'Detener' : 'Entrenar'}
                            </Button>
                            <Button variant="secondary" onClick={() => captura.exportar()} disabled={!hayMuestras}>
                                Enviar
                            </Button>
                        </div>

                        <button
                            type="button"
                            onClick={captura.borrarUltima}
                            disabled={!hayMuestras}
                            className="text-xs font-medium text-brand underline underline-offset-4 transition-opacity hover:opacity-80 disabled:cursor-not-allowed disabled:opacity-40"
                        >
                            Borrar última muestra
                        </button>
                    </div>
                </div>
            </div>
        </PageLayout>
    )
}
