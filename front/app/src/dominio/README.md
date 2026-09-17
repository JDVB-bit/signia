# 🎯 `dominio/` — Reglas del negocio (JavaScript puro)

## 📖 Introducción

La capa más interna del front. Aquí vive **lo que es verdad sobre las señas**
independientemente de la tecnología: qué forma tiene el dato, qué mano gana si
MediaPipe se equivoca y cuándo una grabación no sirve.

**No importa React, ni el DOM, ni MediaPipe.** Es gemela de
`model/signia_modelo/dominio/` en Python: las dos escriben las mismas reglas en
lenguajes distintos.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Responsabilidad |
|---|---|
| `contrato.js` | 📜 Constantes del contrato de datos: `SCHEMA`, `T = 48`, 21 landmarks, 2 manos, lados canónicos |
| `manoDelFrame.js` | ✋ Regla única para elegir la mano de un lado cuando hay dos candidatas |
| `etiquetaDeSena.js` | 🏷️ Normaliza el nombre de una seña (`" Hola "` → `"hola"`) |
| `reglasDeGrabacion.js` | 🎬 Cuándo se cierra una grabación y por qué se descarta |
| `unidadesDeTiempo.js` | ⏲️ `MS_POR_SEGUNDO`, la conversión compartida por todo el front |
| [`__tests__/`](__tests__/) | 🧪 Tests de las reglas (sin navegador) |

---

## 🎯 Qué problema resuelve

1. **Que las reglas no se dispersen.** "Dos manos del mismo lado: gana la de
   mayor score" está escrita en un sitio, no repetida en el hook, en el overlay
   y en el exportador.
2. **Que el dataset no se ensucie.** Una grabación de tres frames o sin manos se
   rechaza en el momento; descubrirlo después de grabar cientos de muestras
   sale carísimo.
3. **Que el contrato sea comprobable.** Las constantes viven aisladas, así el
   test de conformidad puede vigilar que coincidan con las de Python.

---

## 🔗 Qué dependencias tiene

**Ninguna.** Ni paquetes de npm, ni React, ni APIs del navegador. Solo
JavaScript, y por eso sus tests corren en node en milisegundos.

Su contraparte obligatoria es `model/signia_modelo/dominio/contrato.py`: si un
valor cambia aquí, tiene que cambiar allí.

---

## 🧠 Cómo soluciona el problema

```
        dominio/  ← nadie de aquí mira hacia afuera
           ▲   ▲
aplicacion/    presentacion/  ·  infra/
```

Las capas exteriores importan del dominio; el dominio no importa de nadie. Un
cambio de librería (otro detector, otro almacenamiento) no puede alcanzarlo.

Las reglas se expresan como **datos + funciones puras**, no como condiciones
sueltas dentro de un componente: `motivoDeDescarte(frames)` devuelve un motivo
del catálogo `MOTIVOS_DE_DESCARTE`, y la presentación decide qué texto enseñar.
Así se puede cambiar el mensaje sin tocar la regla, y la regla sin tocar la
interfaz.

---

## 🔍 Qué tienen los archivos

### `contrato.js`

| Constante | Valor | Significado |
|---|---|---|
| `SCHEMA` | `1` | Versión del formato de transporte |
| `N_LANDMARKS` / `N_DIMS` / `N_MANOS` | `21` / `3` / `2` | Geometría de MediaPipe |
| `IDX_MUNECA` | `0` | Landmark de la muñeca (origen de forma y escala) |
| `T` | `48` | Frames de la ventana del modelo (~1,6 s a 30 fps) |
| `LADO_IZQUIERDA` / `LADO_DERECHA` | `'izquierda'` / `'derecha'` | Vocabulario del contrato |
| `LADOS` | `['izquierda', 'derecha']` | **Ranuras fijas** del tensor, nunca el orden de detección |
| `TIPO_AISLADA` | `'aislada'` | Única unidad de entrenamiento |
| `SCORE_MAXIMO` | `1` | Confianza que se asume si el detector no la reporta |

### `manoDelFrame.js`

`manoDelFrame(frame, lado)` → la mano de ese lado o `null`. Si MediaPipe reporta
dos con el mismo lado (falso positivo), gana la de **mayor score**; a igualdad,
la primera — por eso la comparación es estrictamente mayor.

### `etiquetaDeSena.js`

`normalizarEtiqueta(texto)` recorta y pasa a minúsculas, así `"Hola"`, `" hola "`
y `"HOLA"` son **la misma clase** para el modelo.

### `reglasDeGrabacion.js`

| Elemento | Valor / salida | Por qué |
|---|---|---|
| `DURACION_MAXIMA_MS` | `4000` | Holgado sobre la ventana del modelo, pero una pulsación olvidada no puede generar una muestra de dos minutos |
| `FRAMES_MINIMOS` | `5` | Por debajo no hay seña que valga |
| `MOTIVOS_DE_DESCARTE` | `'demasiado-corta'`, `'sin-manos'` | Catálogo congelado (`Object.freeze`) |
| `framesConMano(frames)` | número | Cuántos frames llevan al menos una mano |
| `debeCerrarPorTiempo(ms)` | booleano | Cierre automático por tope |
| `motivoDeDescarte(frames)` | motivo o `null` | La única definición de "muestra mala" |

### `unidadesDeTiempo.js`

`MS_POR_SEGUNDO = 1000`. Existe para que ningún archivo escriba `1000` suelto.

---

## 💡 Ejemplos de uso

```js
import { motivoDeDescarte, MOTIVOS_DE_DESCARTE } from './reglasDeGrabacion.js'

motivoDeDescarte([])                 // 'demasiado-corta'
motivoDeDescarte(framesSinManos)     // 'sin-manos'
motivoDeDescarte(framesBuenos)       // null → la muestra sirve
```

```js
import { manoDelFrame } from './manoDelFrame.js'

const floja = { lado: 'derecha', score: 0.4 }
const buena = { lado: 'derecha', score: 0.95 }
manoDelFrame({ manos: [floja, buena] }, 'derecha')   // → buena
manoDelFrame({ manos: [] }, 'derecha')               // → null
```

```js
import { LADOS, T } from './contrato.js'

LADOS.indexOf('derecha')   // 1 → la ranura derecha del tensor
T                          // 48 pasos temporales
```

> ⚠️ Si cambias un valor de `contrato.js`, cambia también
> `model/signia_modelo/dominio/contrato.py`. El test de conformidad lo detectará,
> pero el cambio obliga además a **reentrenar**.
