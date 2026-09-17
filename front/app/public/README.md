# 🌍 `public/` — Archivos estáticos servidos tal cual

## 📖 Introducción

Vite copia esta carpeta **sin procesar** a la raíz del build. Lo que está aquí se
pide por **URL absoluta** (`/favicon.svg`, `/mediapipe/…`) y conserva su nombre
exacto, sin hash.

---

## 📂 Qué archivos y carpetas tiene

| Elemento | Qué es |
|---|---|
| `favicon.svg` | 🤟 Icono de la pestaña del navegador |
| [`mediapipe/`](mediapipe/) | 🖐️ Runtime WASM y modelo de detección de manos, alojados por nosotros |

---

## 🎯 Qué problema resuelve

Hay archivos que **no pueden pasar por el bundler**:

1. **El `.wasm`** lo carga el *glue code* de Emscripten en tiempo de ejecución, a
   partir de una ruta que se le pasa como cadena.
2. **El modelo `.task`** (7,8 MB) lo descarga el propio `HandLandmarker` por URL.
3. **El favicon** lo pide el navegador por una ruta fija declarada en el HTML.

Y, sobre todo, tener MediaPipe aquí evita depender del **CDN de Google en cada
carga**: si ese CDN falla o cambia una versión, la app dejaría de detectar manos.

---

## 🔗 Qué dependencias tiene

- Los binarios provienen del paquete `@mediapipe/tasks-vision` y del repositorio
  público de modelos de Google.
- Quien los consume es
  [`src/infra/mediapipe/detectorDeManos.js`](../src/infra/mediapipe/).
- `index.html` referencia `/favicon.svg`.

---

## 🧠 Cómo soluciona el problema

```
public/favicon.svg                  ──►  /favicon.svg
public/mediapipe/wasm/…             ──►  /mediapipe/wasm/…
public/mediapipe/models/….task      ──►  /mediapipe/models/hand_landmarker.task
```

Rutas absolutas y estables en los tres entornos: `pnpm dev`, `pnpm preview` y el
contenedor nginx.

En producción, `nginx.conf` cachea agresivamente solo `/assets/` (los archivos
con hash que genera Vite). Lo de `public/` se sirve con la política por defecto,
que es lo correcto: su nombre no cambia entre versiones.

---

## 🔍 Qué tienen los archivos

### `favicon.svg`

Icono vectorial de la pestaña; se declara en `index.html`:

```html
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
```

### `mediapipe/`

Dos subcarpetas con su propio README: [`wasm/`](mediapipe/wasm/) (runtime, tres
variantes) y [`models/`](mediapipe/models/) (el `.task`).

> ⚠️ **Tailwind no debe escanear esta carpeta.** `src/index.css` incluye
> `@source not "../public/mediapipe";` porque el *glue code* de Emscripten
> generaba clases falsas. `oxlint` también la ignora (`.oxlintrc.json`). No
> quites ninguna de las dos líneas.

---

## 💡 Ejemplos de uso

```js
// Rutas absolutas desde el código
const RUTA_WASM = '/mediapipe/wasm'
const RUTA_MODELO = '/mediapipe/models/hand_landmarker.task'
```

Comprobar que el build los sirve:

```bash
pnpm build && pnpm preview
curl -I http://localhost:4173/mediapipe/models/hand_landmarker.task
```

> 💡 Una imagen que use un componente **no** va aquí: va en
> [`src/assets/`](../src/assets/), para que Vite la optimice y le ponga hash.
