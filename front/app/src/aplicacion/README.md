# ⚙️ `aplicacion/` — Casos de uso

Combina reglas del dominio para resolver tareas concretas. Sin React ni APIs del navegador.

## 📄 Archivos

| Archivo | Responsabilidad | Gemelo en Python |
|---|---|---|
| `remuestreo.js` | De N frames a 48 índices (`Math.round` ≡ `int(x+0.5)`) | `aplicacion/remuestreo.py` |
| `construirEntrada.js` | Muestra → tensores planos `lm (T,2,21,3)` + `presencia (T,2)` | `aplicacion/preprocess.py` |
| `crearMuestra.js` | Frames grabados → muestra aislada del contrato | — |
| `fpsDeGrabacion.js` | fps reales de una grabación | — |
| `sesionDeGrabacion.js` | Identificador de sesión `AAAA-MM-DD-dispositivo` | — |
| `paqueteDeMuestras.js` | Lote exportable + nombre de fichero legible | — |

## 🔁 Flujo típico

```js
import { crearMuestra } from './crearMuestra.js'
import { construirEntrada } from './construirEntrada.js'

const muestra = crearMuestra({ etiqueta: 'hola', sesion: '2026-09-20-local', frames })
const { lm, presencia, dims } = construirEntrada(muestra)
// dims.lm → [48, 2, 21, 3]; listos para ort.Tensor en la Fase 6
```

> 🔒 `remuestreo.js` es la única pieza del preprocesado escrita dos veces. El resto de la normalización viaja **dentro del grafo ONNX**.
