/** El overlay del esqueleto, probado con un canvas de mentira. */
import { describe, expect, it, vi } from 'vitest'

import { N_LANDMARKS } from '../../../dominio/contrato.js'
import { CONEXIONES, COLOR_POR_LADO, dibujarManos, puntoEnCanvas } from '../dibujarManos.js'

const lm = (n = N_LANDMARKS) => Array.from({ length: n }, (_, i) => [i / 100, i / 200, 0])
const mano = (lado = 'derecha') => ({ lado, score: 0.9, lm: lm() })

function ctxFalso() {
    return {
        textos: [],
        clearRect: vi.fn(),
        beginPath: vi.fn(),
        moveTo: vi.fn(),
        lineTo: vi.fn(),
        stroke: vi.fn(),
        arc: vi.fn(),
        fill: vi.fn(),
        fillText: vi.fn(function (texto) {
            this.textos.push(texto)
        }),
    }
}

const OPCIONES = { ancho: 640, alto: 480, espejado: true }

describe('CONEXIONES', () => {
    it('todas apuntan a landmarks que existen', () => {
        for (const [a, b] of CONEXIONES) {
            expect(a).toBeGreaterThanOrEqual(0)
            expect(b).toBeLessThan(N_LANDMARKS)
        }
    })

    it('no hay ninguna repetida ni ningun punto consigo mismo', () => {
        const claves = CONEXIONES.map(([a, b]) => `${Math.min(a, b)}-${Math.max(a, b)}`)
        expect(new Set(claves).size).toBe(CONEXIONES.length)
        expect(CONEXIONES.every(([a, b]) => a !== b)).toBe(true)
    })

    it('todos los landmarks quedan conectados al esqueleto', () => {
        const usados = new Set(CONEXIONES.flat())
        expect(usados.size).toBe(N_LANDMARKS)
    })
})

describe('puntoEnCanvas', () => {
    it('escala el landmark normalizado al tamano del canvas', () => {
        expect(puntoEnCanvas({ x: 0.25, y: 0.5 }, { ...OPCIONES, espejado: false })).toEqual({
            x: 160,
            y: 240,
        })
    })

    it('espeja la x para que coincida con el video, que se pinta espejado', () => {
        expect(puntoEnCanvas({ x: 0.25, y: 0.5 }, OPCIONES)).toEqual({ x: 480, y: 240 })
    })
})

describe('dibujarManos', () => {
    it('limpia el canvas en cada repintado', () => {
        const ctx = ctxFalso()
        dibujarManos(ctx, [], OPCIONES)
        expect(ctx.clearRect).toHaveBeenCalledWith(0, 0, 640, 480)
    })

    it('dibuja un hueso por conexion y un punto por landmark', () => {
        const ctx = ctxFalso()
        dibujarManos(ctx, [mano()], OPCIONES)
        expect(ctx.moveTo).toHaveBeenCalledTimes(CONEXIONES.length)
        expect(ctx.lineTo).toHaveBeenCalledTimes(CONEXIONES.length)
        expect(ctx.arc).toHaveBeenCalledTimes(N_LANDMARKS)
    })

    it('rotula el lado: es la verificacion del handedness', () => {
        const ctx = ctxFalso()
        dibujarManos(ctx, [mano('izquierda'), mano('derecha')], OPCIONES)
        expect(ctx.textos).toEqual(['izquierda', 'derecha'])
    })

    it('usa un color distinto por mano', () => {
        expect(COLOR_POR_LADO.izquierda).not.toBe(COLOR_POR_LADO.derecha)
    })

    it('ignora una mano con landmarks incompletos en vez de reventar el bucle', () => {
        const ctx = ctxFalso()
        dibujarManos(ctx, [{ lado: 'derecha', lm: lm(4) }], OPCIONES)
        expect(ctx.arc).not.toHaveBeenCalled()
        expect(ctx.clearRect).toHaveBeenCalled()
    })
})
