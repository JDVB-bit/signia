# 🌐 `infra/navegador/` — Adaptadores de las APIs del navegador

## 📖 Introducción

Todo lo que depende del navegador y **puede fallar**: la cámara, el
almacenamiento, las descargas, la preferencia de tema. Cada API cruda queda
envuelta en una función con el vocabulario del proyecto.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Responsabilidad |
|---|---|
| `almacenamientoSeguro.js` | 🔐 Leer y guardar en `localStorage` / `sessionStorage` **sin lanzar nunca** |
| `camara.js` | 🎥 `getUserMedia`: comprobar soporte, abrir y cerrar el flujo de vídeo |
| `permisoDeCamara.js` | 📷 Recordar, solo durante la visita, si se concedió la cámara |
| `preferenciaDeTema.js` | 🌗 Tema claro/oscuro: preferencia guardada, la del sistema y la clase `.dark` |
| `registroDeIntro.js` | 🎞️ Recordar si ya se vio la pantalla de carga |
| `descargarJson.js` | ⬇️ Descargar un objeto como fichero `.json` |
| [`__tests__/`](__tests__/) | 🧪 Tests del almacenamiento en sus tres escenarios |

---

## 🎯 Qué problema resuelve

1. **`localStorage` puede explotar.** En modo privado, con cookies bloqueadas o
   dentro de ciertos iframes, **solo tocar** `window.localStorage` lanza. Sin
   protección, la app entera se caería al arrancar.
2. **La cámara puede no existir** (navegador sin soporte, origen inseguro) o ser
   denegada, y hay que distinguir ambos casos para explicárselo al usuario.
3. **La luz de la cámara.** Si no se detienen las pistas al salir, el indicador
   del dispositivo se queda encendido: un problema de confianza, no técnico.
4. **El parpadeo de tema.** Si el tema se aplicara después de renderizar, la
   primera pantalla saldría con los colores contrarios.

---

## 🔗 Qué dependencias tiene

| API del navegador | Dónde |
|---|---|
| `navigator.mediaDevices.getUserMedia` | `camara.js` |
| `localStorage` / `sessionStorage` | `almacenamientoSeguro.js` |
| `window.matchMedia` | `preferenciaDeTema.js` |
| `document.documentElement.classList` | `preferenciaDeTema.js` |
| `URL.createObjectURL` + `Blob` | `descargarJson.js` |

Ninguna dependencia de npm, ni de React, ni del dominio.

---

## 🧠 Cómo soluciona el problema

### 🔐 Degradar, no romper

```
leerLocal(clave) ──► try { window.localStorage.getItem } catch ──► null
guardarLocal(…)  ──► try { …setItem } catch ──► se ignora
```

Recordar preferencias es **una comodidad**: si el navegador no deja, la app
sigue funcionando sin recordar nada. Todo acceso (incluido el simple hecho de
leer `window[nombre]`) va dentro de `try/catch`.

### 📷 `sessionStorage` para el permiso, `localStorage` para el resto

| Dato | Almacén | Por qué |
|---|---|---|
| Permiso de cámara | `sessionStorage` | Se olvida al cerrar la pestaña: en una visita nueva se vuelve a pedir explícitamente |
| Tema | `localStorage` | Es una preferencia estética: debe durar entre visitas |
| Intro vista | `localStorage` | La animación solo debe verse la primera vez |

El permiso real **siempre lo controla el navegador**; esto solo evita volver a
mostrar el botón al cambiar de página dentro de la misma visita.

---

## 🔍 Qué tienen los archivos

### `almacenamientoSeguro.js`

| Función | Efecto |
|---|---|
| `leerLocal(clave)` / `guardarLocal(clave, valor)` | Persisten entre visitas |
| `leerDeSesion(clave)` / `guardarEnSesion(clave, valor)` | Se olvidan al cerrar la pestaña |

### `camara.js`

| Función | Efecto |
|---|---|
| `camaraSoportada()` | ¿Existe `getUserMedia` en este navegador? |
| `abrirCamara()` | Pide `{ video: true, audio: false }` — el audio pediría otro permiso sin aportar nada |
| `cerrarCamara(flujo)` | Detiene todas las pistas: la luz se apaga |

### `permisoDeCamara.js`

`permisoConcedidoEnEstaVisita()` y `recordarPermisoDeCamara(concedido)`, sobre la
clave `signia-camera-permiso`.

### `preferenciaDeTema.js`

| Función | Efecto |
|---|---|
| `temaOscuroPreferido()` | Preferencia guardada; si no hay, la del sistema |
| `guardarTemaOscuro(oscuro)` | Persiste la elección (clave histórica `signia-theme`) |
| `aplicarTemaOscuro(oscuro)` | Añade o quita la clase `dark` en `<html>` |
| `aplicarTemaInicial()` | Se llama en `main.jsx` **antes** de montar React |

### `registroDeIntro.js`

`introYaVista()` y `marcarIntroVista()`, sobre `signia-intro-vista`.

### `descargarJson.js`

`descargarJson(nombre, contenido)` crea un `Blob`, pulsa un enlace temporal y
libera la URL (`revokeObjectURL`) en cuanto arranca la descarga.

---

## 💡 Ejemplos de uso

```js
import { abrirCamara, camaraSoportada, cerrarCamara } from './camara.js'

if (!camaraSoportada()) mostrarAviso('Este navegador no permite acceder a la cámara.')
const flujo = await abrirCamara()
video.srcObject = flujo
// al desmontar:
cerrarCamara(flujo)
```

```js
import { descargarJson } from './descargarJson.js'

descargarJson('signia-hola-2026-09-20-local.json', { schema: 1, muestras })
```

```js
import { aplicarTemaInicial } from './preferenciaDeTema.js'

aplicarTemaInicial()   // en main.jsx, antes de createRoot
```
