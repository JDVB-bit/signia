/** Lote exportado y nombre de su fichero. */
import { describe, expect, it } from 'vitest'

import { SCHEMA } from '../../dominio/contrato.js'
import { nombreDeFichero, paqueteDeMuestras } from '../paqueteDeMuestras.js'

const SEPTIEMBRE = 8
const FECHA = new Date(2026, SEPTIEMBRE, 20)

describe('paqueteDeMuestras', () => {
    it('envuelve el lote con su schema', () => {
        expect(paqueteDeMuestras([{ etiqueta: 'hola' }])).toEqual({
            schema: SCHEMA,
            muestras: [{ etiqueta: 'hola' }],
        })
    })
})

describe('nombreDeFichero', () => {
    it('usa la etiqueta cuando el lote es de una sola seña', () => {
        const nombre = nombreDeFichero([{ etiqueta: 'hola' }, { etiqueta: 'hola' }], FECHA)
        expect(nombre).toBe('signia-hola-2026-09-20-local.json')
    })

    it('cuenta las señas cuando el lote es mixto', () => {
        const nombre = nombreDeFichero([{ etiqueta: 'hola' }, { etiqueta: 'tu' }], FECHA)
        expect(nombre).toBe('signia-2-senas-2026-09-20-local.json')
    })
})
