/** ⬇️ Descarga un objeto como fichero `.json` desde el navegador. */

const TIPO_MIME_JSON = 'application/json'

/** Crea un enlace temporal al contenido serializado y lo pulsa. */
export function descargarJson(nombre, contenido) {
    const url = URL.createObjectURL(new Blob([JSON.stringify(contenido)], { type: TIPO_MIME_JSON }))
    const enlace = document.createElement('a')
    enlace.href = url
    enlace.download = nombre
    enlace.click()
    // La URL ya no hace falta tras iniciar la descarga: se libera la memoria del Blob
    URL.revokeObjectURL(url)
}
