# 🦴 `infra/canvas/` — Overlay del esqueleto de la mano

## 📖 Introducción

Dibuja sobre el vídeo lo que el detector está viendo: los huesos, las
articulaciones y **el lado** de cada mano. Es el adaptador del `<canvas>`, la
única parte del front que habla con un contexto 2D.

No es decoración: es la herramienta que permite **descartar una muestra mala
antes de guardarla**.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Responsabilidad |
|---|---|
| `dibujarManos.js` | 🎨 Pinta huesos, articulaciones y el rótulo del lado en un contexto 2D |
| `pintarManosSobreVideo.js` | 📐 Ajusta el canvas a la resolución del vídeo y delega en `dibujarManos` |
| [`__tests__/`](__tests__/) | 🧪 Tests con un contexto 2D falso |

---

## 🎯 Qué problema resuelve

1. **Grabar a ciegas.** Sin overlay no se sabe si MediaPipe perdió la mano a
   mitad de la seña; el fallo aparecería al entrenar, con el dataset ya grabado.
2. **Verificar el handedness.** El vídeo se pinta espejado, así que no basta con
   mirar: el rótulo junto a la muñeca convierte una duda del plan en una
   comprobación de diez segundos.
3. **Alinear dos sistemas de coordenadas.** Los landmarks llegan normalizados
   (`0..1`) y el canvas trabaja en píxeles, con el vídeo espejado por CSS.

---

## 🔗 Qué dependencias tiene

- `CanvasRenderingContext2D` del navegador.
- [`../../dominio/contrato.js`](../../dominio/contrato.js) — `N_LANDMARKS`,
  `IDX_MUNECA` y los lados.
- Nada más: ni React, ni MediaPipe.

---

## 🧠 Cómo soluciona el problema

### 🪞 Espejo coherente con el vídeo

```js
x = espejado ? 1 - landmark.x : landmark.x
punto = { x: x * ancho, y: landmark.y * alto }
```

Se invierte **la coordenada**, no el canvas entero. Si se volteara el canvas con
una transformación, los rótulos saldrían escritos al revés.

### 📐 Misma resolución que el vídeo

`pintarManosSobreVideo` iguala `canvas.width/height` a `video.videoWidth/Height`
antes de pintar. Si no coincidieran, el esqueleto aparecería desplazado respecto
a la mano real.

### 🎨 Un color por lado

| Lado | Color |
|---|---|
| Izquierda | 🟠 `#E68825` |
| Derecha | 🔵 `#4FA3D1` |

Los huesos van en blanco translúcido y los puntos en el color del lado: de un
vistazo se ve si el detector confundió las manos.

---

## 🔍 Qué tienen los archivos

### `dibujarManos.js`

| Elemento | Detalle |
|---|---|
| `CONEXIONES` | 21 pares de landmarks: los cinco dedos, la palma y su base |
| `COLOR_POR_LADO` | Color por lado del contrato |
| `puntoEnCanvas(landmark, opciones)` | Landmark normalizado → píxel, con espejado opcional |
| `dibujarHuesos` / `dibujarArticulaciones` / `rotularLado` | Funciones privadas, una por elemento del dibujo |
| `dibujarManos(contexto, manos, opciones)` | Limpia el canvas y repinta el frame entero |

Constantes de estilo: grosor `3 px`, radio del punto `4 px`, separación del
rótulo `8 px`. Una mano cuyo número de landmarks no sea 21 **se salta**: reventar
aquí pararía el bucle de vídeo.

### `pintarManosSobreVideo.js`

`pintarManosSobreVideo(canvas, video, manos, { espejado })` — no hace nada si
todavía no existen el canvas o el vídeo (durante el montaje es normal).

---

## 💡 Ejemplos de uso

```js
import { pintarManosSobreVideo } from './pintarManosSobreVideo.js'

// Dentro del callback de detección
pintarManosSobreVideo(canvasRef.current, videoRef.current, frame.manos)
```

```js
import { dibujarManos, puntoEnCanvas } from './dibujarManos.js'

puntoEnCanvas({ x: 0.25, y: 0.5 }, { ancho: 640, alto: 480, espejado: false })
// → { x: 160, y: 240 }
puntoEnCanvas({ x: 0.25, y: 0.5 }, { ancho: 640, alto: 480 })
// → { x: 480, y: 240 }   (espejado, como el vídeo)
```

En la página, el canvas se superpone al vídeo dentro de `CameraFeed`:

```jsx
<CameraFeed videoRef={videoRef}>
    <canvas ref={canvasRef} className="h-full w-full object-cover" />
</CameraFeed>
```
