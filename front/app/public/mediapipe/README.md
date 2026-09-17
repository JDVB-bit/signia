# 🖐️ `public/mediapipe/` — MediaPipe alojado localmente

## 📖 Introducción

El detector de manos necesita dos cosas en tiempo de ejecución: un **runtime
WebAssembly** y un **modelo** `.task`. Aquí están los dos, servidos desde nuestro
propio dominio en vez de desde el CDN de Google.

---

## 📂 Qué carpetas tiene y qué hay en cada una

| Carpeta | Contenido | Tamaño aprox. |
|---|---|---|
| [`wasm/`](wasm/) | Runtime de visión: 3 variantes (SIMD, módulo, sin SIMD) + su *glue code* JS | ~35 MB |
| [`models/`](models/) | `hand_landmarker.task`, modelo oficial en `float16` | ~7,8 MB |

---

## 🎯 Qué problema resuelve

1. 🔌 **Independencia de terceros.** Sin esto, cada carga de la app depende de
   que el CDN de Google responda y de que no cambie la versión sin avisar.
2. ⚡ **Latencia y caché.** Se sirven desde el mismo origen, con las cabeceras de
   nuestro nginx.
3. 🔒 **Reproducibilidad.** El modelo queda congelado en el repositorio: el
   dataset grabado y el modelo entrenado corresponden a **este** detector.

---

## 🔗 Qué dependencias tiene

| Origen | Qué aporta |
|---|---|
| `@mediapipe/tasks-vision` (ver `package.json`) | Los archivos de `wasm/` |
| Repositorio de modelos de Google | `hand_landmarker.task` |
| Consumidor único | [`src/infra/mediapipe/detectorDeManos.js`](../../src/infra/mediapipe/detectorDeManos.js) |

---

## 🧠 Cómo soluciona el problema

```js
FilesetResolver.forVisionTasks('/mediapipe/wasm')      // elige la variante WASM
  └─► HandLandmarker.createFromOptions(ficheros, {
        baseOptions: { modelAssetPath: '/mediapipe/models/hand_landmarker.task',
                       delegate: 'GPU' },              // con respaldo en CPU
        runningMode: 'VIDEO',
        numHands: 2,
      })
```

El *fileset* detecta si el navegador soporta SIMD y carga el binario adecuado:
por eso hay que copiar **todas** las variantes, no solo la rápida.

---

## 🔍 Qué tienen los archivos

Cada subcarpeta tiene su propio README con el detalle:

- [`wasm/README.md`](wasm/) — las tres variantes y cuándo se usa cada una.
- [`models/README.md`](models/) — qué devuelve el modelo y el aviso del espejo.

---

## 💡 Ejemplos de uso

Actualizar el runtime tras subir la versión del paquete:

```bash
cp node_modules/@mediapipe/tasks-vision/wasm/* public/mediapipe/wasm/
```

Actualizar el modelo (`float16/latest` apunta siempre a la última release):

```bash
curl -L -o public/mediapipe/models/hand_landmarker.task \
  https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task
```

> 🚨 **Cambiar el modelo no es gratis.** Los landmarks que produce son la entrada
> del sistema: otra versión puede desplazar ligeramente los puntos y romper la
> comparabilidad con el dataset ya grabado. Si se actualiza, conviene reentrenar
> y anotarlo en `.claude/mejoras.md`.

> ⚠️ **Nota sobre Tailwind:** `src/index.css` contiene
> `@source not "../public/mediapipe";`. Tailwind v4 escanea todo el proyecto y el
> *glue code* de Emscripten generaba clases falsas (`.visible`, `.absolute`…).
> **No borrar esa línea.**
