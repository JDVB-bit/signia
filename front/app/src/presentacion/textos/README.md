# 💬 `presentacion/textos/` — Lo que lee el usuario

## 📖 Introducción

Los mensajes de la captura, separados del código que decide **cuándo** se
muestran. El dominio devuelve motivos (`'sin-manos'`); aquí se convierten en
frases en español que una persona entiende.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Contenido |
|---|---|
| `textosDeCaptura.js` | 📋 `TEXTO_POR_MOTIVO_DE_DESCARTE` y `AVISOS_DE_CAPTURA` |
| `mensajeDeEstadoDeCaptura.js` | 🎚️ La función que decide **qué** frase ocupa la única línea de estado |
| `textosDeEnvio.js` | 📤 Cómo se cuenta cada desenlace del envío (subido, respaldado, sin muestras) |
| [`__tests__/`](__tests__/) | 🧪 Test de esa prioridad |

---

## 🎯 Qué problema resuelve

1. **Que el dominio no hable en español de interfaz.** `motivoDeDescarte()`
   devuelve un símbolo estable; si el mensaje se escribiera dentro de la regla,
   cambiar una coma obligaría a tocar el dominio (y sus tests).
2. **Que la línea de estado no parpadee.** En Entrenamiento hay *un solo* renglón
   para todo: avisos, carga del detector, errores y el id de sesión. Sin una
   regla de prioridad, dos mensajes se pisarían.
3. **Que los mensajes sean revisables.** Están todos juntos: se leen de una
   pasada y se corrigen sin bucear por los componentes.

---

## 🔗 Qué dependencias tiene

- [`../../dominio/reglasDeGrabacion.js`](../../dominio/reglasDeGrabacion.js) —
  las claves de `MOTIVOS_DE_DESCARTE`.
- [`../estados/estadosDelDetector.js`](../estados/estadosDelDetector.js) — para
  distinguir *cargando* de *error*.

Sin React: son datos y una función pura, y por eso se pueden testear.

---

## 🧠 Cómo soluciona el problema

### 🗺️ Traducción por tabla

```
dominio: 'sin-manos'  ──►  textos: 'No se vio ninguna mano: la muestra se descartó.'
```

El mapa se indexa con las constantes del dominio, no con strings copiados: si un
motivo cambia de nombre, el mapa deja de encontrarlo en desarrollo, no en
producción.

### 🎚️ Prioridad explícita

`mensajeDeEstadoDeCaptura` resuelve la única línea de estado en este orden:

```
1. aviso puntual            → "La grabación fue demasiado corta…"
2. cámara apagada           → "Activa la cámara para empezar a grabar."
3. detector cargando        → "Cargando el detector de manos..."
4. detector con error       → "No se pudo cargar el detector de manos."
5. todo listo               → "Sesión 2026-09-20-local"
```

Lo urgente y puntual gana; lo permanente (la sesión) queda de fondo.

---

## 🔍 Qué tienen los archivos

### `textosDeCaptura.js`

| Export | Contenido |
|---|---|
| `TEXTO_POR_MOTIVO_DE_DESCARTE` | `demasiado-corta` → *"La grabación fue demasiado corta: no se guardó nada."*<br>`sin-manos` → *"No se vio ninguna mano: la muestra se descartó."* |
| `AVISOS_DE_CAPTURA.FALTA_ETIQUETA` | *"Escribe el nombre de la seña antes de grabar."* |
| `AVISOS_DE_CAPTURA.PESTANA_OCULTA` | *"La grabación se descartó al salir de la pestaña."* |
| `textoDeEnvio({resultado, cuantas, motivo})` | *"Se enviaron 4 muestras al servidor."* / *"El servidor no respondio (...). Se descargaron 4 muestras como respaldo."* |
| `ENVIANDO` | Texto del botón mientras la petición está en marcha |

Todos los mensajes explican **qué pasó y qué consecuencia tuvo**, no solo que
algo falló.

### `mensajeDeEstadoDeCaptura.js`

```js
mensajeDeEstadoDeCaptura({ aviso, camaraActiva, estadoDetector, sesion })  // → string
```

---

## 💡 Ejemplos de uso

```jsx
<p className="min-h-[1.5rem] text-center text-sm text-brand" aria-live="polite">
    {mensajeDeEstadoDeCaptura({
        aviso: captura.aviso,
        camaraActiva,
        estadoDetector: captura.estado,
        sesion: captura.sesion,
    })}
</p>
```

```js
// En el hook de grabación: del motivo del dominio al texto del usuario
alAvisarRef.current(TEXTO_POR_MOTIVO_DE_DESCARTE[motivo])
```

> ♿ La línea lleva `aria-live="polite"` y una altura mínima fija: se anuncia a
> lectores de pantalla y el cambio de texto no mueve los botones de sitio.
