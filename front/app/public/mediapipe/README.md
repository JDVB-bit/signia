# 🖐️ `public/mediapipe/` — MediaPipe alojado localmente

Se sirve desde nuestro dominio (no desde el CDN de Google) para no depender de un tercero en cada carga. Lo consume [`src/infra/mediapipe/detectorDeManos.js`](../../src/infra/mediapipe/detectorDeManos.js).

| Carpeta | Contenido |
|---|---|
| [`wasm/`](wasm/) | Runtime WebAssembly de `@mediapipe/tasks-vision` |
| [`models/`](models/) | Modelo `hand_landmarker.task` (float16) |

## 🔄 Actualizar

```bash
# runtime: tras subir la versión de @mediapipe/tasks-vision
cp node_modules/@mediapipe/tasks-vision/wasm/* public/mediapipe/wasm/

# modelo: la ruta float16/latest apunta siempre a la última release
curl -L -o public/mediapipe/models/hand_landmarker.task \
  https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task
```

## ⚠️ Nota sobre Tailwind

`src/index.css` contiene `@source not "../public/mediapipe";`: Tailwind v4 escanea todo el proyecto y el glue-code de Emscripten generaba clases falsas (`.visible`, `.absolute`...). **No borrar esa línea.**
