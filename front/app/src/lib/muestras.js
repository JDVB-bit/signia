/** Del resultado de MediaPipe a una muestra del contrato (Fase 1).
 *
 * Toda la logica que se puede probar sin camara vive aqui, fuera del hook: el
 * hook solo orquesta el bucle de video. Contrato en `model/contrato.md`.
 */

import { N_DIMS, N_LANDMARKS, SCHEMA } from './preprocess.js'

/** Tope de duracion de una grabacion. La ventana del modelo son ~1.6 s (T=48 a
 * 30 fps); se graba mas holgado porque el remuestreo recorta, pero sin dejar
 * que una pulsacion olvidada genere una muestra de dos minutos. */
export const DURACION_MAXIMA_MS = 4000

/** Por debajo de esto no hay sena que valga: se descarta la muestra. */
export const FRAMES_MINIMOS = 5

/** Decimales que se guardan de cada coordenada. MediaPipe no tiene precision
 * real mas alla de esto y el JSON ocupa la mitad. Muy por encima del 1e-5 que
 * exige el test de conformidad. */
const DECIMALES = 6

/** MediaPipe etiqueta la mano en ingles y respecto a la imagen que recibe.
 *
 * OJO (riesgo del plan): el video se PINTA espejado, pero al detector se le
 * pasa el frame tal cual. Si al levantar la mano derecha la app dice
 * "izquierda", hay que poner esto a `true` y regenerar nada -- el dataset ya
 * grabado quedaria con los lados cambiados, por eso se verifica ANTES de
 * grabar en serio, con el rotulo que dibuja el overlay.
 */
export const INVERTIR_LADO = false

const LADO_POR_CATEGORIA = {
    Left: 'izquierda',
    Right: 'derecha',
}

const OPUESTO = {
    izquierda: 'derecha',
    derecha: 'izquierda',
}

/** "Left"/"Right" de MediaPipe -> el lado del contrato. */
export function ladoDesdeCategoria(categoria, invertir = INVERTIR_LADO) {
    const lado = LADO_POR_CATEGORIA[categoria]
    if (lado === undefined) return null
    return invertir ? OPUESTO[lado] : lado
}

const redondear = (valor) => Number(valor.toFixed(DECIMALES))

/** Resultado de `detectForVideo` -> un frame del contrato.
 *
 * Un frame puede quedarse con 0, 1 o 2 manos: la ausencia es informacion y no
 * se rellena. Se ignoran las manos cuyo handedness no se entienda, en vez de
 * inventarles un lado.
 */
export function frameDesdeResultado(resultado, t, { invertirLado = INVERTIR_LADO } = {}) {
    const landmarks = resultado?.landmarks ?? []
    const handedness = resultado?.handedness ?? resultado?.handednesses ?? []

    const manos = []
    landmarks.forEach((puntos, i) => {
        const categoria = handedness[i]?.[0]
        const lado = ladoDesdeCategoria(categoria?.categoryName, invertirLado)
        if (lado === null || puntos.length !== N_LANDMARKS) return

        manos.push({
            lado,
            score: redondear(categoria.score ?? 1),
            lm: puntos.map((p) => [redondear(p.x), redondear(p.y), redondear(p.z ?? 0)]),
        })
    })

    return { t, manos }
}

/** Identificador de la tanda de grabacion.
 *
 * `sesion` es lo que permite la evaluacion honesta de la Fase 4 (el split es
 * por sesion, nunca aleatorio). Fecha + un id estable del navegador agrupa
 * "mismo dia, mismo equipo", que es la aproximacion razonable a una tanda.
 */
export function idSesion(fecha = new Date(), dispositivo = 'local') {
    const dia = [
        fecha.getFullYear(),
        String(fecha.getMonth() + 1).padStart(2, '0'),
        String(fecha.getDate()).padStart(2, '0'),
    ].join('-')
    return `${dia}-${dispositivo}`
}

/** Etiqueta tal y como se guarda: sin espacios de mas y en minusculas. */
export function normalizarEtiqueta(texto) {
    return (texto ?? '').trim().toLowerCase()
}

/** Frames grabados -> muestra aislada del contrato. */
export function crearMuestra({ etiqueta, sesion, frames, fpsAprox = null }) {
    const limpia = normalizarEtiqueta(etiqueta)
    if (!limpia) throw new Error('la muestra necesita una etiqueta')
    if (!sesion) throw new Error('la muestra necesita una sesion')
    if (!frames?.length) throw new Error('la muestra necesita al menos un frame')

    return {
        schema: SCHEMA,
        tipo: 'aislada',
        etiqueta: limpia,
        sesion,
        fps_aprox: fpsAprox === null ? null : Number(fpsAprox.toFixed(1)),
        frames: frames.map((frame, i) => ({ t: i, manos: frame.manos })),
    }
}

/** Frames por segundo reales de la grabacion, para dejarlo anotado. */
export function fpsDe(nFrames, duracionMs) {
    if (duracionMs <= 0) return null
    return (nFrames * 1000) / duracionMs
}

/** Cuantos frames de la grabacion llevan al menos una mano.
 *
 * Sirve para avisar de una muestra mala antes de guardarla: si la mano no
 * aparecio, la muestra no ensena nada y ensucia el dataset.
 */
export function framesConMano(frames) {
    return frames.filter((frame) => frame.manos.length > 0).length
}

/** ¿Toca cerrar la grabacion por haber alcanzado el tope de duracion?
 *
 * Una pulsacion olvidada no puede generar una muestra de dos minutos: el
 * remuestreo la comprimiria a 48 frames y saldria una sena irreconocible.
 */
export function debeCerrarPorTiempo(transcurridoMs) {
    return transcurridoMs >= DURACION_MAXIMA_MS
}

/** Por que NO sirve esta grabacion, o null si sirve.
 *
 * La regla de "muestra mala" vive aqui y en ningun otro sitio: el hook solo
 * ensena el motivo. Descartar en el momento es mucho mas barato que descubrir
 * el dataset sucio despues de grabar cientos de muestras.
 */
export function motivoDeDescarte(frames) {
    if (frames.length < FRAMES_MINIMOS) {
        return 'Grabacion demasiado corta: no se guardo nada.'
    }
    if (framesConMano(frames) === 0) {
        return 'No se vio ninguna mano: la muestra se descarto.'
    }
    return null
}

/** El fichero que descarga el boton "Enviar" en esta fase.
 *
 * Es un lote de muestras crudas, exactamente el formato que consumira
 * `POST /muestras` en la Fase 5: aqui solo cambia el transporte.
 */
export function paqueteDeMuestras(muestras) {
    return { schema: SCHEMA, muestras }
}

/** Nombre del fichero descargado: legible y ordenable. */
export function nombreDeFichero(muestras, fecha = new Date()) {
    const etiquetas = [...new Set(muestras.map((m) => m.etiqueta))]
    const parte = etiquetas.length === 1 ? etiquetas[0] : `${etiquetas.length}-senas`
    return `signia-${parte}-${idSesion(fecha)}.json`
}

/** Dimensiones utiles para el overlay y para validar en tests. */
export const FORMA_DE_MANO = { landmarks: N_LANDMARKS, dims: N_DIMS }
