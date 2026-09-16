/** 🖐️ Adaptador de MediaPipe HandLandmarker: una unica instancia compartida por toda la app.
 *
 * Los assets se sirven desde `public/mediapipe/` (ver su README) para no
 * depender del CDN de Google en cada carga.
 */

import { FilesetResolver, HandLandmarker } from '@mediapipe/tasks-vision'

import { N_MANOS } from '../../dominio/contrato.js'

const RUTA_WASM = '/mediapipe/wasm'
const RUTA_MODELO = '/mediapipe/models/hand_landmarker.task'

/** Modo de ejecucion para frames consecutivos de un <video>. */
const MODO_VIDEO = 'VIDEO'

/** Delegados en orden de preferencia: la GPU es mucho mas rapida, la CPU siempre existe. */
const DELEGADOS = ['GPU', 'CPU']

let detectorPromesa = null

/** Intenta crear el detector con cada delegado hasta que uno funcione. */
async function crearDetector() {
    const ficheros = await FilesetResolver.forVisionTasks(RUTA_WASM)
    let ultimoError = null

    for (const delegado of DELEGADOS) {
        try {
            return await HandLandmarker.createFromOptions(ficheros, {
                baseOptions: { modelAssetPath: RUTA_MODELO, delegate: delegado },
                runningMode: MODO_VIDEO,
                numHands: N_MANOS,
            })
        } catch (error) {
            // 🔁 Sin WebGL (o con drivers rotos) la GPU falla: se prueba el siguiente delegado
            ultimoError = error
        }
    }
    throw ultimoError
}

/** Devuelve (creandola una sola vez) la promesa del detector de manos.
 *
 * Si la creacion falla se olvida la promesa, para que un reintento posterior
 * (por ejemplo, al volver a activar la camara) no herede el error para siempre.
 */
export function obtenerDetectorDeManos() {
    if (!detectorPromesa) {
        detectorPromesa = crearDetector().catch((error) => {
            detectorPromesa = null
            throw error
        })
    }
    return detectorPromesa
}
