import { useState } from "react"
import PageLayout from "../utils/PageLayout"
import CameraFeed from "../utils/CameraFeed"
import Button from "../utils/Button"

export default function Traduccion() {
    // TODO: esto lo va a actualizar el pipeline de reconocimiento cuando exista.
    const [traduccion, setTraduccion] = useState("")

    const handleTraducir = () => {
        // TODO: disparar el reconocimiento de senas y pedirle la traduccion al backend.
    }

    return (
        <PageLayout>
            <h2 className="text-center text-4xl font-extrabold tracking-tight text-brand drop-shadow-sm sm:text-5xl lg:text-6xl">
                Traductor
            </h2>

            {/*Mismos 2 bloques del mismo tamaño que Entrenamiento: la camara,
                y al lado el boton de traducir (mitad de arriba, empieza a la
                misma altura que la camara) + la caja con la traduccion que
                devuelve el backend (mitad de abajo, hasta el final de la camara).*/}
            <div className="grid w-full grid-cols-1 gap-8 sm:grid-cols-2">
                <div className="h-[27rem] w-full">
                    {/*Camara para capturar las senas a traducir en tiempo real.*/}
                    <CameraFeed className="h-full w-full" />
                </div>

                <section className="grid h-[27rem] w-full grid-rows-2 gap-6 rounded-2xl bg-surface p-8">
                    <div className="flex items-center justify-center">
                        {/*10% mas grande que los botones de Entrenamiento (size="lg").*/}
                        <Button variant="primary" size="lg" onClick={handleTraducir}>
                            Traducir
                        </Button>
                    </div>

                    <div className="flex items-center justify-center text-center text-brand bg-bg rounded-lg">
                        {traduccion || "La traduccion aparecera aqui"}
                    </div>
                </section>
            </div>
        </PageLayout>
    )
}
