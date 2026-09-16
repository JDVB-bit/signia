/** Regla unica para elegir la mano de un lado cuando MediaPipe reporta duplicadas. */
import { describe, expect, it } from 'vitest'

import { LADO_DERECHA, LADO_IZQUIERDA } from '../contrato.js'
import { manoDelFrame } from '../manoDelFrame.js'

const mano = (lado, score) => ({ lado, score, lm: [] })

describe('manoDelFrame', () => {
    it('devuelve null si no hay mano de ese lado', () => {
        expect(manoDelFrame({ manos: [mano(LADO_DERECHA, 0.9)] }, LADO_IZQUIERDA)).toBeNull()
    })

    it('tolera un frame sin manos', () => {
        expect(manoDelFrame({}, LADO_DERECHA)).toBeNull()
    })

    it('con dos manos del mismo lado gana la de mayor score', () => {
        const floja = mano(LADO_DERECHA, 0.4)
        const buena = mano(LADO_DERECHA, 0.95)
        expect(manoDelFrame({ manos: [floja, buena] }, LADO_DERECHA)).toBe(buena)
        expect(manoDelFrame({ manos: [buena, floja] }, LADO_DERECHA)).toBe(buena)
    })

    it('ante un empate gana la primera', () => {
        const primera = mano(LADO_DERECHA, 0.8)
        const segunda = mano(LADO_DERECHA, 0.8)
        expect(manoDelFrame({ manos: [primera, segunda] }, LADO_DERECHA)).toBe(primera)
    })
})
