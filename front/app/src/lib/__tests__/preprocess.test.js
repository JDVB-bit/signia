/** Tests propios del preprocesado en JS (los bordes, no solo la conformidad). */
import { describe, expect, it } from 'vitest'

import {
    LADOS,
    N_DIMS,
    N_LANDMARKS,
    T,
    apilarFrames,
    construirEntrada,
    indicesRemuestreo,
    manoDelFrame,
} from '../preprocess.js'

const IZQ = 0
const DER = 1

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

describe('indicesRemuestreo', () => {
    it.each([1, 2, 17, 47, 48, 49, 200])('siempre devuelve T indices (n=%i)', (n) => {
        expect(indicesRemuestreo(n, T)).toHaveLength(T)
    })

    it.each([2, 5, 48, 300])('conserva los extremos (n=%i)', (n) => {
        const idx = indicesRemuestreo(n, T)
        expect(idx[0]).toBe(0)
        expect(idx[idx.length - 1]).toBe(n - 1)
    })

    it('no decrece nunca', () => {
        const idx = indicesRemuestreo(77, T)
        expect(idx).toEqual([...idx].sort((a, b) => a - b))
    })

    it('con la longitud exacta es la identidad', () => {
        expect(indicesRemuestreo(T, T)).toEqual(Array.from({ length: T }, (_, i) => i))
    })

    it('con un solo frame lo repite', () => {
        expect(new Set(indicesRemuestreo(1, T))).toEqual(new Set([0]))
    })

    it('redondea hacia arriba, como int(x+0.5) en Python', () => {
        // El caso donde round() de Python (al par) daria [0, 0, 1, 2, 2].
        expect(indicesRemuestreo(3, 5)).toEqual([0, 1, 1, 2, 2])
    })

    it('rechaza una secuencia vacia', () => {
        expect(() => indicesRemuestreo(0, T)).toThrow(/secuencia/)
    })

    it('rechaza un destino invalido', () => {
        expect(() => indicesRemuestreo(10, 0)).toThrow(/destino/)
    })
})

describe('manoDelFrame', () => {
    it('devuelve null si no hay mano de ese lado', () => {
        expect(manoDelFrame(frame(['derecha']), 'izquierda')).toBeNull()
    })

    it('tolera un frame sin manos', () => {
        expect(manoDelFrame({}, 'derecha')).toBeNull()
    })

    it('con dos manos del mismo lado gana la de mayor score', () => {
        const floja = mano('derecha', { score: 0.4, dx: 0.1 })
        const buena = mano('derecha', { score: 0.95, dx: 0.9 })
        expect(manoDelFrame({ manos: [floja, buena] }, 'derecha')).toBe(buena)
        expect(manoDelFrame({ manos: [buena, floja] }, 'derecha')).toBe(buena)
    })
})

describe('apilarFrames', () => {
    const valoresPorMano = N_LANDMARKS * N_DIMS

    it('las ranuras son izquierda, derecha en ese orden', () => {
        expect(LADOS).toEqual(['izquierda', 'derecha'])
    })

    it('la mano ausente queda en ceros y con presencia 0', () => {
        const { lm, presencia } = apilarFrames([frame(['derecha'])])
        expect(Array.from(presencia)).toEqual([0, 1])
        expect(Array.from(lm.slice(0, valoresPorMano)).every((v) => v === 0)).toBe(true)
        expect(Array.from(lm.slice(valoresPorMano)).some((v) => v !== 0)).toBe(true)
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
        expect(a.lm[IZQ * valoresPorMano]).toBeCloseTo(0.1, 5)
        expect(a.lm[DER * valoresPorMano]).toBeCloseTo(0.9, 5)
    })
})

describe('construirEntrada', () => {
    it('produce siempre T pasos aunque la grabacion sea corta', () => {
        const muestra = { frames: [frame(), frame(), frame()] }
        expect(construirEntrada(muestra).presencia).toHaveLength(T * 2)
    })

    it('conserva el orden temporal', () => {
        const muestra = {
            frames: Array.from({ length: 10 }, (_, t) => frame(['derecha'], { dx: t / 10 })),
        }
        const { lm } = construirEntrada(muestra, 10)
        const xs = Array.from({ length: 10 }, (_, i) => lm[(i * 2 + DER) * N_LANDMARKS * N_DIMS])
        expect(xs).toEqual([...xs].sort((a, b) => a - b))
        expect(new Set(xs).size).toBe(10)
    })
})
