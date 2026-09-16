/** Traduccion del handedness de MediaPipe al lado del contrato. */
import { describe, expect, it } from 'vitest'

import { ladoDesdeCategoria } from '../ladoDesdeCategoria.js'

describe('ladoDesdeCategoria', () => {
    it('traduce lo que devuelve MediaPipe', () => {
        expect(ladoDesdeCategoria('Left')).toBe('izquierda')
        expect(ladoDesdeCategoria('Right')).toBe('derecha')
    })

    it('puede invertirse si el espejo del video engañara al detector', () => {
        expect(ladoDesdeCategoria('Left', true)).toBe('derecha')
        expect(ladoDesdeCategoria('Right', true)).toBe('izquierda')
    })

    it('devuelve null ante una categoria desconocida', () => {
        expect(ladoDesdeCategoria('Foot')).toBeNull()
        expect(ladoDesdeCategoria(undefined)).toBeNull()
    })
})
