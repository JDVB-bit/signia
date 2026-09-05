/** Una sola imagen del cinturon. Recibe la imagen como prop (src/alt) para que
 * ImageBelt solo se preocupe de la posicion/animacion, no de como se pinta
 * cada elemento. */
export default function CarouselImage({ src, alt }) {
    return (
        <div className="h-full w-full shrink-0 basis-full px-1">
            <img src={src} alt={alt} className="h-full w-full rounded-lg object-cover" />
        </div>
    )
}
