# 🧪 `dominio/__tests__/` — Tests de las reglas del negocio

## 📖 Introducción

Un archivo de test por módulo de [`dominio/`](../). Como las reglas son
funciones puras, estos tests **no necesitan navegador, ni cámara, ni DOM**:
corren en node y tardan milisegundos.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Módulo que verifica | Casos cubiertos |
|---|---|---|
| `manoDelFrame.test.js` | `manoDelFrame.js` | Mano ausente, frame vacío, gana el mayor score, empate por orden de aparición |
| `etiquetaDeSena.test.js` | `etiquetaDeSena.js` | Espacios y mayúsculas, texto ausente (`undefined`) |
| `reglasDeGrabacion.test.js` | `reglasDeGrabacion.js` | Tope de duración, grabación corta, grabación sin manos, conteo de frames útiles |

> `contrato.js` y `unidadesDeTiempo.js` no tienen test propio: son constantes, y
> quien las vigila de verdad es el test de conformidad contra Python
> ([`aplicacion/__tests__/`](../../aplicacion/__tests__/)).

---

## 🎯 Qué problema resuelve

Las reglas del dominio son **decisiones que afectan al dataset**, y un dataset
mal grabado no se arregla después. Estos tests fijan esas decisiones por
escrito:

- Que el desempate entre dos manos sea **determinista** (si no, el mismo vídeo
  produciría tensores distintos en dos ejecuciones).
- Que `"Hola"` y `"hola"` sean la misma clase, y no dos carpetas del dataset.
- Que el tope de grabación siga dejando margen sobre la ventana del modelo.

---

## 🔗 Qué dependencias tiene

- `vitest` (configurado en `vite.config.js` con `environment: 'node'`).
- Los propios módulos de `dominio/`. **Nada más**: ni mocks, ni jsdom.

---

## 🧠 Cómo soluciona el problema

Cada test describe la regla **en el idioma del negocio**, no en el de la
implementación. Por ejemplo, el tope de duración no se comprueba solo con su
valor, sino con la propiedad que debe cumplir:

```js
it('el tope deja margen de sobra sobre la ventana del modelo', () => { … })
```

Así, si alguien baja `DURACION_MAXIMA_MS` a 1 s, el test falla explicando **por
qué** está mal, en vez de limitarse a decir que un número cambió.

---

## 🔍 Qué tienen los archivos

| Test | Lo que garantiza |
|---|---|
| `con dos manos del mismo lado gana la de mayor score` | La regla es la misma que `Frame.mano()` en Python |
| `ante un empate gana la primera` | El desempate es determinista |
| `tolera un frame sin manos` | Un frame vacío no rompe el bucle de vídeo |
| `una grabacion demasiado corta se descarta` | `FRAMES_MINIMOS` se aplica de verdad |
| `basta con que la mano aparezca en algun frame` | No se exige mano en todos los frames: entrar al encuadre es normal |
| `convierte la ausencia de texto en cadena vacia` | `normalizarEtiqueta(undefined)` no lanza |

---

## 💡 Ejemplos de uso

```bash
pnpm test                       # toda la suite (105 tests)
pnpm test -- dominio            # solo estos
pnpm test:watch -- dominio      # en vigilancia mientras se programa
```

Añadir una regla nueva al dominio significa añadir aquí su test:

```js
import { describe, expect, it } from 'vitest'
import { miRegla } from '../miRegla.js'

describe('miRegla', () => {
    it('describe la propiedad en lenguaje de negocio', () => {
        expect(miRegla(entrada)).toBe(salidaEsperada)
    })
})
```
