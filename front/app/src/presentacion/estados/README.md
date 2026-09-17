# 🚥 `presentacion/estados/` — Estados compartidos de la interfaz

## 📖 Introducción

Los dos conjuntos de estados que la interfaz necesita comparar en varios sitios
a la vez: en qué situación está **la cámara** y en qué situación está **el
detector de manos**.

Son constantes congeladas, no lógica. Existen para que nadie escriba `'activa'`
a mano en tres archivos distintos.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Contenido |
|---|---|
| `estadosDeCamara.js` | 📷 `ESTADOS_CAMARA`: `INICIAL`, `SOLICITANDO`, `ACTIVA`, `DENEGADA`, `NO_SOPORTADA` |
| `estadosDelDetector.js` | 🖐️ `ESTADOS_DETECTOR`: `INACTIVO`, `CARGANDO`, `LISTO`, `ERROR` |

---

## 🎯 Qué problema resuelve

El mismo estado se consulta desde tres capas distintas:

```
useCamara ──► CameraFeed ──► Entrenamiento
  (lo produce)  (lo pinta)     (lo traduce a camaraActiva)
```

Con strings literales, un `'no soportada'` con espacio en vez de guion no falla:
simplemente **no coincide nunca**, y la interfaz se queda muda sin error. Un
símbolo compartido convierte ese error silencioso en algo imposible.

---

## 🔗 Qué dependencias tiene

**Ninguna.** Son objetos planos con `Object.freeze`.

---

## 🧠 Cómo soluciona el problema

Cada conjunto es la **lista cerrada** de situaciones posibles, y cada situación
tiene su respuesta en la interfaz:

| `ESTADOS_CAMARA` | Qué ve el usuario |
|---|---|
| `INICIAL` | Botón *Activar cámara* |
| `SOLICITANDO` | "Solicitando acceso a la cámara..." |
| `ACTIVA` | El vídeo en vivo (y el overlay, si lo hay) |
| `DENEGADA` | Explicación + botón para reintentar |
| `NO_SOPORTADA` | "Este navegador no permite acceder a la cámara." |

| `ESTADOS_DETECTOR` | Qué implica |
|---|---|
| `INACTIVO` | La cámara está apagada: no se descarga el modelo |
| `CARGANDO` | Descargando WASM + modelo; *Entrenar* deshabilitado |
| `LISTO` | Se puede grabar |
| `ERROR` | No se pudo cargar; se explica en la línea de estado |

`Object.freeze` impide que alguien "arregle" un estado mutando el objeto en
tiempo de ejecución.

---

## 🔍 Qué tienen los archivos

```js
export const ESTADOS_CAMARA = Object.freeze({
    INICIAL: 'inicial',
    SOLICITANDO: 'solicitando',
    ACTIVA: 'activa',
    DENEGADA: 'denegada',
    NO_SOPORTADA: 'no-soportada',
})
```

```js
export const ESTADOS_DETECTOR = Object.freeze({
    INACTIVO: 'inactivo',
    CARGANDO: 'cargando',
    LISTO: 'listo',
    ERROR: 'error',
})
```

Los valores son strings legibles a propósito: aparecen tal cual en las React
DevTools al depurar.

---

## 💡 Ejemplos de uso

```jsx
import { ESTADOS_CAMARA } from '../estados/estadosDeCamara'

const alCambiarEstadoCamara = useCallback(
    (estado) => setCamaraActiva(estado === ESTADOS_CAMARA.ACTIVA),
    [],
)
```

```jsx
import { ESTADOS_DETECTOR } from '../estados/estadosDelDetector'

const detectorListo = captura.estado === ESTADOS_DETECTOR.LISTO
<Button disabled={!detectorListo}>Entrenar</Button>
```

```jsx
// Mapear estado → contenido, sin cadenas de if
const MENSAJE_POR_ESTADO = {
    [ESTADOS_CAMARA.DENEGADA]: 'Se denegó el acceso a la cámara…',
    [ESTADOS_CAMARA.SOLICITANDO]: 'Solicitando acceso a la cámara...',
}
```
