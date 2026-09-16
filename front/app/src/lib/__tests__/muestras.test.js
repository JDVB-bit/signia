/** Todo lo que el bucle de captura decide, probado sin camara. */
import { describe, expect, it } from 'vitest'

import { N_LANDMARKS } from '../preprocess.js'
import {
    DURACION_MAXIMA_MS,
    FRAMES_MINIMOS,
    crearMuestra,
    debeCerrarPorTiempo,
    fpsDe,
    framesConMano,
    frameDesdeResultado,
    idSesion,
    ladoDesdeCategoria,
    motivoDeDescarte,
    nombreDeFichero,
    normalizarEtiqueta,
    paqueteDeMuestras,
} from '../muestras.js'

const puntos = (n = N_LANDMARKS) =>
    Array.from({ length: n }, (_, i) => ({ x: i / 100, y: i / 200, z: i / 1000 }))

const resultado = (manos) => ({
    landmarks: manos.map((m) => m.puntos ?? puntos()),
    handedness: manos.map((m) => [{ categoryName: m.categoria, score: m.score ?? 0.9 }]),
})

describe('ladoDesdeCategoria', () => {
    it('traduce lo que devuelve MediaPipe', () => {
        expect(ladoDesdeCategoria('Left')).toBe('izquierda')
        expect(ladoDesdeCategoria('Right')).toBe('derecha')
    })

    it('puede invertirse si el espejo del video enganara al detector', () => {
        expect(ladoDesdeCategoria('Left', true)).toBe('derecha')
        expect(ladoDesdeCategoria('Right', true)).toBe('izquierda')
    })

    it('devuelve null ante una categoria desconocida', () => {
        expect(ladoDesdeCategoria('Foot')).toBeNull()
        expect(ladoDesdeCategoria(undefined)).toBeNull()
    })
})

describe('frameDesdeResultado', () => {
    it('sin manos produce un frame vacio, no un hueco', () => {
        expect(frameDesdeResultado({ landmarks: [], handedness: [] }, 7)).toEqual({
            t: 7,
            manos: [],
        })
    })

    it('tolera un resultado nulo', () => {
        expect(frameDesdeResultado(null, 0).manos).toEqual([])
    })

    it('convierte una mano al formato del contrato', () => {
        const frame = frameDesdeResultado(resultado([{ categoria: 'Right', score: 0.97 }]), 3)
        expect(frame.t).toBe(3)
        expect(frame.manos).toHaveLength(1)
        expect(frame.manos[0].lado).toBe('derecha')
        expect(frame.manos[0].score).toBeCloseTo(0.97, 6)
        expect(frame.manos[0].lm).toHaveLength(N_LANDMARKS)
        expect(frame.manos[0].lm[0]).toHaveLength(3)
    })

    it('conserva las dos manos', () => {
        const frame = frameDesdeResultado(
            resultado([{ categoria: 'Left' }, { categoria: 'Right' }]),
            0,
        )
        expect(frame.manos.map((m) => m.lado)).toEqual(['izquierda', 'derecha'])
    })

    it('acepta el campo handednesses en plural', () => {
        const frame = frameDesdeResultado(
            { landmarks: [puntos()], handednesses: [[{ categoryName: 'Left', score: 0.8 }]] },
            0,
        )
        expect(frame.manos[0].lado).toBe('izquierda')
    })

    it('descarta una mano con un numero de landmarks que no es el del contrato', () => {
        const crudo = resultado([{ categoria: 'Right', puntos: puntos(5) }])
        expect(frameDesdeResultado(crudo, 0).manos).toEqual([])
    })

    it('descarta una mano sin handedness en vez de inventarle un lado', () => {
        expect(frameDesdeResultado({ landmarks: [puntos()], handedness: [] }, 0).manos).toEqual([])
    })

    it('redondea las coordenadas a 6 decimales', () => {
        const crudo = {
            landmarks: [Array.from({ length: N_LANDMARKS }, () => ({ x: 0.1234567891, y: 0.5, z: 0 }))],
            handedness: [[{ categoryName: 'Right', score: 1 }]],
        }
        expect(frameDesdeResultado(crudo, 0).manos[0].lm[0][0]).toBe(0.123457)
    })

    it('pone z a 0 si MediaPipe no la da', () => {
        const crudo = {
            landmarks: [Array.from({ length: N_LANDMARKS }, () => ({ x: 0.1, y: 0.2 }))],
            handedness: [[{ categoryName: 'Right', score: 1 }]],
        }
        expect(frameDesdeResultado(crudo, 0).manos[0].lm[0][2]).toBe(0)
    })
})

