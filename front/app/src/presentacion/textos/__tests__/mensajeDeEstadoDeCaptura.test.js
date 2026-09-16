/** Prioridad de los mensajes de la linea de estado de Entrenamiento. */
import { describe, expect, it } from 'vitest'

import { ESTADOS_DETECTOR } from '../../estados/estadosDelDetector.js'
import { mensajeDeEstadoDeCaptura } from '../mensajeDeEstadoDeCaptura.js'

const listo = { aviso: null, camaraActiva: true, estadoDetector: ESTADOS_DETECTOR.LISTO, sesion: 's1' }

describe('mensajeDeEstadoDeCaptura', () => {
    it('un aviso puntual gana a todo lo demas', () => {
        expect(mensajeDeEstadoDeCaptura({ ...listo, camaraActiva: false, aviso: 'ojo' })).toBe('ojo')
    })

    it('sin camara pide activarla', () => {
        expect(mensajeDeEstadoDeCaptura({ ...listo, camaraActiva: false })).toMatch(/cámara/)
    })

    it('informa mientras carga el detector', () => {
        expect(mensajeDeEstadoDeCaptura({ ...listo, estadoDetector: ESTADOS_DETECTOR.CARGANDO })).toMatch(/Cargando/)
    })

    it('informa si el detector fallo', () => {
        expect(mensajeDeEstadoDeCaptura({ ...listo, estadoDetector: ESTADOS_DETECTOR.ERROR })).toMatch(/No se pudo/)
    })

    it('con todo listo muestra la sesion', () => {
        expect(mensajeDeEstadoDeCaptura(listo)).toBe('Sesión s1')
    })
})
