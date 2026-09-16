import useTema from '../../hooks/useTema'

const ICONO_PASAR_A_CLARO = '☀️'
const ICONO_PASAR_A_OSCURO = '🌙'

/** Boton del header que alterna la paleta clara/oscura (el icono muestra a cual se pasa). */
export default function ThemeToggle() {
    const { oscuro, alternarTema } = useTema()

    return (
        <button
            type="button"
            onClick={alternarTema}
            aria-pressed={oscuro}
            aria-label="Cambiar paleta de colores"
            className="rounded-full px-4 py-2 text-sm font-medium text-secondary transition-opacity hover:opacity-80"
        >
            {oscuro ? ICONO_PASAR_A_CLARO : ICONO_PASAR_A_OSCURO}
        </button>
    )
}
