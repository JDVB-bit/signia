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

            {/*Camara a la izquierda, con un margen antes del borde (~15% del
                ancho renderizado), y los controles del pipeline a la derecha.*/}
            <div className="flex flex-col gap-10 lg:flex-row">
                <div className="hidden shrink-0 lg:block lg:w-[15%]" aria-hidden="true" />

                <section className="aspect-video w-full lg:w-[35%] lg:shrink-0">
                    {/*Camara para que el usuario practique las senas frente a ella.
                        El resto del modulo (validacion, guia, etc.) queda pendiente.*/}
                    <CameraFeed className="h-full w-full" />
                </section>

                <section className="flex w-full flex-col gap-6 lg:w-[35%]">
                    {/*Controles del pipeline: nombre de la sena a capturar,
                        contador de muestras tomadas, y las acciones de
                        entrenar/enviar.*/}
                    <div>
                        <label htmlFor="nombre-sena" className="block text-sm font-medium">
                            Nombre seña
                        </label>
                        <input
                            id="nombre-sena"
                            type="text"
                            value={nombreSena}
                            onChange={(event) => setNombreSena(event.target.value)}
                            placeholder="Ingresa el nombre de la seña que estas realizando"
                            className="mt-1 w-full rounded-md border border-secondary/40 bg-surface px-3 py-2 text-sm"
                        />
                    </div>

                    {/*Contador de muestras, a modo de "boton" llamativo con el
                        color principal de la paleta contraria.*/}
                    <div className="flex w-fit flex-col items-center gap-1 rounded-2xl bg-brand-inverso px-8 py-4 text-white shadow-md">
                        <span className="text-4xl font-extrabold leading-none">{muestras}</span>
                        <span className="text-xs font-medium uppercase tracking-wide opacity-90">
                            Muestras tomadas
                        </span>
                    </div>

                    <div className="flex gap-3">
                        <Button variant="primary" onClick={handleEntrenar}>
                            Entrenar
                        </Button>
                        <Button variant="secondary" onClick={handleEnviar}>
                            Enviar
                        </Button>
                    </div>
                </section>
            </div>
        </PageLayout>
    )
}
