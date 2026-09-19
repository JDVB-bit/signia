# 📡 `red/` — Hablar con la API de SignIA

## 📖 Introducción

El adaptador de red del front: dónde está el backend y cómo se le manda un lote
de muestras. Es **solo transporte** — qué hacer si falla lo decide la capa de
aplicación ([`envioDeMuestras.js`](../../aplicacion/envioDeMuestras.js)).

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Responsabilidad |
|---|---|
| `urlDeLaApi.js` | 🌐 La base de la API y sus endpoints, en un único sitio |
| `clienteDeMuestras.js` | 📤 `subirLote(paquete)` → `POST /muestras` |
| [`__tests__/`](__tests__/) | 🧪 12 tests con un `fetch` de mentira |

---

## 🎯 Qué problema resuelve

Antes, *Enviar* descargaba un JSON que alguien tenía que mover a mano hasta el
dataset. Ese paso manual es donde se pierden muestras y se confunden sesiones.

Y dos problemas de red que hay que tratar distinto:

| Situación | Qué significa |
|---|---|
| El backend está apagado | Normal en local: hay que **guardar el lote igualmente** |
| El backend responde `422` | El lote no cumple el contrato: hay que **enseñar por qué** |

---

## 🔗 Qué dependencias tiene

Ninguna librería: `fetch` del navegador. La URL sale de `import.meta.env`, que
Vite resuelve en tiempo de compilación.

---

## 🧠 Cómo soluciona el problema

### 🔧 La URL no está escrita en el código que la usa

```js
export const URL_API_POR_DEFECTO = 'http://localhost:8000'
export function baseDeLaApi(entorno = import.meta.env) { … }
```

En desarrollo apunta al backend local; en el despliegue se cambia con
`VITE_API_URL` sin tocar código. Es la misma idea que `rutas.js` con las rutas
del sitio: **una sola fuente**.

### 💉 `fetch` se puede sustituir

```js
subirLote(paquete, { peticion: miFetch, entorno: {} })
```

Por eso los tests comprueban el método, las cabeceras y el cuerpo exactos sin
levantar un servidor.

### 📣 El motivo del backend llega intacto

Si la respuesta no es `ok`, el cliente lee `detail` y lo pone en el `Error`. Ese
texto ya dice *qué muestra* del lote falla, porque lo genera el mismo validador
que usa el entrenamiento. Si el cuerpo no es JSON (un `502` de un proxy, por
ejemplo), hay un mensaje de reserva y no una excepción rara.

---

## 🔍 Qué tienen los archivos

### `urlDeLaApi.js`

| Elemento | Qué es |
|---|---|
| `URL_API_POR_DEFECTO` | `http://localhost:8000`, el backend local |
| `ENDPOINTS` | `/muestras`, `/senas`, `/salud` |
| `baseDeLaApi(entorno)` | La variable `VITE_API_URL` o el local; quita la barra final |
| `urlDe(endpoint, entorno)` | La URL absoluta |

### `clienteDeMuestras.js`

| Elemento | Qué es |
|---|---|
| `subirLote(paquete, opciones)` | `POST` del lote; devuelve `{guardadas, identificadores, por_etiqueta}` |
| `motivoDelFallo(respuesta)` | Lee `detail` sin romperse si no hay JSON |

---

## 💡 Ejemplos de uso

```js
import { subirLote } from './infra/red/clienteDeMuestras.js'

try {
    const { guardadas, por_etiqueta } = await subirLote(paquete)
    console.log(`el servidor guardo ${guardadas}`, por_etiqueta)
} catch (error) {
    // El backend esta apagado o rechazo el lote: `error.message` lo explica
}
```

Apuntar a otro backend al compilar:

```bash
VITE_API_URL=https://api.signia.example pnpm build
```
