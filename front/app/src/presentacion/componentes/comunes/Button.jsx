/** Colores por variante, usando solo la paleta de `index.css`. */
const ESTILOS_POR_VARIANTE = {
    // Acción principal: el color de resalte con el texto alterno encima
    primary: 'bg-secondary text-brand-inverso',
    // Acción secundaria: el color de las secciones con el texto normal
    secondary: 'bg-surface text-brand',
}

/** "lg" es un 10% mas grande que "md" (lo usa, por ejemplo, el boton de Traducir). */
const ESTILOS_POR_TAMANO = {
    md: 'px-8 py-4 text-base',
    lg: 'px-[2.2rem] py-[1.1rem] text-[1.1rem]',
}

const ESTILOS_HABILITADO = 'hover:opacity-90'
const ESTILOS_DESHABILITADO = 'cursor-not-allowed opacity-50'

/** Boton comun del sitio. Siempre `type="button"` para no enviar formularios por accidente. */
export default function Button({ children, variant = 'primary', size = 'md', onClick, disabled = false }) {
    const estadoVisual = disabled ? ESTILOS_DESHABILITADO : ESTILOS_HABILITADO
    const className = `rounded-md font-semibold transition-opacity ${estadoVisual} ${ESTILOS_POR_TAMANO[size]} ${ESTILOS_POR_VARIANTE[variant]}`

    return (
        <button type="button" className={className} onClick={onClick} disabled={disabled}>
            {children}
        </button>
    )
}
