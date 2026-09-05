import { FilesetResolver, HandLandmarker } from '@mediapipe/tasks-vision'

// Assets self-hosted en public/mediapipe/ (ver public/mediapipe/README.md).
// No se usa el CDN de Google para no depender de un tercero en cada carga.
const WASM_PATH = '/mediapipe/wasm'
const MODEL_PATH = '/mediapipe/models/hand_landmarker.task'

let handLandmarkerPromise = null

/**
 * Crea (una sola vez, reutilizable) la instancia de HandLandmarker.
 * Usar dentro de un componente/hook para extraer los puntos de la mano
 * desde webcam o imágenes, y mandarlos al backend.
 */
export function getHandLandmarker() {
  if (!handLandmarkerPromise) {
    handLandmarkerPromise = FilesetResolver.forVisionTasks(WASM_PATH).then((filesetResolver) =>
      HandLandmarker.createFromOptions(filesetResolver, {
        baseOptions: {
          modelAssetPath: MODEL_PATH,
          delegate: 'GPU',
        },
        runningMode: 'VIDEO',
        numHands: 2,
      }),
    )
  }
  return handLandmarkerPromise
}
