# MediaPipe self-hosted assets

Estos archivos se sirven localmente (no desde el CDN de Google) para no depender
de un tercero en cada carga de la app. Los usa [`src/lib/handLandmarker.js`](../../src/lib/handLandmarker.js).

## wasm/

Copiado directo de `node_modules/@mediapipe/tasks-vision/wasm/` (paquete
`@mediapipe/tasks-vision`, ver versión en `package.json`). Se actualiza solo:

```bash
cp node_modules/@mediapipe/tasks-vision/wasm/* public/mediapipe/wasm/
```

## models/hand_landmarker.task

Modelo oficial de Google, descargado de:
https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task

Para actualizarlo a la última versión, volver a descargar de esa misma URL
(el path `float16/latest/` siempre apunta a la última release del modelo float16).

## Nota sobre Tailwind

`src/index.css` tiene `@source not "../public/mediapipe";` porque Tailwind v4
escanea automáticamente todo el proyecto buscando clases usadas, y el JS
glue-code de Emscripten en `wasm/*.js` generaba falsos positivos (clases como
`.visible`/`.absolute` que nadie usa). No borrar esa línea.
