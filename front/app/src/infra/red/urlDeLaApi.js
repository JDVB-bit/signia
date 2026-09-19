/** 🌐 Donde vive la API de SignIA.
 *
 * Una sola fuente para toda la app, igual que `rutas.js` con las rutas del
 * sitio. En desarrollo apunta al backend local; en el despliegue se cambia con
 * la variable `VITE_API_URL`, sin tocar codigo (plan, independencia del
 * despliegue).
 */

/** El backend en local, el que arranca `uvicorn app.main:app`. */
export const URL_API_POR_DEFECTO = 'http://localhost:8000'

/** Endpoints que consume el front, relativos a la base. */
export const ENDPOINTS = Object.freeze({
    MUESTRAS: '/muestras',
    SENAS: '/senas',
    SALUD: '/salud',
})

/** Base de la API: la variable de entorno si existe, el local si no. */
export function baseDeLaApi(entorno = import.meta.env) {
    const configurada = entorno?.VITE_API_URL
    return typeof configurada === 'string' && configurada ? configurada.replace(/\/$/, '') : URL_API_POR_DEFECTO
}

/** URL absoluta de un endpoint. */
export function urlDe(endpoint, entorno = import.meta.env) {
    return `${baseDeLaApi(entorno)}${endpoint}`
}
