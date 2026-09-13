import { useState } from "react"
import PageLayout from "../utils/PageLayout"
import CameraFeed from "../utils/CameraFeed"
import Button from "../utils/Button"

export default function Entrenamiento() {
    const [nombreSena, setNombreSena] = useState("")
    // TODO: esto lo va a actualizar el pipeline de captura de muestras cuando exista.
    const [muestras, setMuestras] = useState(0)

    const handleEntrenar = () => {
        // TODO: disparar el pipeline de captura/entrenamiento con la camara.
    }

    const handleEnviar = () => {
        // TODO: enviar las muestras capturadas (nombreSena + muestras) al backend.
    }

    return (
        <PageLayout>
            <h2 className="text-center text-4xl font-extrabold tracking-tight text-brand drop-shadow-sm sm:text-5xl lg:text-6xl">
                Entrenamiento
            </h2>

            {/*Solo 2 bloques del mismo tamaño (misma fila de grilla, se
                estiran parejo): la camara, y una sola seccion que agrupa
                nombre de la sena + contador + botones.*/}
            <div className="mx-auto grid w-full max-w-6xl grid-cols-1 gap-8 sm:grid-cols-2">
                <div className="h-[27rem] w-full">
                    {/*Camara para que el usuario practique las senas frente a ella.
                        El resto del modulo (validacion, guia, etc.) queda pendiente.*/}
                    <CameraFeed className="h-full w-full" />
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
                        <span className="text-5xl font-extrabold leading-none">{muestras}</span>
                        <span className="text-xs font-medium uppercase tracking-wide opacity-90">
                            Muestras tomadas
                        </span>
                    </div>

                    <div className="flex justify-center gap-4">
                        <Button variant="primary" onClick={handleEntrenar}>
                            Entrenar
                        </Button>
                        <Button variant="secondary" onClick={handleEnviar}>
                            Enviar
                        </Button>
                    </div>
                </div>
            </div>
        </PageLayout>
    )
}
