/** Cuando se cierra una grabacion y cuando se descarta, probado sin camara. */
import { describe, expect, it } from 'vitest'

import {
    DURACION_MAXIMA_MS,
    FRAMES_MINIMOS,
    MOTIVOS_DE_DESCARTE,
    debeCerrarPorTiempo,
    framesConMano,
    motivoDeDescarte,
} from '../reglasDeGrabacion.js'

const VENTANA_DEL_MODELO_MS = 1600
const conMano = { manos: [{ lado: 'derecha' }] }
const sinManos = { manos: [] }

describe('debeCerrarPorTiempo', () => {
    it('el tope de duracion cierra la grabacion sola', () => {
        expect(debeCerrarPorTiempo(DURACION_MAXIMA_MS)).toBe(true)
        expect(debeCerrarPorTiempo(DURACION_MAXIMA_MS + 1)).toBe(true)
    })

    it('antes del tope no se cierra nada', () => {
        expect(debeCerrarPorTiempo(0)).toBe(false)
        expect(debeCerrarPorTiempo(DURACION_MAXIMA_MS - 1)).toBe(false)
    })

    it('el tope deja margen de sobra sobre la ventana del modelo', () => {
        expect(DURACION_MAXIMA_MS).toBeGreaterThan(VENTANA_DEL_MODELO_MS)
    })
})

describe('motivoDeDescarte', () => {
    it('una grabacion demasiado corta se descarta', () => {
        const frames = Array.from({ length: FRAMES_MINIMOS - 1 }, () => conMano)
        expect(motivoDeDescarte(frames)).toBe(MOTIVOS_DE_DESCARTE.DEMASIADO_CORTA)
    })

    it('una grabacion sin ninguna mano se descarta', () => {
        const frames = Array.from({ length: FRAMES_MINIMOS + 5 }, () => sinManos)
        expect(motivoDeDescarte(frames)).toBe(MOTIVOS_DE_DESCARTE.SIN_MANOS)
    })

    it('basta con que la mano aparezca en algun frame', () => {
        const frames = [...Array.from({ length: FRAMES_MINIMOS }, () => sinManos), conMano]
        expect(motivoDeDescarte(frames)).toBeNull()
    })
})

describe('framesConMano', () => {
    it('cuenta los frames utiles', () => {
        expect(framesConMano([{ manos: [] }, { manos: [{}] }, { manos: [{}, {}] }])).toBe(2)
    })
})
