// Solo los 5 colores de la paleta: primary usa "secondary" (el color
// alterno para resaltar) de fondo con "brand-inverso" (texto alterno)
// encima; secondary usa "surface" (el color secundario) de fondo con
// "brand" (el color de texto normal) encima.
const COLOR_STYLES = {
    primary: 'bg-secondary text-brand-inverso',
    secondary: 'bg-surface text-brand',
    sidebar: '',
    burble: '',
    stop: '',
    default: ''
}

// "lg" es un 10% mas grande que el tamaño por defecto (lo usa, por
// ejemplo, el boton "Traducir" de la pagina de Traduccion).
const SIZE_STYLES = {
    default: 'px-8 py-4 text-base',
    lg: 'px-[2.2rem] py-[1.1rem] text-[1.1rem]',
}

function Button({ children, variant = "default", size = "default", onClick }) {
    const className = `rounded-md font-semibold transition-opacity hover:opacity-90 ${SIZE_STYLES[size]} ${COLOR_STYLES[variant]}`

    return (
        <button className={className} onClick={onClick}>
            {variant === 'sidebar' ? (
                <span className=''></span>
            ) : (
                children
            )}
        </button>
    )
}

export default Button
