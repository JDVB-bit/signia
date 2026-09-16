import { Fragment } from 'react'

import { ESTILOS_TITULO_PAGINA } from './TituloPagina'

/** Retraso entre la aparicion de una palabra y la siguiente. */
const RETRASO_ENTRE_PALABRAS_MS = 90

/** Titulo de pagina que aparece palabra a palabra con el efecto "polvo" (`animate-dust-in`). */
export default function TituloAnimado({ texto }) {
    const palabras = texto.split(' ')

    return (
        <h2 className={ESTILOS_TITULO_PAGINA}>
            {palabras.map((palabra, indice) => (
                <Fragment key={`${palabra}-${indice}`}>
                    <span
                        className="animate-dust-in inline-block"
                        style={{ animationDelay: `${indice * RETRASO_ENTRE_PALABRAS_MS}ms` }}
                    >
                        {palabra}
                    </span>
                    {/* inline-block se come los espacios: se reponen entre palabras */}
                    {indice < palabras.length - 1 ? ' ' : ''}
                </Fragment>
            ))}
        </h2>
    )
}
