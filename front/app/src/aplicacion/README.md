# ⚙️ `aplicacion/` — Casos de uso del front

## 📖 Introducción

La capa que **combina las reglas del dominio para resolver tareas concretas**:
remuestrear una grabación, construir el tensor, armar la muestra del contrato y
preparar el lote que se exporta.

No sabe nada de React ni del navegador: recibe datos, devuelve datos. Es gemela
de `model/signia_modelo/aplicacion/` en Python.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Responsabilidad | Gemelo en Python |
|---|---|---|
| `remuestreo.js` | ⏱️ De `n` frames a `T = 48` índices | `aplicacion/remuestreo.py` |
| `construirEntrada.js` | 🧱 Muestra → tensores planos `lm` + `presencia` | `aplicacion/preprocess.py` |
| `crearMuestra.js` | 📼 Frames grabados → muestra aislada del contrato | — |
| `fpsDeGrabacion.js` | 🎞️ fps reales de una grabación | — |
| `sesionDeGrabacion.js` | 🗓️ Identificador de la tanda: `AAAA-MM-DD-dispositivo` | — |
| `paqueteDeMuestras.js` | 📦 Lote exportable + nombre de fichero legible | — |
| [`__tests__/`](__tests__/) | 🧪 Tests propios y el de conformidad con Python | — |

---

## 🎯 Qué problema resuelve

1. **La deriva silenciosa entre navegador y entrenamiento.** El remuestreo es la
   única pieza del preprocesado escrita dos veces; si las dos versiones dejaran
   de coincidir, el modelo fallaría en producción y funcionaría en los tests.
2. **La longitud variable.** Una seña puede durar 0,8 s o 3 s, pero el modelo
   espera siempre `(48, 128)`.
3. **El formato de intercambio.** Lo que el front produce tiene que ser
   exactamente lo que Python valida y, en la Fase 5, lo que acepte
   `POST /muestras`.

---

## 🔗 Qué dependencias tiene

- [`../dominio/`](../dominio/) — constantes del contrato y reglas.
- **Nada más.** Sin React, sin MediaPipe, sin APIs del navegador.
- Contraparte de verificación: los fixtures de `model/tests/fixtures/`.

---

## 🧠 Cómo soluciona el problema

### ⏱️ Remuestreo: elegir, nunca interpolar

```
indice(i) = Math.round( i * (n - 1) / (T - 1) )     para i = 0 .. T-1
```

- Se **eligen** frames existentes. Interpolar entre un frame con mano y otro sin
  ella inventaría medias manos que MediaPipe nunca produjo.
- Si sobran frames se saltan; si faltan se repiten. Los extremos siempre se
  conservan: `indice(0) = 0`, `indice(T-1) = n-1`.
- `Math.round` equivale al `int(x + 0.5)` de Python — **no** al `round()` de
  Python, que redondea al par (`round(0.5) == 0`). Esa diferencia bastaría para
  que los dos lados vieran tensores distintos.

### 🧱 Tensor crudo, sin normalizar

Aquí **no** se resta la muñeca ni se calcula la escala: eso viaja dentro del
grafo ONNX, para que entrenamiento e inferencia ejecuten literalmente el mismo
código (principio 2 del plan).

```
muestra.frames ──► indicesRemuestreo ──► apilarFrames ──► { lm, presencia, dims }
```

| Salida | Forma | Contenido |
|---|---|---|
| `lm` | `(n, 2, 21, 3)` | Landmarks crudos, ranura `0 = izquierda`, `1 = derecha` |
| `presencia` | `(n, 2)` | `1` si esa mano está en el frame, `0` si no |

Se devuelven como `Float32Array` **planos** y en orden C: es lo que espera
`ort.Tensor` de onnxruntime-web y lo mismo que hace numpy.

---

## 🔍 Qué tienen los archivos

### `remuestreo.js`

`indicesRemuestreo(nFrames, destino = T)` → array de índices. Lanza `Error` con
secuencia vacía o destino inválido; con `destino === 1` devuelve `[0]` sin
dividir.

### `construirEntrada.js`

| Función | Qué hace |
|---|---|
| `apilarFrames(frames)` | Apila frames **ya elegidos**; la mano ausente queda en ceros y con presencia `0` (eso distingue "no hay mano" de "hay una mano en el origen") |
| `construirEntrada(muestra, destino = T)` | Remuestrea y apila: la muestra completa → ventana fija |

### `crearMuestra.js`

`crearMuestra({ etiqueta, sesion, frames, fpsAprox })` → objeto del contrato.
Reindexa `t` desde 0 (la muestra es una grabación nueva, no un trozo del bucle),
normaliza la etiqueta y **lanza** si falta etiqueta, sesión o frames.

### `fpsDeGrabacion.js`

`fpsDe(nFrames, duracionMs)` → fps reales, o `null` si la duración no es válida.

### `sesionDeGrabacion.js`

`idSesion(fecha, dispositivo)` → `2026-09-20-local`. La `sesion` es lo que
permite la evaluación honesta de la Fase 4: **el split del dataset es por
sesión, nunca aleatorio**.

### `paqueteDeMuestras.js`

| Función | Salida |
|---|---|
| `paqueteDeMuestras(muestras)` | `{ schema: 1, muestras }` — exactamente lo que consumirá el endpoint |
| `nombreDeFichero(muestras, fecha)` | `signia-hola-2026-09-20-local.json`, o `signia-3-senas-…` si el lote es mixto |

---

## 💡 Ejemplos de uso

```js
import { crearMuestra } from './crearMuestra.js'
import { construirEntrada } from './construirEntrada.js'
import { idSesion } from './sesionDeGrabacion.js'

const muestra = crearMuestra({ etiqueta: 'Hola', sesion: idSesion(), frames })
muestra.etiqueta            // 'hola'  (normalizada)

const { lm, presencia, dims } = construirEntrada(muestra)
dims.lm                     // [48, 2, 21, 3]  → listo para ort.Tensor (Fase 6)
presencia.length            // 96  (= 48 × 2)
```

```js
import { nombreDeFichero, paqueteDeMuestras } from './paqueteDeMuestras.js'

descargarJson(nombreDeFichero(muestras), paqueteDeMuestras(muestras))
```

> 🔒 `remuestreo.js` es la única pieza del preprocesado escrita dos veces. Si la
> tocas, ejecuta **las dos** suites (`pnpm test` y `pytest`) antes de commitear.
