/** Test de conformidad JS <-> Python (Fase 0 del plan).
 *
 * Lee los MISMOS fixtures que verifica pytest en `model/tests/test_conformidad.py`
 * y comprueba que el remuestreo y el tensor crudo de este lado coinciden a 1e-5.
 *
 * Es la red que impide la deriva silenciosa entre el preprocesado del
 * entrenamiento y el del navegador. Si falla, NO se regeneran los fixtures sin
 * pensar: significa que los dos lados han dejado de calcular lo mismo.
 */
import { readFileSync, readdirSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'

import {
    N_DIMS,
    N_LANDMARKS,
    N_MANOS,
    T,
    construirEntrada,
    indicesRemuestreo,
} from '../preprocess.js'

const CARPETA = fileURLToPath(new URL('../../../../../model/tests/fixtures/', import.meta.url))
const TOLERANCIA = 1e-5

const fixtures = readdirSync(CARPETA)
    .filter((nombre) => nombre.endsWith('.json'))
    .map((nombre) => JSON.parse(readFileSync(CARPETA + nombre, 'utf8')))

describe('fixtures de conformidad', () => {
    it('estan generados', () => {
        expect(fixtures.length).toBeGreaterThan(0)
    })

    it('usan la misma T que este codigo', () => {
        for (const fixture of fixtures) expect(fixture.T).toBe(T)
    })
})

describe.each(fixtures.map((f) => [f.nombre, f]))('caso %s', (_nombre, fixture) => {
    const { muestra, esperado } = fixture

    it('el remuestreo elige los mismos indices que Python', () => {
        expect(indicesRemuestreo(muestra.frames.length, fixture.T)).toEqual(esperado.indices)
    })

    it('la presencia coincide exactamente', () => {
        const { presencia } = construirEntrada(muestra, fixture.T)
        expect(Array.from(presencia)).toEqual(esperado.presencia)
    })

    it('los landmarks coinciden a 1e-5', () => {
        const { lm } = construirEntrada(muestra, fixture.T)
        expect(lm.length).toBe(esperado.lm.length)

        let maxDiff = 0
        for (let i = 0; i < lm.length; i += 1) {
            maxDiff = Math.max(maxDiff, Math.abs(lm[i] - esperado.lm[i]))
        }
        expect(maxDiff).toBeLessThan(TOLERANCIA)
    })

    it('el tensor tiene la forma del contrato', () => {
        const { dims } = construirEntrada(muestra, fixture.T)
        expect(dims.lm).toEqual([T, N_MANOS, N_LANDMARKS, N_DIMS])
        expect(dims.presencia).toEqual([T, N_MANOS])
    })
})
