/** El transporte del lote: que se manda, que se devuelve y como falla. */
import { describe, expect, it, vi } from 'vitest'

import { subirLote } from '../clienteDeMuestras.js'

const PAQUETE = { schema: 1, muestras: [{ etiqueta: 'hola' }] }

/** Respuesta de fetch, con lo justo que usa el cliente. */
const respuesta = ({ ok = true, cuerpo = {}, rompeAlLeer = false } = {}) => ({
    ok,
    json: rompeAlLeer ? () => Promise.reject(new Error('no es JSON')) : () => Promise.resolve(cuerpo),
})

describe('subirLote', () => {
    it('hace un POST con el paquete en el cuerpo', async () => {
        const peticion = vi.fn().mockResolvedValue(respuesta({ cuerpo: { guardadas: 1 } }))
        await subirLote(PAQUETE, { peticion, entorno: {} })

        const [url, opciones] = peticion.mock.calls[0]
        expect(url).toContain('/muestras')
        expect(opciones.method).toBe('POST')
        expect(JSON.parse(opciones.body)).toEqual(PAQUETE)
    })

    it('declara que manda JSON', async () => {
        const peticion = vi.fn().mockResolvedValue(respuesta())
        await subirLote(PAQUETE, { peticion, entorno: {} })
        expect(peticion.mock.calls[0][1].headers['Content-Type']).toBe('application/json')
    })

    it('devuelve lo que responde el backend', async () => {
        const cuerpo = { guardadas: 3, por_etiqueta: { hola: 3 } }
        const peticion = vi.fn().mockResolvedValue(respuesta({ cuerpo }))
        await expect(subirLote(PAQUETE, { peticion, entorno: {} })).resolves.toEqual(cuerpo)
    })

    it('lanza con el motivo que da el backend', async () => {
        const cuerpo = { detail: 'muestra 1 del lote: falta la lista' }
        const peticion = vi.fn().mockResolvedValue(respuesta({ ok: false, cuerpo }))
        await expect(subirLote(PAQUETE, { peticion, entorno: {} })).rejects.toThrow('muestra 1 del lote')
    })

    it('tolera un error sin cuerpo JSON (un 502 de un proxy, por ejemplo)', async () => {
        const peticion = vi.fn().mockResolvedValue(respuesta({ ok: false, rompeAlLeer: true }))
        await expect(subirLote(PAQUETE, { peticion, entorno: {} })).rejects.toThrow('rechazo el lote')
    })

    it('deja subir el fallo de red', async () => {
        const peticion = vi.fn().mockRejectedValue(new Error('Failed to fetch'))
        await expect(subirLote(PAQUETE, { peticion, entorno: {} })).rejects.toThrow('Failed to fetch')
    })
})
