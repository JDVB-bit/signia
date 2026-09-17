# 🔌 `infra/` — Adaptadores a tecnologías externas

## 📖 Introducción

La capa que toca **lo que no es nuestro**: la librería de Google, el `<canvas>`,
la cámara, el almacenamiento del navegador. Traduce esos detalles al lenguaje
del dominio y aísla al resto de la aplicación de ellos.

Si mañana cambia MediaPipe, el almacenamiento o la forma de descargar un
fichero, **solo se toca esta carpeta**.

---

## 📂 Qué carpetas tiene y qué hace cada una

| Carpeta | Adapta… | Archivos |
|---|---|---|
| [`mediapipe/`](mediapipe/) | El detector de manos de Google → frames del contrato | `detectorDeManos.js`, `ladoDesdeCategoria.js`, `frameDesdeDeteccion.js` |
| [`canvas/`](canvas/) | El dibujo del esqueleto sobre el vídeo | `dibujarManos.js`, `pintarManosSobreVideo.js` |
| [`navegador/`](navegador/) | Cámara, almacenamiento, descargas y tema | `camara.js`, `almacenamientoSeguro.js`, `descargarJson.js`, `permisoDeCamara.js`, `preferenciaDeTema.js`, `registroDeIntro.js` |

---

## 🎯 Qué problema resuelve

1. **Que una librería externa no se infiltre en todo el código.** MediaPipe se
   importa en **un solo archivo**; el resto de la app no sabe que existe.
2. **Que las APIs frágiles no tumben la aplicación.** `localStorage` lanza una
   excepción con solo tocarlo en modo privado; la cámara puede no existir.
3. **Que el dominio siga siendo verificable sin navegador.** Al empujar todo lo
   impuro aquí, `dominio/` y `aplicacion/` se prueban en node.

---

## 🔗 Qué dependencias tiene

| Dependencia | Dónde se usa |
|---|---|
| `@mediapipe/tasks-vision` | Solo en `mediapipe/detectorDeManos.js` |
| Assets de `public/mediapipe/` | Modelo `.task` y runtime WASM |
| APIs del navegador | `navigator.mediaDevices`, `localStorage`, `sessionStorage`, `URL.createObjectURL`, `CanvasRenderingContext2D` |
| [`../dominio/`](../dominio/) | Constantes del contrato (landmarks, lados) |

**No importa React**: los hooks que usan estos adaptadores viven en
[`../presentacion/hooks/`](../presentacion/hooks/).

---

## 🧠 Cómo soluciona el problema

```
presentacion/  (React)
     │  usa
     ▼
   infra/  ──► @mediapipe, canvas, getUserMedia, storage
     │  traduce a
     ▼
  dominio/  (frames, lados, contrato)
```

Cada adaptador expone una función con **vocabulario del proyecto**
(`abrirCamara`, `frameDesdeResultado`, `permisoConcedidoEnEstaVisita`) en vez de
la API cruda. Eso permite:

- **Sustituir** la tecnología sin tocar la interfaz.
- **Degradar con elegancia**: si el almacenamiento falla, se pierde el recuerdo,
  no la funcionalidad; si la GPU falla, el detector cae a CPU.

---

## 🔍 Qué hay en cada subcarpeta

| Pieza | Detalle clave |
|---|---|
| `detectorDeManos.js` | Instancia **única** y perezosa; prueba `GPU` y cae a `CPU`; olvida la promesa si falla, para poder reintentar |
| `frameDesdeDeteccion.js` | Redondea a 6 decimales e **ignora** manos sin handedness o con landmarks incompletos |
| `ladoDesdeCategoria.js` | `"Left"/"Right"` → lado del contrato, con el interruptor `INVERTIR_LADO` |
| `dibujarManos.js` | 21 conexiones, un color por lado y el **rótulo del lado** junto a la muñeca |
| `pintarManosSobreVideo.js` | Iguala la resolución del canvas a la del vídeo antes de pintar |
| `almacenamientoSeguro.js` | Todo acceso va en `try/catch`: recordar es una comodidad, no un requisito |
| `camara.js` | `getUserMedia` solo de vídeo (el audio pediría otro permiso sin aportar nada) |

---

## 💡 Ejemplos de uso

```js
import { obtenerDetectorDeManos } from './mediapipe/detectorDeManos.js'
import { frameDesdeResultado } from './mediapipe/frameDesdeDeteccion.js'
import { pintarManosSobreVideo } from './canvas/pintarManosSobreVideo.js'

const detector = await obtenerDetectorDeManos()
const frame = frameDesdeResultado(detector.detectForVideo(video, performance.now()), 0)
pintarManosSobreVideo(canvas, video, frame.manos)
```

```js
import { abrirCamara, cerrarCamara } from './navegador/camara.js'

const flujo = await abrirCamara()
video.srcObject = flujo
// …
cerrarCamara(flujo)   // apaga la luz de la cámara
```
