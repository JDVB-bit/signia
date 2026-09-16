/** fps reales de una grabacion. */
import { describe, expect, it } from 'vitest'

import { fpsDe } from '../fpsDeGrabacion.js'

describe('fpsDe', () => {
    it('calcula los frames por segundo reales', () => {
        expect(fpsDe(48, 1600)).toBeCloseTo(30, 6)
    })

    it('devuelve null con una duracion no valida', () => {
        expect(fpsDe(10, 0)).toBeNull()
    })
})