describe('crearMuestra', () => {
    const frames = [
        { t: 40, manos: [] },
        { t: 41, manos: [{ lado: 'derecha', score: 1, lm: [] }] },
    ]

    it('produce una muestra aislada del contrato', () => {
        const muestra = crearMuestra({ etiqueta: 'Hola', sesion: 's1', frames, fpsAprox: 29.97 })
        expect(muestra.schema).toBe(1)
        expect(muestra.tipo).toBe('aislada')
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

describe('cuando se cierra y cuando se descarta', () => {
    const conMano = { manos: [{ lado: 'derecha' }] }
    const sinManos = { manos: [] }

    it('el tope de duracion cierra la grabacion sola', () => {
        expect(debeCerrarPorTiempo(DURACION_MAXIMA_MS)).toBe(true)
        expect(debeCerrarPorTiempo(DURACION_MAXIMA_MS + 1)).toBe(true)
    })

    it('antes del tope no se cierra nada', () => {
        expect(debeCerrarPorTiempo(0)).toBe(false)
        expect(debeCerrarPorTiempo(DURACION_MAXIMA_MS - 1)).toBe(false)
    })

    it('el tope deja margen de sobra sobre la ventana del modelo (~1.6 s)', () => {
        expect(DURACION_MAXIMA_MS).toBeGreaterThan(2000)
    })

    it('una grabacion demasiado corta se descarta', () => {
        const frames = Array.from({ length: FRAMES_MINIMOS - 1 }, () => conMano)
        expect(motivoDeDescarte(frames)).toMatch(/corta/)
    })

    it('una grabacion sin ninguna mano se descarta', () => {
        const frames = Array.from({ length: FRAMES_MINIMOS + 5 }, () => sinManos)
        expect(motivoDeDescarte(frames)).toMatch(/mano/)
    })

    it('basta con que la mano aparezca en algun frame', () => {
        const frames = [...Array.from({ length: FRAMES_MINIMOS }, () => sinManos), conMano]
        expect(motivoDeDescarte(frames)).toBeNull()
    })
})

describe('utilidades', () => {
    it('normalizarEtiqueta limpia espacios y mayusculas', () => {
        expect(normalizarEtiqueta('  HOLA  ')).toBe('hola')
        expect(normalizarEtiqueta(undefined)).toBe('')
    })

    it('idSesion tiene el formato del plan', () => {
        expect(idSesion(new Date(2026, 8, 20), 'snt')).toBe('2026-09-20-snt')
    })

    it('fpsDe calcula los frames por segundo reales', () => {
        expect(fpsDe(48, 1600)).toBeCloseTo(30, 6)
        expect(fpsDe(10, 0)).toBeNull()
    })

    it('framesConMano cuenta los frames utiles', () => {
        expect(framesConMano([{ manos: [] }, { manos: [{}] }, { manos: [{}, {}] }])).toBe(2)
    })

    it('paqueteDeMuestras envuelve el lote con su schema', () => {
        expect(paqueteDeMuestras([{ etiqueta: 'hola' }])).toEqual({
            schema: 1,
            muestras: [{ etiqueta: 'hola' }],
        })
    })

    it('nombreDeFichero usa la etiqueta cuando el lote es de una sola sena', () => {
        const nombre = nombreDeFichero([{ etiqueta: 'hola' }, { etiqueta: 'hola' }], new Date(2026, 8, 20))
        expect(nombre).toBe('signia-hola-2026-09-20-local.json')
    })

    it('nombreDeFichero cuenta las senas cuando el lote es mixto', () => {
        const nombre = nombreDeFichero([{ etiqueta: 'hola' }, { etiqueta: 'tu' }], new Date(2026, 8, 20))
        expect(nombre).toBe('signia-2-senas-2026-09-20-local.json')
    })
})
