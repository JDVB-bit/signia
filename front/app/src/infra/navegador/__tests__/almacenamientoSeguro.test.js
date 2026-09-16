/** El acceso al almacenamiento del navegador nunca debe tumbar la app. */
import { afterEach, describe, expect, it, vi } from 'vitest'

import { guardarLocal, leerDeSesion, leerLocal } from '../almacenamientoSeguro.js'

/** Almacen en memoria con la misma interfaz que localStorage. */
function almacenEnMemoria() {
    const datos = new Map()
    return {
        getItem: (clave) => (datos.has(clave) ? datos.get(clave) : null),
        setItem: (clave, valor) => datos.set(clave, String(valor)),
    }
}

afterEach(() => {
    vi.unstubAllGlobals()
})

describe('almacenamientoSeguro', () => {
    it('sin window (tests, SSR) lee null y guardar no lanza', () => {
        expect(leerLocal('clave')).toBeNull()
        expect(() => guardarLocal('clave', 'valor')).not.toThrow()
    })

    it('lee lo que guarda cuando el almacen funciona', () => {
        vi.stubGlobal('window', { localStorage: almacenEnMemoria() })
        guardarLocal('tema', 'dark')
        expect(leerLocal('tema')).toBe('dark')
    })

    it('si el almacen lanza (modo privado) se comporta como vacio', () => {
        const roto = {
            getItem: () => {
                throw new Error('SecurityError')
            },
            setItem: () => {
                throw new Error('QuotaExceededError')
            },
        }
        vi.stubGlobal('window', { localStorage: roto, sessionStorage: roto })
        expect(leerLocal('tema')).toBeNull()
        expect(leerDeSesion('permiso')).toBeNull()
        expect(() => guardarLocal('tema', 'dark')).not.toThrow()
    })
})
