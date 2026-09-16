/** 🎥 Adaptador de `getUserMedia`: abrir y cerrar el flujo de video de la camara. */

/** Solo video: el audio no aporta nada a la lengua de señas y pediria otro permiso. */
const RESTRICCIONES_DE_CAMARA = { video: true, audio: false }

export function camaraSoportada() {
    return typeof navigator !== 'undefined' && Boolean(navigator.mediaDevices?.getUserMedia)
}

/** Pide la camara al navegador; rechaza si el usuario la deniega. */
export function abrirCamara() {
    return navigator.mediaDevices.getUserMedia(RESTRICCIONES_DE_CAMARA)
}

/** Apaga todas las pistas del flujo (la luz de la camara se apaga). */
export function cerrarCamara(flujo) {
    flujo?.getTracks().forEach((pista) => pista.stop())
}
