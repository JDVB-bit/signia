/** Bordes del remuestreo en JS (la igualdad con Python la vigila conformidad.test.js). */
import { describe, expect, it } from 'vitest'

import { T } from '../../dominio/contrato.js'
import { indicesRemuestreo } from '../remuestreo.js'

describe('indicesRemuestreo', () => {
    it.each([1, 2, 17, 47, 48, 49, 200])('siempre devuelve T indices (n=%i)', (n) => {
        expect(indicesRemuestreo(n, T)).toHaveLength(T)
    })

    it.each([2, 5, 48, 300])('conserva los extremos (n=%i)', (n) => {
        const indices = indicesRemuestreo(n, T)
        expect(indices[0]).toBe(0)
        expect(indices[indices.length - 1]).toBe(n - 1)
    })

    it('no decrece nunca', () => {
        const indices = indicesRemuestreo(77, T)
        expect(indices).toEqual([...indices].sort((a, b) => a - b))
    })

    it('con la longitud exacta es la identidad', () => {
        expect(indicesRemuestreo(T, T)).toEqual(Array.from({ length: T }, (_, i) => i))
    })

    it('con un solo frame lo repite', () => {
        expect(new Set(indicesRemuestreo(1, T))).toEqual(new Set([0]))
    })

    it('redondea hacia arriba, como int(x+0.5) en Python', () => {
        // El round() de Python (al par) daria [0, 0, 1, 2, 2]
        expect(indicesRemuestreo(3, 5)).toEqual([0, 1, 1, 2, 2])
    })

    it('rechaza una secuencia vacia', () => {
        expect(() => indicesRemuestreo(0, T)).toThrow(/secuencia/)
    })

    it('rechaza un destino invalido', () => {
        expect(() => indicesRemuestreo(10, 0)).toThrow(/destino/)
    })
})
