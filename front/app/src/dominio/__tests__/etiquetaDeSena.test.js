/** Normalizacion de la etiqueta que escribe el usuario. */
import { describe, expect, it } from 'vitest'

import { normalizarEtiqueta } from '../etiquetaDeSena.js'

describe('normalizarEtiqueta', () => {
    it('limpia espacios y mayusculas', () => {
        expect(normalizarEtiqueta('  HOLA  ')).toBe('hola')
    })

    it('convierte la ausencia de texto en cadena vacia', () => {
        expect(normalizarEtiqueta(undefined)).toBe('')
    })
})
