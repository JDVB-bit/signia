export const THEME_STORAGE_KEY = 'signia-theme'

/** Calcula si el tema oscuro deberia estar activo (preferencia guardada,
 * o si no hay ninguna, la preferencia del sistema). */
export function calcularTemaOscuro() {
    if (typeof window === 'undefined') return false
    const guardado = localStorage.getItem(THEME_STORAGE_KEY)
    if (guardado) return guardado === 'dark'
    return window.matchMedia('(prefers-color-scheme: dark)').matches
}

/** Aplica la clase .dark al <html> ANTES de que se monte cualquier
 * componente, para que la pantalla de carga (y todo lo demas) ya nazca
 * con los colores correctos del tema, sin parpadeos. */
export function aplicarTemaInicial() {
    const oscuro = calcularTemaOscuro()
    document.documentElement.classList.toggle('dark', oscuro)
    return oscuro
}
