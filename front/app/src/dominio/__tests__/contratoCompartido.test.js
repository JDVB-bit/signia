/** Mitad JS de la red de contrato cruzado (Fase 2 del plan).
 *
 * Lee `model/contrato.json` -generado por `model/scripts/exportar_contrato.py`
 * desde `dominio/contrato.py`- y comprueba que `contrato.js` declara los mismos
 * valores. La conformidad de la Fase 0 compara tensores y no veria un cambio en
 * `SCHEMA`, `IDX_MUNECA` o `N_MANOS`: este test cierra ese hueco.
 *
 * Si falla, uno de los dos lados cambio solo. El arreglo es decidir cual es el
 * correcto, no igualar el otro a ciegas: si el que cambio es Python hay que
 * reentrenar, y si es JS puede haber muestras ya grabadas con el valor viejo.
 */
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'

import * as contratoJs from '../contrato.js'

// De src/dominio/__tests__/ a la raiz del repo hay cinco niveles
const RUTA = fileURLToPath(new URL('../../../../../model/contrato.json', import.meta.url))
const contratoPy = JSON.parse(readFileSync(RUTA, 'utf8'))

/** Constantes que se llaman distinto en cada lenguaje, y solo esas. */
const ALIAS_EN_JS = { LADOS_CANONICOS: 'LADOS' }

/** Nombre que tiene en `contrato.js` la constante `clave` de Python. */
const nombreEnJs = (clave) => ALIAS_EN_JS[clave] ?? clave

describe('contrato.json', () => {
    it('esta generado por el script del modelo', () => {
        expect(contratoPy.generado_por).toBe('model/scripts/exportar_contrato.py')
    })

    it('trae constantes y la lista de compartidas', () => {
        expect(Object.keys(contratoPy.constantes).length).toBeGreaterThan(0)
        expect(contratoPy.compartidas_con_js.length).toBeGreaterThan(0)
    })
})

describe.each(contratoPy.compartidas_con_js)('constante compartida %s', (clave) => {
    const enJs = nombreEnJs(clave)

    it('esta declarada en contrato.js', () => {
        expect(contratoJs).toHaveProperty(enJs)
    })

    it('vale lo mismo que en Python', () => {
        expect(contratoJs[enJs]).toEqual(contratoPy.constantes[clave])
    })
})

describe('constantes que Python exporta y JS tambien declara', () => {
    // Vigila las que hoy son solo de Python (F, EPS_ESCALA...) desde el momento
    // en que el front las necesite: no hay que acordarse de ampliar el test
    const comunes = Object.keys(contratoPy.constantes).filter(
        (clave) => nombreEnJs(clave) in contratoJs,
    )

    it('hay al menos las compartidas', () => {
        expect(comunes.length).toBeGreaterThanOrEqual(contratoPy.compartidas_con_js.length)
    })

    it.each(comunes)('%s coincide', (clave) => {
        expect(contratoJs[nombreEnJs(clave)]).toEqual(contratoPy.constantes[clave])
    })
})

describe('coherencia interna del contrato de JS', () => {
    it('LADOS son los dos lados con nombre, en el orden canonico', () => {
        expect(contratoJs.LADOS).toEqual([contratoJs.LADO_IZQUIERDA, contratoJs.LADO_DERECHA])
    })

    it('hay una ranura de mano por lado canonico', () => {
        expect(contratoJs.LADOS).toHaveLength(contratoJs.N_MANOS)
    })

    it('el indice de la muneca esta dentro de los landmarks', () => {
        expect(contratoJs.IDX_MUNECA).toBeGreaterThanOrEqual(0)
        expect(contratoJs.IDX_MUNECA).toBeLessThan(contratoJs.N_LANDMARKS)
    })
})
