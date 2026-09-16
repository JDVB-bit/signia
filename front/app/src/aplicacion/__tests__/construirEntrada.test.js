/** Construccion del tensor crudo: ranuras, ausencias y orden temporal. */
import { describe, expect, it } from 'vitest'

import { LADOS, N_DIMS, N_LANDMARKS, N_MANOS, T } from '../../dominio/contrato.js'
import { apilarFrames, construirEntrada } from '../construirEntrada.js'

const RANURA_IZQUIERDA = 0
const RANURA_DERECHA = 1
const VALORES_POR_MANO = N_LANDMARKS * N_DIMS

const punto = (i) => [0.02 * (i % 5), 0.03 * Math.floor(i / 5), 0.001 * i]
const mano = (lado, { score = 0.9, dx = 0.5 } = {}) => ({
    lado,
    score,
    lm: Array.from({ length: N_LANDMARKS }, (_, i) => {
        const [x, y, z] = punto(i)
        return [x + dx, y, z]
    }),
})
const frame = (lados = ['derecha'], opciones) => ({
    manos: lados.map((lado) => mano(lado, opciones)),
})

describe('apilarFrames', () => {
    it('las ranuras son izquierda, derecha en ese orden', () => {
        expect(LADOS).toEqual(['izquierda', 'derecha'])
    })

    it('la mano ausente queda en ceros y con presencia 0', () => {
        const { lm, presencia } = apilarFrames([frame(['derecha'])])
        expect(Array.from(presencia)).toEqual([0, 1])
        expect(Array.from(lm.slice(0, VALORES_POR_MANO)).every((v) => v === 0)).toBe(true)
        expect(Array.from(lm.slice(VALORES_POR_MANO)).some((v) => v !== 0)).toBe(true)
    })

    it('el frame sin manos no rompe nada', () => {
        const { lm, presencia } = apilarFrames([{ manos: [] }])
        expect(Array.from(presencia)).toEqual([0, 0])
        expect(lm.every((v) => v === 0)).toBe(true)
    })

    it('la ranura no depende del orden de deteccion', () => {
        const a = apilarFrames([{ manos: [mano('izquierda', { dx: 0.1 }), mano('derecha', { dx: 0.9 })] }])
        const b = apilarFrames([{ manos: [mano('derecha', { dx: 0.9 }), mano('izquierda', { dx: 0.1 })] }])
        expect(Array.from(a.lm)).toEqual(Array.from(b.lm))
        expect(a.lm[RANURA_IZQUIERDA * VALORES_POR_MANO]).toBeCloseTo(0.1, 5)
        expect(a.lm[RANURA_DERECHA * VALORES_POR_MANO]).toBeCloseTo(0.9, 5)
    })
})

describe('construirEntrada', () => {
    it('produce siempre T pasos aunque la grabacion sea corta', () => {
        const muestra = { frames: [frame(), frame(), frame()] }
        expect(construirEntrada(muestra).presencia).toHaveLength(T * N_MANOS)
    })

    it('conserva el orden temporal', () => {
        const pasos = 10
        const muestra = {
            frames: Array.from({ length: pasos }, (_, t) => frame(['derecha'], { dx: t / pasos })),
        }
        const { lm } = construirEntrada(muestra, pasos)
        const xs = Array.from({ length: pasos }, (_, i) => lm[(i * N_MANOS + RANURA_DERECHA) * VALORES_POR_MANO])
        expect(xs).toEqual([...xs].sort((a, b) => a - b))
        expect(new Set(xs).size).toBe(pasos)
    })
})
