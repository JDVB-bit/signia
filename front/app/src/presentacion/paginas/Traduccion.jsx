import CameraFeed from '../componentes/camara/CameraFeed'
import Button from '../componentes/comunes/Button'
import PageLayout from '../componentes/layout/PageLayout'
import TituloPagina from '../componentes/layout/TituloPagina'

/** Modo CONTINUO: el producto, traducir una frase seguida (Fases 6 y 6b del plan).
 *
 * Todavia no hay modelo entrenado, asi que la pagina no finge traducir: el
 * boton queda deshabilitado y se explica por que. Cuando exista el pipeline,
 * "Traducir" pasara a ser un interruptor de sesion y la caja mostrara las glosas.
 */
export default function Traduccion() {
    return (
        <PageLayout>
            <TituloPagina>Traductor</TituloPagina>

            {/* Mismos dos bloques que Entrenamiento: la camara y el panel de traduccion */}
            <div className="grid w-full grid-cols-1 gap-8 sm:grid-cols-2">
                <div className="h-[27rem] w-full">
                    <CameraFeed className="h-full w-full" />
                </div>

                <section className="grid h-[27rem] w-full grid-rows-2 gap-6 rounded-2xl bg-surface p-8">
                    <div className="flex items-center justify-center">
                        <Button variant="primary" size="lg" disabled>
                            Traducir
                        </Button>
                    </div>

                    <div
                        className="flex items-center justify-center rounded-lg bg-bg p-4 text-center text-brand"
                        aria-live="polite"
                    >
                        El traductor estará disponible cuando haya un modelo entrenado. Mientras tanto,
                        puedes ayudar grabando señas en Entrenamiento.
                    </div>
                </section>
            </div>
        </PageLayout>
    )
}
