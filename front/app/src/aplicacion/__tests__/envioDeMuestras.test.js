/** Subir el lote, y si el backend no esta, no perderlo. */
import { describe, expect, it, vi } from 'vitest'

import { RESULTADOS_DE_ENVIO, enviarMuestras } from '../envioDeMuestras.js'

const PAQUETE = { schema: 1, muestras: [{ etiqueta: 'hola' }, { etiqueta: 'tu' }] }

/** Backend que responde como el de verdad. */
const subidaOk = (respuesta = { guardadas: 2, por_etiqueta: { hola: 1, tu: 1 } }) =>
    vi.fn().mockResolvedValue(respuesta)

/** Backend apagado. */
const subidaRota = (motivo = 'Failed to fetch') => vi.fn().mockRejectedValue(new Error(motivo))

describe('cuando el backend responde', () => {
    it('informa de que se subio', async () => {
        const desenlace = await enviarMuestras({ paquete: PAQUETE, subir: subidaOk(), descargar: vi.fn() })
        expect(desenlace.resultado).toBe(RESULTADOS_DE_ENVIO.SUBIDO)
    })

    it('no descarga nada', async () => {
        const descargar = vi.fn()
        await enviarMuestras({ paquete: PAQUETE, subir: subidaOk(), descargar })
        expect(descargar).not.toHaveBeenCalled()
    })

    it('cuenta lo que dice el servidor, no lo que se envio', async () => {
        const subir = subidaOk({ guardadas: 1, por_etiqueta: { hola: 1 } })
        const desenlace = await enviarMuestras({ paquete: PAQUETE, subir, descargar: vi.fn() })
        expect(desenlace.cuantas).toBe(1)
    })

    it('sin conteo en la respuesta, asume las enviadas', async () => {
        const desenlace = await enviarMuestras({ paquete: PAQUETE, subir: subidaOk({}), descargar: vi.fn() })
        expect(desenlace.cuantas).toBe(2)
    })

    it('envia el paquete tal cual', async () => {
        const subir = subidaOk()
        await enviarMuestras({ paquete: PAQUETE, subir, descargar: vi.fn() })
        expect(subir).toHaveBeenCalledWith(PAQUETE)
    })
})

describe('cuando el backend no responde', () => {
    it('descarga el lote como respaldo', async () => {
        const descargar = vi.fn()
        await enviarMuestras({ paquete: PAQUETE, subir: subidaRota(), descargar })
        expect(descargar).toHaveBeenCalledWith(PAQUETE)
    })

    it('lo cuenta como respaldo y no como error', async () => {
        const desenlace = await enviarMuestras({ paquete: PAQUETE, subir: subidaRota(), descargar: vi.fn() })
        expect(desenlace.resultado).toBe(RESULTADOS_DE_ENVIO.RESPALDADO)
    })

    it('conserva el motivo para poder enseñarlo', async () => {
        const desenlace = await enviarMuestras({
            paquete: PAQUETE,
            subir: subidaRota('muestra 1 del lote: falta la lista'),
            descargar: vi.fn(),
        })
        expect(desenlace.motivo).toContain('muestra 1 del lote')
    })

    it('nunca lanza: media hora de grabacion no se pierde por una excepcion', async () => {
        await expect(
            enviarMuestras({ paquete: PAQUETE, subir: subidaRota(), descargar: vi.fn() }),
        ).resolves.toBeDefined()
    })
})

describe('cuando no hay nada que enviar', () => {
    it('no llama al servidor', async () => {
        const subir = subidaOk()
        await enviarMuestras({ paquete: { schema: 1, muestras: [] }, subir, descargar: vi.fn() })
        expect(subir).not.toHaveBeenCalled()
    })

    it('no descarga un fichero vacio', async () => {
        const descargar = vi.fn()
        await enviarMuestras({ paquete: { schema: 1, muestras: [] }, subir: subidaOk(), descargar })
        expect(descargar).not.toHaveBeenCalled()
    })

    it('lo dice', async () => {
        const desenlace = await enviarMuestras({
            paquete: { schema: 1, muestras: [] },
            subir: subidaOk(),
            descargar: vi.fn(),
        })
        expect(desenlace.resultado).toBe(RESULTADOS_DE_ENVIO.SIN_MUESTRAS)
    })
})
