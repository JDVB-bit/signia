/** Titulo principal de una pagina, con el mismo estilo en todo el sitio. */
export const ESTILOS_TITULO_PAGINA =
    'text-center text-4xl font-extrabold tracking-tight text-brand drop-shadow-sm sm:text-5xl lg:text-6xl'

export default function TituloPagina({ children }) {
    return <h2 className={ESTILOS_TITULO_PAGINA}>{children}</h2>
}
