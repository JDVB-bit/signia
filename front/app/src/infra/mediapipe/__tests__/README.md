# 🧪 `infra/mediapipe/__tests__/` — Tests del adaptador de MediaPipe

## 📖 Introducción

Verifican la **traducción** entre lo que devuelve MediaPipe y el frame del
contrato. Usan resultados falsos con la forma exacta de `detectForVideo`, así
que **no necesitan cámara, ni WASM, ni GPU**.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Módulo que verifica | Casos cubiertos |
|---|---|---|
| `ladoDesdeCategoria.test.js` | `ladoDesdeCategoria.js` | Traducción `Left`/`Right`, inversión por espejo, categoría desconocida |
| `frameDesdeDeteccion.test.js` | `frameDesdeDeteccion.js` | 0/1/2 manos, resultado nulo, `handednesses` en plural, landmarks incompletos, redondeo, `z` ausente |

`detectorDeManos.js` no se testea aquí: su trabajo es instanciar una librería
externa con WASM: se verifica en el navegador, no con un doble.

---

## 🎯 Qué problema resuelve

El adaptador es el sitio donde **entran datos ajenos** al sistema. Si acepta
basura, esa basura acaba en el dataset y de ahí en el modelo. Estos tests fijan
la política:

- Lo que no se entiende **se descarta**, no se rellena con valores inventados.
- Lo que falta (`z`, `score`) tiene un valor por defecto explícito.
- Lo que cambia entre versiones de la librería (`handedness` vs
  `handednesses`) se tolera.

---

## 🔗 Qué dependencias tiene

- `vitest` en entorno node.
- Los módulos de [`../`](../). **No** se importa `@mediapipe/tasks-vision`: los
  resultados se fabrican a mano.

---

## 🧠 Cómo soluciona el problema

Cada test construye un resultado sintético con la forma que documenta MediaPipe:

```js
const resultado = (manos) => ({
    landmarks: manos.map((m) => m.puntos ?? puntos()),
    handedness: manos.map((m) => [{ categoryName: m.categoria, score: m.score ?? 0.9 }]),
})
```

Eso permite probar lo que en la vida real solo ocurre de vez en cuando (una
mano a medias, un handedness ausente) de forma determinista y en milisegundos.

---

## 🔍 Qué tienen los archivos

| Test | Lo que garantiza |
|---|---|
| `sin manos produce un frame vacio, no un hueco` | La ausencia se representa, no se omite |
| `tolera un resultado nulo` | Un fallo puntual del detector no rompe el bucle |
| `conserva las dos manos` | Las señas a dos manos no se recortan |
| `acepta el campo handednesses en plural` | Cambiar de versión de la librería no rompe la captura |
| `descarta una mano con un numero de landmarks que no es el del contrato` | Nunca entra una mano de 5 puntos al dataset |
| `descarta una mano sin handedness en vez de inventarle un lado` | Un lado inventado corrompería la ranura del tensor |
| `redondea las coordenadas a los decimales del contrato` | El JSON pesa la mitad sin perder precisión útil |
| `puede invertirse si el espejo del video engañara al detector` | El interruptor `INVERTIR_LADO` funciona de verdad |

---

## 💡 Ejemplos de uso

```bash
pnpm test -- mediapipe
```

```js
// Un resultado falso mínimo para probar el adaptador
const crudo = {
    landmarks: [Array.from({ length: 21 }, () => ({ x: 0.1, y: 0.2, z: 0 }))],
    handedness: [[{ categoryName: 'Right', score: 0.98 }]],
}

frameDesdeResultado(crudo, 0)
// → { t: 0, manos: [{ lado: 'derecha', score: 0.98, lm: [[0.1, 0.2, 0], …] }] }
```
