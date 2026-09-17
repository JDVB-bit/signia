# 🖐️ `infra/mediapipe/` — Adaptador de MediaPipe HandLandmarker

## 📖 Introducción

La frontera con la librería de Google. Aquí se crea el detector y se traduce lo
que devuelve (`landmarks` + `handedness`) al **frame del contrato** que entiende
el resto de SignIA.

Es el único punto del front que importa `@mediapipe/tasks-vision`.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Responsabilidad |
|---|---|
| `detectorDeManos.js` | 🤖 Crea **una sola vez** el detector; prueba GPU y cae a CPU si falla |
| `ladoDesdeCategoria.js` | ✋ `"Left"` / `"Right"` → `"izquierda"` / `"derecha"`, con el interruptor `INVERTIR_LADO` |
| `frameDesdeDeteccion.js` | 🎞️ Resultado de `detectForVideo` → `{ t, manos }` del contrato |
| [`__tests__/`](__tests__/) | 🧪 Tests de la traducción (sin cámara ni WASM) |

---

## 🎯 Qué problema resuelve

1. **El coste de arrancar.** El runtime WASM y el modelo pesan varios MB y
   tardan en inicializarse: crear un detector por componente sería inaceptable.
2. **La fragilidad del entorno.** Sin WebGL, o con drivers rotos, el delegado
   `GPU` falla; sin respaldo, la app se quedaría sin detector.
3. **La forma del dato.** MediaPipe devuelve objetos `{x, y, z}` con nombres en
   inglés; el contrato pide arrays `[x, y, z]` redondeados y lados en español.
4. **El espejo.** El vídeo se pinta espejado pero al detector llega el frame tal
   cual: hay que poder corregir el lado **antes** de grabar el dataset.

---

## 🔗 Qué dependencias tiene

- `@mediapipe/tasks-vision` (`FilesetResolver`, `HandLandmarker`).
- Los assets de [`public/mediapipe/`](../../../public/mediapipe/): runtime WASM
  y `hand_landmarker.task`.
- [`../../dominio/contrato.js`](../../dominio/contrato.js) — `N_LANDMARKS`,
  `N_MANOS`, lados y `SCORE_MAXIMO`.

---

## 🧠 Cómo soluciona el problema

### 🔁 Instancia única con reintento

```
obtenerDetectorDeManos()
   └─ ¿hay promesa? ── sí ──► se reutiliza
                    └─ no ──► crearDetector()
                                 ├─ delegado GPU  ✅ → detector
                                 └─ falla → delegado CPU ✅ → detector
                                             └─ falla → se OLVIDA la promesa
```

Olvidar la promesa fallida es deliberado: si el primer intento falla (por
ejemplo, porque la pestaña aún no tenía WebGL), volver a activar la cámara
reintenta en vez de heredar el error para siempre.

### 🎞️ Traducción honesta del frame

- Un frame puede quedarse con **0, 1 o 2 manos**: la ausencia es información y
  no se rellena.
- Las manos con handedness desconocido o con un número de landmarks distinto de
  21 **se ignoran**, en vez de inventarles datos.
- Se aceptan las dos formas del campo (`handedness` y `handednesses`), porque
  cambia según la versión de `tasks-vision`.

---

## 🔍 Qué tienen los archivos

### `detectorDeManos.js`

| Constante / función | Valor o efecto |
|---|---|
| `RUTA_WASM` | `/mediapipe/wasm` |
| `RUTA_MODELO` | `/mediapipe/models/hand_landmarker.task` |
| `MODO_VIDEO` | `'VIDEO'` — optimizado para frames consecutivos |
| `DELEGADOS` | `['GPU', 'CPU']`, en orden de preferencia |
| `obtenerDetectorDeManos()` | Promesa compartida del detector (`numHands: 2`) |

### `ladoDesdeCategoria.js`

| Elemento | Detalle |
|---|---|
| `INVERTIR_LADO` | `false`. ⚠️ Interruptor del riesgo del espejo |
| `ladoDesdeCategoria(categoria, invertir)` | Lado del contrato, o `null` si la categoría es desconocida |

### `frameDesdeDeteccion.js`

| Elemento | Detalle |
|---|---|
| `DECIMALES_COORDENADA` | `6`. MediaPipe no es más preciso, el JSON ocupa la mitad y sigue muy por encima del `1e-5` del test |
| `Z_POR_DEFECTO` | `0` si el detector no reporta profundidad |
| `frameDesdeResultado(resultado, t, opciones)` | `{ t, manos: [{ lado, score, lm }] }` |

---

## 💡 Ejemplos de uso

```js
import { obtenerDetectorDeManos } from './detectorDeManos.js'
import { frameDesdeResultado } from './frameDesdeDeteccion.js'

const detector = await obtenerDetectorDeManos()
const frame = frameDesdeResultado(detector.detectForVideo(video, performance.now()), 0)
// → { t: 0, manos: [{ lado: 'derecha', score: 0.97, lm: [[0.51, 0.62, -0.02], …21] }] }
```

```js
import { ladoDesdeCategoria } from './ladoDesdeCategoria.js'

ladoDesdeCategoria('Right')          // 'derecha'
ladoDesdeCategoria('Right', true)    // 'izquierda'  (espejo corregido)
ladoDesdeCategoria('Foot')           // null
```

---

## ⚠️ Antes de grabar el dataset

Abre **Entrenamiento**, activa la cámara y levanta la mano **derecha**. Lee el
rótulo que dibuja el esqueleto junto a la muñeca:

| Dice | Acción |
|---|---|
| `derecha` | ✅ Todo correcto, a grabar |
| `izquierda` | Pon `INVERTIR_LADO = true` en `ladoDesdeCategoria.js` **antes** de grabar |

Corregirlo después obligaría a reparar el dataset entero: los lados quedarían
cambiados en todas las muestras ya guardadas.
