/** 💬 La unica linea de estado de Entrenamiento: lo que hace falta saber antes de pulsar. */

import { ESTADOS_DETECTOR } from '../estados/estadosDelDetector.js'

/** Prioridad: aviso puntual > camara apagada > detector cargando o con error > sesion actual. */
export function mensajeDeEstadoDeCaptura({ aviso, camaraActiva, estadoDetector, sesion }) {
    if (aviso) return aviso
    if (!camaraActiva) return 'Activa la cámara para empezar a grabar.'
    if (estadoDetector === ESTADOS_DETECTOR.CARGANDO) return 'Cargando el detector de manos...'
    if (estadoDetector === ESTADOS_DETECTOR.ERROR) return 'No se pudo cargar el detector de manos.'
    return `Sesión ${sesion}`
}
