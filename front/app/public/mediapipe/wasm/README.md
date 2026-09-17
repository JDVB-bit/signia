# ⚙️ `public/mediapipe/wasm/` — Runtime WebAssembly de MediaPipe

## 📖 Introducción

Copia literal de `node_modules/@mediapipe/tasks-vision/wasm/`. Es el motor que
ejecuta el modelo de manos dentro del navegador.

**Ningún archivo de esta carpeta se edita a mano**: se sustituyen enteros al
actualizar el paquete.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Para qué |
|---|---|
| `vision_wasm_internal.wasm` + `.js` | Runtime con **SIMD**: el rápido, para navegadores modernos |
| `vision_wasm_module_internal.wasm` + `.js` | Variante empaquetada como **módulo ES** |
| `vision_wasm_nosimd_internal.wasm` + `.js` | Respaldo **sin SIMD**, para navegadores que no lo soportan |

Los `.js` son *glue code* generado por Emscripten: cargan el `.wasm`, reservan
memoria y exponen la API a JavaScript.

---

## 🎯 Qué problema resuelve

Ejecutar **visión por computador en el cliente**, a ritmo de vídeo y sin enviar
imágenes a ningún servidor. El usuario nunca sube su cara ni su habitación: solo
—si decide grabar— 21 coordenadas por mano.

Eso tiene dos consecuencias grandes para SignIA:

- 🔐 **Privacidad por diseño**: el vídeo no sale del dispositivo.
- 💸 **Coste cero de inferencia**: no hace falta un servidor con GPU.

---

## 🔗 Qué dependencias tiene

Ninguna propia. Los carga
`FilesetResolver.forVisionTasks('/mediapipe/wasm')` desde
[`src/infra/mediapipe/detectorDeManos.js`](../../../src/infra/mediapipe/detectorDeManos.js).

---

## 🧠 Cómo soluciona el problema

```
FilesetResolver.forVisionTasks('/mediapipe/wasm')
        │
        ├── ¿SIMD disponible? ──► vision_wasm_internal.wasm       (rápido)
        └── si no             ──► vision_wasm_nosimd_internal.wasm (compatible)
```

El resolutor comprueba las capacidades del navegador y elige la variante
adecuada. Por eso deben estar **todas**: si falta la `nosimd`, un navegador sin
SIMD se queda sin detector.

---

## 🔍 Qué tienen los archivos

Son binarios y código generado; no hay nada que leer ni que documentar línea a
línea. Lo único relevante para el proyecto:

| Hecho | Consecuencia |
|---|---|
| Pesan ~35 MB en total | Se sirven desde `public/`, nunca por el bundler |
| El `.js` es *glue code* de Emscripten | Tailwind y oxlint deben **ignorar** esta carpeta |
| La variante la elige el resolutor | No se puede borrar ninguna "para ahorrar espacio" |

---

## 💡 Ejemplos de uso

```bash
# Actualizar tras cambiar la versión de @mediapipe/tasks-vision
cp node_modules/@mediapipe/tasks-vision/wasm/* public/mediapipe/wasm/
```

```bash
# Comprobar que el servidor los entrega
pnpm preview
curl -I http://localhost:4173/mediapipe/wasm/vision_wasm_internal.wasm
```

> 📌 Si el detector falla al arrancar, mira primero aquí: un 404 en uno de estos
> archivos se manifiesta como "No se pudo cargar el detector de manos" en la
> página de Entrenamiento.
