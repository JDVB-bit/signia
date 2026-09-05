import { useEffect, useState } from 'react'
import { THEME_STORAGE_KEY, calcularTemaOscuro } from './theme'

export default function ThemeToggle() {
    const [dark, setDark] = useState(calcularTemaOscuro)

    useEffect(() => {
        document.documentElement.classList.toggle('dark', dark)
        localStorage.setItem(THEME_STORAGE_KEY, dark ? 'dark' : 'light')
    }, [dark])

    return (
        <button
            type="button"
            onClick={() => setDark((prev) => !prev)}
            aria-pressed={dark}
            aria-label="Cambiar paleta de colores"
            className="rounded-full px-4 py-2 text-sm font-medium text-secondary transition-opacity hover:opacity-80"
        >
            {dark ? '☀️' : '🌙'}
        </button>
    )
}
