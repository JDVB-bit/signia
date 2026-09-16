import { useCallback, useRef, useState } from "react"
import PageLayout from "../utils/PageLayout"
import CameraFeed from "../utils/CameraFeed"
import Button from "../utils/Button"
import useCapturaSenas from "../lib/useCapturaSenas"

/** Modo AISLADO: el camino de captura de dato para entrenar (Fase 1 del plan).
 *
 * "Entrenar" graba UNA muestra de UNA sena (pulsar inicia, pulsar otra vez o el
 * tope de tiempo la cierra) y sube el contador. "Enviar" descarga todas las
 * muestras acumuladas como JSON; en la Fase 5 pasara a llamar al endpoint.
 * Traducir una frase seguida es el modo continuo, y vive en `Traduccion`. */
export default function Entrenamiento() {
    const [nombreSena, setNombreSena] = useState("")
    const [camaraActiva, setCamaraActiva] = useState(false)
    const videoRef = useRef(null)
    const canvasRef = useRef(null)

    const alCambiarEstadoCamara = useCallback(
        (estado) => setCamaraActiva(estado === "activa"),
        [],
    )

    const captura = useCapturaSenas({
        videoRef,
        canvasRef,
        etiqueta: nombreSena,
        activo: camaraActiva,
    })

    const listo = captura.estado === "listo"

    return (
        <PageLayout>
            <h2 className="text-center text-4xl font-extrabold tracking-tight text-brand drop-shadow-sm sm:text-5xl lg:text-6xl">
                Entrenamiento
            </h2>

            {/*Solo 2 bloques del mismo tamaño (misma fila de grilla, se
                estiran parejo): la camara, y una sola seccion que agrupa
                nombre de la sena + contador + botones.*/}
            <div className="grid w-full grid-cols-1 gap-8 sm:grid-cols-2">
                <div className="h-[27rem] w-full">
                    {/*Camara + overlay del esqueleto de la mano: permite
                        descartar una muestra mala antes de guardarla, y ver
                        que lado (izquierda/derecha) reporta MediaPipe.*/}
                    <CameraFeed
                        className="h-full w-full"
                        videoRef={videoRef}
                        onEstado={alCambiarEstadoCamara}
                        resaltado={captura.grabando}
                    >
                        <canvas ref={canvasRef} className="h-full w-full object-cover" />

                        <div className="absolute inset-x-0 top-0 flex items-center justify-between gap-2 p-3 text-xs font-semibold">
                            <span className="rounded-full bg-brand-inverso/70 px-3 py-1 text-bg">
                                {captura.manosDetectadas === 0
                                    ? "sin manos"
                                    : `${captura.manosDetectadas} mano${captura.manosDetectadas > 1 ? "s" : ""}`}
                            </span>

                            {captura.grabando && (
                                <span className="flex items-center gap-2 rounded-full bg-secondary px-3 py-1 text-brand-inverso">
                                    <span className="h-2 w-2 animate-pulse rounded-full bg-red-500" />
                                    grabando {captura.segundos.toFixed(1)}s
                                </span>
                            )}
                        </div>
                    </CameraFeed>
                </div>

                <div className="flex h-[27rem] w-full flex-col justify-between gap-6 rounded-2xl bg-surface p-8">
                    <div>
                        <label htmlFor="nombre-sena" className="block text-sm font-medium text-brand">
                            Nombre seña
                        </label>
                        <input
                            id="nombre-sena"
                            type="text"
                            value={nombreSena}
                            onChange={(event) => setNombreSena(event.target.value)}
                            placeholder="Ingresa el nombre de la seña que estas realizando"
                            className="mt-1 w-full rounded-md border border-secondary/40 bg-bg px-3 py-2 text-sm placeholder:text-brand"
                        />
                    </div>

                    <div className="flex flex-col items-center gap-1 rounded-2xl bg-secondary p-6 text-brand-inverso shadow-md">
                        <span className="text-5xl font-extrabold leading-none">
                            {captura.muestras.length}
                        </span>
                        <span className="text-xs font-medium uppercase tracking-wide opacity-90">
                            Muestras tomadas
                        </span>
                    </div>

                    {/*Una sola linea de estado: lo que hace falta saber antes
                        de pulsar, sin mover el resto del bloque.*/}
                    <p className="min-h-[1.5rem] text-center text-sm text-brand">
                        {captura.aviso
                            ? captura.aviso
                            : !camaraActiva
                              ? "Activa la camara para empezar a grabar."
                              : captura.estado === "cargando"
                                ? "Cargando el detector de manos..."
                                : captura.estado === "error"
                                  ? "No se pudo cargar el detector de manos."
                                  : `Sesion ${captura.sesion}`}
                    </p>

                    <div className="flex flex-col items-center gap-3">
                        <div className="flex justify-center gap-4">
                            <Button
                                variant="primary"
                                onClick={captura.alternarGrabacion}
                                disabled={!listo}
                            >
                                {captura.grabando ? "Detener" : "Entrenar"}
                            </Button>
                            <Button
                                variant="secondary"
                                onClick={() => captura.exportar()}
                                disabled={captura.muestras.length === 0}
                            >
                                Enviar
                            </Button>
                        </div>

                        <button
                            type="button"
                            onClick={captura.borrarUltima}
                            disabled={captura.muestras.length === 0}
                            className="text-xs font-medium text-brand underline underline-offset-4 transition-opacity hover:opacity-80 disabled:cursor-not-allowed disabled:opacity-40"
                        >
                            Borrar ultima muestra
                        </button>
                    </div>
                </div>
            </div>
        </PageLayout>
    )
}
