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
            <section className="mx-auto aspect-video w-full max-w-2xl">
                {/*Camara para que el usuario practique las senas frente a ella.
                    El resto del modulo (validacion, guia, etc.) queda pendiente.*/}
                <CameraFeed className="h-full w-full" />
            </section>

            <section className="mx-auto w-full max-w-2xl space-y-4">
                {/*Controles del pipeline de entrenamiento: nombre de la sena a
                    capturar, contador de muestras tomadas, y las acciones de
                    entrenar/enviar. Sin estilos definitivos todavia.*/}
                <div>
                    <label htmlFor="nombre-sena" className="block text-sm font-medium">
                        Nombre seña
                    </label>
                    <input
                        id="nombre-sena"
                        type="text"
                        value={nombreSena}
                        onChange={(event) => setNombreSena(event.target.value)}
                        placeholder="Ej: Hola"
                        className="mt-1 w-full rounded-md border border-secondary/40 bg-surface px-3 py-2 text-sm"
                    />
                </div>

                <p className="text-sm">
                    Muestras tomadas: <span className="font-semibold">{muestras}</span>
                </p>

                <div className="flex gap-3">
                    <Button variant="primary" onClick={handleEntrenar}>
                        Entrenar
                    </Button>
                    <Button variant="secondary" onClick={handleEnviar}>
                        Enviar
                    </Button>
                </div>
            </section>
        </PageLayout>
    )
}
