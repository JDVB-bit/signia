/** 🔐 Acceso a localStorage / sessionStorage que nunca rompe la app.
 *
 * En modo privado, con cookies bloqueadas o dentro de algunos iframes, solo
 * *tocar* `window.localStorage` ya lanza una excepcion. Recordar preferencias es
 * una comodidad: si no se puede, la app sigue funcionando sin recordar nada.
 */

/** Devuelve el almacen pedido o null si el navegador no deja usarlo. */
function obtenerAlmacen(nombre) {
    try {
        return typeof window === 'undefined' ? null : window[nombre]
    } catch {
        return null
    }
}

function leer(nombreAlmacen, clave) {
    try {
        return obtenerAlmacen(nombreAlmacen)?.getItem(clave) ?? null
    } catch {
        return null
    }
}

function guardar(nombreAlmacen, clave, valor) {
    try {
        obtenerAlmacen(nombreAlmacen)?.setItem(clave, valor)
    } catch {
        // Cuota llena o almacen bloqueado: se pierde el recuerdo, no la funcionalidad
    }
}

/** Persiste entre visitas. */
export const leerLocal = (clave) => leer('localStorage', clave)
export const guardarLocal = (clave, valor) => guardar('localStorage', clave, valor)

/** Se olvida al cerrar la pestaña. */
export const leerDeSesion = (clave) => leer('sessionStorage', clave)
export const guardarEnSesion = (clave, valor) => guardar('sessionStorage', clave, valor)
