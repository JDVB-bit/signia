/** De donde sale la URL de la API: la variable de entorno o el local. */
import { describe, expect, it } from 'vitest'

import { ENDPOINTS, URL_API_POR_DEFECTO, baseDeLaApi, urlDe } from '../urlDeLaApi.js'

describe('baseDeLaApi', () => {
    it('usa el backend local cuando no hay variable', () => {
        expect(baseDeLaApi({})).toBe(URL_API_POR_DEFECTO)
    })

    it('respeta la variable del despliegue', () => {
        expect(baseDeLaApi({ VITE_API_URL: 'https://api.signia.example' })).toBe('https://api.signia.example')
    })

    it('quita la barra final para no generar URLs con dos', () => {
        expect(baseDeLaApi({ VITE_API_URL: 'https://api.example/' })).toBe('https://api.example')
    })

    it('ignora una variable vacia', () => {
        expect(baseDeLaApi({ VITE_API_URL: '' })).toBe(URL_API_POR_DEFECTO)
    })
})

describe('urlDe', () => {
    it('pega la base con el endpoint', () => {
        expect(urlDe(ENDPOINTS.MUESTRAS, {})).toBe(`${URL_API_POR_DEFECTO}/muestras`)
    })

    it('conoce los tres endpoints que consume el front', () => {
        expect(Object.values(ENDPOINTS)).toEqual(['/muestras', '/senas', '/salud'])
    })
})
