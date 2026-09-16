/** 📜 Constantes del contrato de datos, gemelas de `model/signia_modelo/dominio/contrato.py`.
 *
 * Fuente de verdad en prosa: `model/contrato.md`. Si un valor cambia aqui tiene
 * que cambiar tambien en Python, y el test de conformidad lo vigila.
 */

// --- Versionado ---
export const SCHEMA = 1

// --- Geometria de MediaPipe HandLandmarker ---
export const N_LANDMARKS = 21
export const N_DIMS = 3
export const N_MANOS = 2
export const IDX_MUNECA = 0

// --- Ventana temporal del modelo (~1.6 s a 30 fps) ---
export const T = 48

// --- Vocabulario ---
export const LADO_IZQUIERDA = 'izquierda'
export const LADO_DERECHA = 'derecha'

/** Ranuras fijas del tensor, en este orden. Nunca el orden de deteccion. */
export const LADOS = [LADO_IZQUIERDA, LADO_DERECHA]

export const TIPO_AISLADA = 'aislada'

/** Confianza maxima de MediaPipe; se asume si el detector no la reporta. */
export const SCORE_MAXIMO = 1
