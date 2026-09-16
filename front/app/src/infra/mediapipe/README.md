# 🖐️ `infra/mediapipe/` — Adaptador de MediaPipe HandLandmarker

| Archivo | Responsabilidad |
|---|---|
| `detectorDeManos.js` | Crea **una sola vez** el detector; prueba GPU y cae a CPU si falla |
| `ladoDesdeCategoria.js` | `"Left"/"Right"` → `"izquierda"/"derecha"` (con `INVERTIR_LADO`) |
| `frameDesdeDeteccion.js` | Resultado de `detectForVideo` → `{ t, manos }` del contrato, redondeado a 6 decimales |

## 💡 Uso

```js
import { obtenerDetectorDeManos } from './detectorDeManos.js'
import { frameDesdeResultado } from './frameDesdeDeteccion.js'

const detector = await obtenerDetectorDeManos()
const frame = frameDesdeResultado(detector.detectForVideo(video, performance.now()), 0)
// → { t: 0, manos: [{ lado: 'derecha', score: 0.97, lm: [[x, y, z], ...21] }] }
```

## ⚠️ Antes de grabar el dataset

Levanta la mano **derecha** frente a la cámara en Entrenamiento y lee el rótulo del esqueleto. Si dice "izquierda", pon `INVERTIR_LADO = true` en `ladoDesdeCategoria.js`.
