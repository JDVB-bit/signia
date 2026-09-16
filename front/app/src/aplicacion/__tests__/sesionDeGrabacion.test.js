/** Formato del identificador de sesion. */
import { describe, expect, it } from 'vitest'

import { DISPOSITIVO_POR_DEFECTO, idSesion } from '../sesionDeGrabacion.js'

const SEPTIEMBRE = 8

describe('idSesion', () => {
    it('tiene el formato del plan', () => {
        expect(idSesion(new Date(2026, SEPTIEMBRE, 20), 'snt')).toBe('2026-09-20-snt')
    })

    it('usa el dispositivo por defecto si no se indica', () => {
        expect(idSesion(new Date(2026, SEPTIEMBRE, 20))).toBe(`2026-09-20-${DISPOSITIVO_POR_DEFECTO}`)
    })
})
