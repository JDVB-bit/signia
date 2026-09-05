import { useEffect, useState } from 'react'
import CarouselImage from './CarouselImage'

const TIEMPO_VISIBLE_MS = 7500
const DURACION_TRANSICION_MS = 700

/** Efecto "cinturon": las imagenes se muestran una a la vez, cada una unos
 * 5 segundos, y al pasar a la siguiente esta empuja a la anterior hacia la
 * izquierda con una animacion fluida. Al llegar a la ultima, vuelve a la
 * primera sin salto brusco (se agrega una copia de la primera al final del
 * cinturon y se hace un reset invisible al llegar a ella). */
export default function ImageBelt({ images }) {
    const [index, setIndex] = useState(0)
    const [conTransicion, setConTransicion] = useState(true)

    const cinturon = [...images, images[0]]

    useEffect(() => {
        const id = setInterval(() => {
            setIndex((prev) => prev + 1)
        }, TIEMPO_VISIBLE_MS)
        return () => clearInterval(id)
    }, [])

    useEffect(() => {
        if (index !== images.length) return undefined

        const id = setTimeout(() => {
            setConTransicion(false)
            setIndex(0)
        }, DURACION_TRANSICION_MS)
        return () => clearTimeout(id)
    }, [index, images.length])

    useEffect(() => {
        if (conTransicion) return undefined
        const id = requestAnimationFrame(() => setConTransicion(true))
        return () => cancelAnimationFrame(id)
    }, [conTransicion])

    return (
        <div className="h-full w-full overflow-hidden rounded-lg">
            <div
                className="flex h-full"
                style={{
                    transform: `translateX(-${index * 100}%)`,
                    transition: conTransicion
                        ? `transform ${DURACION_TRANSICION_MS}ms cubic-bezier(0.65, 0, 0.35, 1)`
                        : 'none',
                }}
            >
                {cinturon.map((imagen, i) => (
                    <CarouselImage key={`${imagen.alt}-${i}`} src={imagen.src} alt={imagen.alt} />
                ))}
            </div>
        </div>
    )
}
