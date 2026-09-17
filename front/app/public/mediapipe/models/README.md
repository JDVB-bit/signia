# 🧠 `public/mediapipe/models/` — Modelo de detección de manos

## 📖 Introducción

El modelo oficial de Google que localiza las manos en la imagen y devuelve sus
**21 landmarks** por mano. Es **la entrada de todo el sistema**: sin estos puntos
no hay dataset, ni features, ni predicción.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Qué es |
|---|---|
| `hand_landmarker.task` | Modelo `float16` de MediaPipe HandLandmarker (~7,8 MB). Paquete cerrado con detector de palma + regresor de landmarks + clasificador de *handedness* |

---

## 🎯 Qué problema resuelve

Convierte píxeles en **geometría**. En vez de entrenar con vídeo —caro, pesado y
sensible a la ropa, la luz o el fondo—, SignIA entrena con 21 puntos por mano:

| | Vídeo | Landmarks |
|---|---|---|
| Tamaño de una muestra | MB | KB |
| Sensible a fondo/ropa/luz | Mucho | Poco |
| Grabable a mano en un portátil | No | Sí |

Además aporta el **`handedness`** (`Left` / `Right`), del que salen las ranuras
canónicas del tensor del contrato.

---

## 🔗 Qué dependencias tiene

Lo carga `@mediapipe/tasks-vision` mediante
`baseOptions.modelAssetPath = '/mediapipe/models/hand_landmarker.task'`, desde
[`src/infra/mediapipe/detectorDeManos.js`](../../../src/infra/mediapipe/detectorDeManos.js).
Necesita el runtime de [`../wasm/`](../wasm/) para ejecutarse.

---

## 🧠 Cómo soluciona el problema

Salida por frame, en coordenadas **normalizadas** `[0, 1]` respecto al encuadre:

| Campo | Contenido |
|---|---|
| `landmarks[i]` | 21 puntos `{ x, y, z }` de la mano `i` |
| `handedness[i][0]` | `{ categoryName: "Left" \| "Right", score }` |

Que estén normalizadas es lo que permite que el tensor no dependa de la
resolución de la cámara: la misma seña grabada en 720p y en 1080p produce
prácticamente los mismos números.

La `z` es una profundidad **relativa** y ruidosa: el contrato la conserva dentro
de la forma, pero **no** la usa para la escala ni para la posición.

---

## 🔍 Qué tiene el archivo

`hand_landmarker.task` es un contenedor binario (no editable) que incluye:

1. **Detector de palma** — encuentra dónde hay manos en la imagen.
2. **Regresor de landmarks** — coloca los 21 puntos dentro de cada mano.
3. **Clasificador de handedness** — decide si es izquierda o derecha, con score.

Configuración con la que lo usa SignIA: `runningMode: 'VIDEO'`, `numHands: 2`,
delegado `GPU` con respaldo en `CPU`.

---

## 💡 Ejemplos de uso

```js
const detector = await obtenerDetectorDeManos()
const resultado = detector.detectForVideo(video, performance.now())

resultado.landmarks[0][0]    // { x: 0.51, y: 0.62, z: -0.02 }  ← muñeca
resultado.handedness[0][0]   // { categoryName: 'Right', score: 0.98 }
```

Actualizar el modelo:

```bash
curl -L -o hand_landmarker.task \
  https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task
```

> 🪞 **Cuidado con el espejo.** El vídeo se pinta espejado para que el usuario se
> vea natural, pero al detector llega el frame tal cual. Por eso el overlay
> rotula el lado junto a la muñeca y existe el interruptor `INVERTIR_LADO` en
> `src/infra/mediapipe/ladoDesdeCategoria.js`: **se verifica antes de grabar el
> dataset**, no después.
