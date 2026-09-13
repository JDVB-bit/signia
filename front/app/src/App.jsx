import { Fragment } from "react"
import "./App.css"
import PageLayout from "./utils/PageLayout"
import Typewriter from "./utils/Typewriter"
import SectionCard from "./utils/SectionCard"
import InfoBubble from "./utils/InfoBubble"
import ImageBelt from "./utils/ImageBelt"
import senasPersona1 from "./assets/senas-persona1.jpg"
import senasPersona2 from "./assets/senas-persona2.jpg"
import senasPersona3 from "./assets/senas-persona3.jpg"

const TITULO = "Traductor de lenguaje de señas con Inteligencia Artificial"
const PALABRAS_TITULO = TITULO.split(" ")

const IMAGENES_CARRUSEL = [
    { src: senasPersona1, alt: "Persona haciendo una sena en LSE" },
    { src: senasPersona2, alt: "Persona haciendo una sena en LSE" },
    { src: senasPersona3, alt: "Persona haciendo una sena en LSE" },
]

export default function App() {

    return (
        <PageLayout>
            {/*Titulo principal con efecto de aparicion tipo "polvo", palabra a palabra*/}
            <h2 className="text-center text-4xl font-extrabold tracking-tight text-brand drop-shadow-sm sm:text-5xl lg:text-6xl">
                {PALABRAS_TITULO.map((palabra, index) => (
                    <Fragment key={`${palabra}-${index}`}>
                        <span
                            className="animate-dust-in inline-block"
                            style={{ animationDelay: `${index * 90}ms` }}
                        >
                            {palabra}
                        </span>
                        {index < PALABRAS_TITULO.length - 1 ? " " : ""}
                    </Fragment>
                ))}
            </h2>
            {/*Fila 1: "Que es" va siempre junto a la seccion de imagenes*/}
            <div className="grid grid-cols-1 items-center gap-8 lg:grid-cols-2">
                <SectionCard title="¿Qué es?">
                    <Typewriter
                        className="mt-3 leading-relaxed"
                        text="SignIA es una aplicacion web que traduce la Lengua de Señas Espanola (LSE) a texto en tiempo real, usando la camara del dispositivo. Esta pensada para acercar la comunicacion entre personas sordas o con discapacidad auditiva y personas oyentes que no conocen la lengua de señas, sin necesidad de un interprete presente."
                    />
                    <InfoBubble label="Mas sobre que es SignIA">
                        <p>
                            Al usar SignIA, la persona simplemente se coloca frente a la camara y hace las
                            señas con normalidad; la aplicacion las reconoce y muestra el texto
                            correspondiente de forma inmediata, directamente en el navegador y sin instalar
                            nada. Por ahora, SignIA reconoce frases cortas (de hasta 5 palabras) en LSE,
                            como una primera version pensada para crecer con el tiempo hacia un vocabulario
                            mas amplio.
                        </p>
                        <p className="text-sm opacity-80">
                            Proyecto academico desarrollado por <strong>Edy Avila</strong>,{" "}
                            <strong>Juan Vieda</strong> y <strong>Andersson Castro</strong>.
                        </p>
                    </InfoBubble>
                </SectionCard>

                <section className="mx-auto h-56 w-full max-w-md overflow-hidden rounded-lg sm:h-64">
                    {/*Cinturon de imagenes: cada una se ve ~5s y la siguiente empuja a la
                        anterior hacia la izquierda con una transicion fluida.*/}
                    <ImageBelt images={IMAGENES_CARRUSEL} />
                </section>
            </div>

            {/*Fila 2: Mision y Herramientas, con distinto ancho pero misma altura
                (se estiran parejo dentro de la fila del grid)*/}
            <div className="grid grid-cols-1 items-stretch gap-10 lg:grid-cols-12">
                <SectionCard title="Misión" className="flex flex-col lg:col-span-7 lg:p-12">
                    <Typewriter
                        className="mt-3 leading-relaxed"
                        text="Acercar la Lengua de Señas Espanola a cualquier persona, en cualquier momento, sin que la comunicacion dependa de que ambas partes compartan el mismo idioma o sistema de señas. Buscamos que traducir LSE sea tan simple como abrir una pagina web."
                    />
                    <InfoBubble label="Mas sobre nuestra mision">
                        <p>
                            Queremos que SignIA sea util en situaciones cotidianas — la atencion al
                            publico, un salon de clases, o simplemente una conversacion entre amigos y
                            familiares — sin costo ni curva de aprendizaje para quien la usa. Mas alla de
                            la traduccion en si, aspiramos a que este sea un primer paso hacia
                            herramientas mas accesibles para la comunidad sorda hispanohablante.
                        </p>
                    </InfoBubble>
                </SectionCard>

                <SectionCard title="Herramientas" className="flex flex-col lg:col-span-5">
                    <Typewriter
                        className="mt-3 leading-relaxed"
                        text="SignIA ofrece un traductor en tiempo real que convierte señas en texto apenas se realizan frente a la camara, sin registros, descargas ni configuracion previa: se abre la pagina y se empieza a traducir."
                    />
                    <InfoBubble label="Ver todas las herramientas">
                        <ul className="list-disc space-y-2 pl-5">
                            <li>
                                <strong>Traduccion instantanea:</strong> el texto aparece en pantalla
                                mientras se hacen las señas.
                            </li>
                            <li>
                                <strong>Sin instalacion:</strong> funciona directamente desde el
                                navegador, en computador o celular.
                            </li>
                            <li>
                                <strong>Frases de hasta 5 palabras</strong> en esta primera version.
                            </li>
                        </ul>
                    </InfoBubble>
                </SectionCard>
            </div>
        </PageLayout>
    );
}
