import senasPersona1 from '../../assets/senas-persona1.jpg'
import senasPersona2 from '../../assets/senas-persona2.jpg'
import senasPersona3 from '../../assets/senas-persona3.jpg'
import ImageBelt from '../componentes/contenido/ImageBelt'
import InfoBubble from '../componentes/contenido/InfoBubble'
import SectionCard from '../componentes/contenido/SectionCard'
import Typewriter from '../componentes/contenido/Typewriter'
import PageLayout from '../componentes/layout/PageLayout'
import TituloAnimado from '../componentes/layout/TituloAnimado'

const TITULO = 'Traductor de lengua de señas con Inteligencia Artificial'

const TEXTO_ALTERNATIVO_IMAGEN = 'Persona haciendo una seña en LSE'
const IMAGENES_CARRUSEL = [senasPersona1, senasPersona2, senasPersona3].map((src) => ({
    src,
    alt: TEXTO_ALTERNATIVO_IMAGEN,
}))

/** Pagina de inicio: que es SignIA, su mision y sus herramientas. */
export default function Inicio() {
    return (
        <PageLayout>
            <TituloAnimado texto={TITULO} />

            {/* Fila 1: "¿Qué es?" siempre junto al carrusel de imagenes */}
            <div className="grid grid-cols-1 items-center gap-8 lg:grid-cols-2">
                <SectionCard title="¿Qué es?">
                    <Typewriter
                        className="mt-3 leading-relaxed"
                        text="SignIA es una aplicación web que traduce la Lengua de Signos Española (LSE) a texto en tiempo real, usando la cámara del dispositivo. Está pensada para acercar la comunicación entre personas sordas o con discapacidad auditiva y personas oyentes que no conocen la lengua de señas, sin necesidad de un intérprete presente."
                    />
                    <InfoBubble label="Más sobre qué es SignIA">
                        <p>
                            Al usar SignIA, la persona simplemente se coloca frente a la cámara y hace las
                            señas con normalidad; la aplicación las reconoce y muestra el texto
                            correspondiente de forma inmediata, directamente en el navegador y sin instalar
                            nada. Por ahora, SignIA reconoce frases cortas (de hasta 5 palabras) en LSE,
                            como una primera versión pensada para crecer con el tiempo hacia un vocabulario
                            más amplio.
                        </p>
                        <p className="text-sm opacity-80">
                            Proyecto académico desarrollado por <strong>Edy Avila</strong>,{' '}
                            <strong>Juan Vieda</strong> y <strong>Andersson Castro</strong>.
                        </p>
                    </InfoBubble>
                </SectionCard>

                <section className="mx-auto h-56 w-full max-w-md overflow-hidden rounded-lg sm:h-64">
                    <ImageBelt images={IMAGENES_CARRUSEL} />
                </section>
            </div>

            {/* Fila 2: Misión y Herramientas, distinto ancho pero misma altura */}
            <div className="grid grid-cols-1 items-stretch gap-10 lg:grid-cols-12">
                <SectionCard title="Misión" className="flex flex-col lg:col-span-7 lg:p-12">
                    <Typewriter
                        className="mt-3 leading-relaxed"
                        text="Acercar la Lengua de Signos Española a cualquier persona, en cualquier momento, sin que la comunicación dependa de que ambas partes compartan el mismo idioma o sistema de señas. Buscamos que traducir LSE sea tan simple como abrir una página web."
                    />
                    <InfoBubble label="Más sobre nuestra misión">
                        <p>
                            Queremos que SignIA sea útil en situaciones cotidianas — la atención al
                            público, un salón de clases, o simplemente una conversación entre amigos y
                            familiares — sin costo ni curva de aprendizaje para quien la usa. Más allá de
                            la traducción en sí, aspiramos a que este sea un primer paso hacia
                            herramientas más accesibles para la comunidad sorda hispanohablante.
                        </p>
                    </InfoBubble>
                </SectionCard>

                <SectionCard title="Herramientas" className="flex flex-col lg:col-span-5">
                    <Typewriter
                        className="mt-3 leading-relaxed"
                        text="SignIA ofrece un traductor en tiempo real que convierte señas en texto apenas se realizan frente a la cámara, sin registros, descargas ni configuración previa: se abre la página y se empieza a traducir."
                    />
                    <InfoBubble label="Ver todas las herramientas">
                        <ul className="list-disc space-y-2 pl-5">
                            <li>
                                <strong>Traducción instantánea:</strong> el texto aparece en pantalla
                                mientras se hacen las señas.
                            </li>
                            <li>
                                <strong>Sin instalación:</strong> funciona directamente desde el
                                navegador, en computador o celular.
                            </li>
                            <li>
                                <strong>Frases de hasta 5 palabras</strong> en esta primera versión.
                            </li>
                        </ul>
                    </InfoBubble>
                </SectionCard>
            </div>
        </PageLayout>
    )
}
