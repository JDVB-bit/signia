/** Resultado de MediaPipe -> frame del contrato, sin camara. */
import { describe, expect, it } from 'vitest'

import { N_DIMS, N_LANDMARKS } from '../../../dominio/contrato.js'
import { DECIMALES_COORDENADA, frameDesdeResultado } from '../frameDesdeDeteccion.js'

const SCORE_TIPICO = 0.9

const puntos = (n = N_LANDMARKS) =>
    Array.from({ length: n }, (_, i) => ({ x: i / 100, y: i / 200, z: i / 1000 }))

const resultado = (manos) => ({
    landmarks: manos.map((m) => m.puntos ?? puntos()),
    handedness: manos.map((m) => [{ categoryName: m.categoria, score: m.score ?? SCORE_TIPICO }]),
})

describe('frameDesdeResultado', () => {
    it('sin manos produce un frame vacio, no un hueco', () => {
        expect(frameDesdeResultado({ landmarks: [], handedness: [] }, 7)).toEqual({ t: 7, manos: [] })
    })

    it('tolera un resultado nulo', () => {
        expect(frameDesdeResultado(null, 0).manos).toEqual([])
    })

    it('convierte una mano al formato del contrato', () => {
        const frame = frameDesdeResultado(resultado([{ categoria: 'Right', score: 0.97 }]), 3)
        expect(frame.t).toBe(3)
        expect(frame.manos).toHaveLength(1)
        expect(frame.manos[0].lado).toBe('derecha')
        expect(frame.manos[0].score).toBeCloseTo(0.97, DECIMALES_COORDENADA)
        expect(frame.manos[0].lm).toHaveLength(N_LANDMARKS)
        expect(frame.manos[0].lm[0]).toHaveLength(N_DIMS)
    })

    it('conserva las dos manos', () => {
        const frame = frameDesdeResultado(resultado([{ categoria: 'Left' }, { categoria: 'Right' }]), 0)
        expect(frame.manos.map((m) => m.lado)).toEqual(['izquierda', 'derecha'])
    })

    it('acepta el campo handednesses en plural', () => {
        const frame = frameDesdeResultado(
            { landmarks: [puntos()], handednesses: [[{ categoryName: 'Left', score: 0.8 }]] },
            0,
        )
        expect(frame.manos[0].lado).toBe('izquierda')
    })

    it('descarta una mano con un numero de landmarks que no es el del contrato', () => {
        const crudo = resultado([{ categoria: 'Right', puntos: puntos(5) }])
        expect(frameDesdeResultado(crudo, 0).manos).toEqual([])
    })

    it('descarta una mano sin handedness en vez de inventarle un lado', () => {
        expect(frameDesdeResultado({ landmarks: [puntos()], handedness: [] }, 0).manos).toEqual([])
    })

    it('redondea las coordenadas a los decimales del contrato', () => {
        const crudo = {
            landmarks: [Array.from({ length: N_LANDMARKS }, () => ({ x: 0.1234567891, y: 0.5, z: 0 }))],
            handedness: [[{ categoryName: 'Right', score: 1 }]],
        }
        expect(frameDesdeResultado(crudo, 0).manos[0].lm[0][0]).toBe(0.123457)
    })

    it('pone z a 0 si MediaPipe no la da', () => {
        const crudo = {
            landmarks: [Array.from({ length: N_LANDMARKS }, () => ({ x: 0.1, y: 0.2 }))],
            handedness: [[{ categoryName: 'Right', score: 1 }]],
        }
        expect(frameDesdeResultado(crudo, 0).manos[0].lm[0][2]).toBe(0)
    })
})
