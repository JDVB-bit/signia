import { useEffect, useState } from 'react'

import CarouselImage from './CarouselImage'

const TIEMPO_VISIBLE_MS = 7500
const DURACION_TRANSICION_MS = 700
const CURVA_TRANSICION = 'cubic-bezier(0.65, 0, 0.35, 1)'
const PORCENTAJE_POR_IMAGEN = 100

/** Carrusel tipo "cinturon": cada imagen se ve unos segundos y la siguiente la empuja a la izquierda.
 *
 * Para volver al principio sin salto, se añade una copia de la primera imagen
 * al final; al llegar a ella se salta sin transicion (invisible) al indice 0.
 */
export default function ImageBelt({ images }) {
    const [indice, setIndice] = useState(0)
    const [conTransicion, setConTransicion] = useState(true)

    const cinturon = [...images, images[0]]

    // ⏭️ Avanza una imagen cada TIEMPO_VISIBLE_MS
    useEffect(() => {
        const intervalo = setInterval(() => setIndice((previo) => previo + 1), TIEMPO_VISIBLE_MS)
        return () => clearInterval(intervalo)
    }, [])

    // 🔁 Al llegar a la copia, cuando termina la animacion, salta al inicio sin transicion
    useEffect(() => {
        if (indice !== images.length) return undefined
        const espera = setTimeout(() => {
            setConTransicion(false)
            setIndice(0)
        }, DURACION_TRANSICION_MS)
        return () => clearTimeout(espera)
    }, [indice, images.length])

    // Se reactiva la transicion en el frame siguiente, ya con el salto aplicado
    useEffect(() => {
        if (conTransicion) return undefined
        const frame = requestAnimationFrame(() => setConTransicion(true))
        return () => cancelAnimationFrame(frame)
    }, [conTransicion])

    return (
        <div className="h-full w-full overflow-hidden rounded-lg">
            <div
                className="flex h-full"
                style={{
                    transform: `translateX(-${indice * PORCENTAJE_POR_IMAGEN}%)`,
                    transition: conTransicion ? `transform ${DURACION_TRANSICION_MS}ms ${CURVA_TRANSICION}` : 'none',
                }}
            >
                {cinturon.map((imagen, posicion) => (
                    <CarouselImage key={`${imagen.alt}-${posicion}`} src={imagen.src} alt={imagen.alt} />
                ))}
            </div>
        </div>
    )
}
