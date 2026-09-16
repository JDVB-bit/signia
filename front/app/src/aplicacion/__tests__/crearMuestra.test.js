/** Frames grabados -> muestra aislada del contrato. */
import { describe, expect, it } from 'vitest'

import { SCHEMA, TIPO_AISLADA } from '../../dominio/contrato.js'
import { crearMuestra } from '../crearMuestra.js'

const frames = [
    { t: 40, manos: [] },
    { t: 41, manos: [{ lado: 'derecha', score: 1, lm: [] }] },
]

describe('crearMuestra', () => {
    it('produce una muestra aislada del contrato', () => {
        const muestra = crearMuestra({ etiqueta: 'Hola', sesion: 's1', frames, fpsAprox: 29.97 })
        expect(muestra.schema).toBe(SCHEMA)
        expect(muestra.tipo).toBe(TIPO_AISLADA)
        expect(muestra.etiqueta).toBe('hola')
        expect(muestra.sesion).toBe('s1')
        expect(muestra.fps_aprox).toBe(30)
    })

    it('reindexa t desde 0: la muestra es una grabacion nueva, no un trozo', () => {
        const muestra = crearMuestra({ etiqueta: 'hola', sesion: 's1', frames })
        expect(muestra.frames.map((f) => f.t)).toEqual([0, 1])
    })

    it('conserva las manos tal cual', () => {
        const muestra = crearMuestra({ etiqueta: 'hola', sesion: 's1', frames })
        expect(muestra.frames[1].manos).toBe(frames[1].manos)
    })

    it.each([
        ['sin etiqueta', { etiqueta: '   ', sesion: 's1', frames }, /etiqueta/],
        ['sin sesion', { etiqueta: 'hola', sesion: '', frames }, /sesion/],
        ['sin frames', { etiqueta: 'hola', sesion: 's1', frames: [] }, /frame/],
    ])('rechaza una muestra %s', (_caso, argumentos, patron) => {
        expect(() => crearMuestra(argumentos)).toThrow(patron)
    })
})
