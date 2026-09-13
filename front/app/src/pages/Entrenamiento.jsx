import PageLayout from "../utils/PageLayout"
import CameraFeed from "../utils/CameraFeed"

export default function Entrenamiento() {

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
        </PageLayout>
    )
}
