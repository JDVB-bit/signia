# 🧠 `models/` — Modelo de detección de manos

| Archivo | Qué es |
|---|---|
| `hand_landmarker.task` | Modelo oficial de Google (float16): detecta hasta 2 manos y devuelve 21 landmarks `(x, y, z)` por mano |

Se carga así (ver `src/infra/mediapipe/detectorDeManos.js`):

```js
HandLandmarker.createFromOptions(ficheros, {
  baseOptions: { modelAssetPath: '/mediapipe/models/hand_landmarker.task', delegate: 'GPU' },
  runningMode: 'VIDEO',
  numHands: 2,
})
```
