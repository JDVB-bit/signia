/** Los tres desenlaces del envio, contados en castellano. */
import { describe, expect, it } from 'vitest'

import { RESULTADOS_DE_ENVIO } from '../../../aplicacion/envioDeMuestras.js'
import { textoDeEnvio } from '../textosDeEnvio.js'

describe('textoDeEnvio', () => {
    it('confirma la subida con el numero de muestras', () => {
        const texto = textoDeEnvio({ resultado: RESULTADOS_DE_ENVIO.SUBIDO, cuantas: 4 })
        expect(texto).toBe('Se enviaron 4 muestras al servidor.')
    })

    it('concuerda en singular', () => {
        const texto = textoDeEnvio({ resultado: RESULTADOS_DE_ENVIO.SUBIDO, cuantas: 1 })
        expect(texto).toContain('1 muestra ')
    })

    it('explica el respaldo sin llamarlo error', () => {
        const texto = textoDeEnvio({
            resultado: RESULTADOS_DE_ENVIO.RESPALDADO,
            cuantas: 4,
            motivo: 'Failed to fetch',
        })
        expect(texto).toContain('respaldo')
        expect(texto).toContain('Failed to fetch')
    })

    it('avisa cuando no hay nada que enviar', () => {
        expect(textoDeEnvio({ resultado: RESULTADOS_DE_ENVIO.SIN_MUESTRAS, cuantas: 0 })).toContain(
            'no hay muestras',
        )
    })
})
