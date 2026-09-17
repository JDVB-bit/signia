# 🪝 `presentacion/hooks/` — Estado y efectos de React

## 📖 Introducción

Los hooks son **el pegamento**: conectan los adaptadores de `infra/` y las
reglas del `dominio/` con el ciclo de vida de React. Aquí vive todo lo que
tiene que ver con *cuándo* pasan las cosas (montar, desmontar, cada frame),
nunca *qué* significan.

Cada hook tiene una sola responsabilidad, y `useCapturaSenas` los compone.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Responsabilidad |
|---|---|
| `useCapturaSenas.js` | 📸 **Compone** detector, bucle, grabación y lote; es la API que usa la página |
| `useDetectorDeManos.js` | 🖐️ Carga el detector cuando hace falta y expone su estado |
| `useBucleDeDeteccion.js` | 🔁 Bucle `requestAnimationFrame` que pasa cada frame nuevo por el detector |
| `useGrabacionDeMuestra.js` | 🎬 Máquina de estados de **una** grabación: iniciar, acumular, cerrar, abortar |
| `useMuestrasCapturadas.js` | 🗃️ Lote acumulado en memoria: agregar, borrar la última, limpiar |
| `useCamara.js` | 📷 Ciclo de vida de la cámara: permiso, flujo, apagado |
| `useTema.js` | 🌗 Tema claro/oscuro sincronizado con documento y preferencia |
| `useIntroInicial.js` | 🎞️ Si toca mostrar la pantalla de carga |
| `useCerrarConEscape.js` | ⎋ Cerrar un panel abierto al pulsar `Escape` |

---

## 🎯 Qué problema resuelve

1. **El bucle de vídeo es hostil a React.** Corre a 30-60 Hz; si cada frame
   reiniciara efectos o recreara callbacks, la app se arrastraría.
2. **Los recursos hay que soltarlos.** Cámara encendida, `rAF` en marcha o un
   detector a medio cargar tras desmontar la página son fugas reales.
3. **Las respuestas tardías.** Activar la cámara dos veces seguidas, o salir
   mientras carga el detector, produce respuestas que llegan cuando ya no
   importan y pisarían el estado actual.
4. **Un hook gigante no se entiende.** Separar "cargar detector", "recorrer
   frames" y "grabar una muestra" permite leer cada pieza sola.

---

## 🔗 Qué dependencias tiene

| Dependencia | Para qué |
|---|---|
| `react` | `useState`, `useEffect`, `useRef`, `useCallback` |
| `../../infra/` | Cámara, detector, canvas, descarga, almacenamiento |
| `../../aplicacion/` | `crearMuestra`, `fpsDe`, `paqueteDeMuestras`, `idSesion` |
| `../../dominio/` | Reglas de grabación y normalización de etiqueta |
| `../estados/` y `../textos/` | Estados comparables y avisos |

---

## 🧠 Cómo soluciona el problema

### 🧩 Composición, no un hook monolítico

```
useCapturaSenas
 ├── useDetectorDeManos ......... ¿hay detector? ¿en qué estado?
 ├── useBucleDeDeteccion ........ un callback por frame nuevo
 ├── useGrabacionDeMuestra ...... buffer, cronómetro, cierre y descarte
 └── useMuestrasCapturadas ...... el lote en memoria
```

La página recibe **una sola API estable** y no se entera de la fontanería.

### 📌 Refs para lo que lee el bucle

El callback de detección y la etiqueta se guardan en `useRef`: cambiar la
etiqueta mientras se graba **no** reinicia el `requestAnimationFrame`, y el bucle
nunca lee un valor viejo.

### 🎫 Generaciones para descartar respuestas tardías

`useCamara` lleva un contador que cambia en cada montaje/desmontaje. Si llega un
flujo de una "generación" anterior, se cierra en vez de conectarse. `useDetectorDeManos`
hace lo equivalente con una bandera `cancelado`.

### ⏭️ Solo frames nuevos

`requestAnimationFrame` corre a ~60 Hz y la cámara entrega ~30: el bucle compara
`video.currentTime` con el anterior y **salta** si el vídeo no avanzó. Así no se
procesa dos veces el mismo frame.

---

## 🔍 Qué tienen los archivos

### `useCapturaSenas({ videoRef, canvasRef, etiqueta, activo })`

| Devuelve | Qué es |
|---|---|
| `estado` | Estado del detector (`inactivo`, `cargando`, `listo`, `error`) |
| `grabando`, `segundos` | Si hay grabación en curso y cuánto lleva |
| `muestras`, `sesion` | Lote en memoria e id de la tanda |
| `manosDetectadas`, `aviso` | Realimentación para el usuario |
| `alternarGrabacion`, `borrarUltima`, `limpiar`, `exportar` | Acciones |

Si la cámara se apaga a mitad de una grabación, **aborta**: esa grabación ya no
es válida.

### `useGrabacionDeMuestra({ etiqueta, sesion, alGuardar, alAvisar })`

| Acción | Qué hace |
|---|---|
| `alternar()` | Inicia o cierra; exige etiqueta antes de empezar |
| `registrarFrame(frame)` | Acumula, actualiza el cronómetro y cierra al llegar al tope |
| `abortar(aviso)` | Descarta la grabación en curso |

🙈 **Con la pestaña oculta el navegador congela `rAF`**: al volver, el contador
ya habría pasado el tope y cerraría una muestra con cuatro frames sueltos.
Además, una seña que nadie estaba mirando no es buen dato. Se descarta.

### `useDetectorDeManos(activo)`

Mientras `activo` sea `false` no descarga nada (el modelo pesa varios MB).
Devuelve `{ estado, detector }`.

### `useBucleDeDeteccion({ videoRef, detector, alDetectar })`

Arranca al haber detector y cancela el `rAF` al desmontar.

### `useCamara(videoRef)`

Devuelve `{ estado, activar }`. Se activa sola si el permiso ya se concedió en
esta visita; al desmontar **siempre** apaga el flujo.

### `useTema()` · `useIntroInicial()` · `useCerrarConEscape(abierto, cerrar)`

Tres hooks pequeños: alternar tema y persistirlo, decidir si se muestra la intro
y cerrar paneles con `Escape`.

---

## 💡 Ejemplos de uso

```jsx
const captura = useCapturaSenas({ videoRef, canvasRef, etiqueta: nombreSena, activo: camaraActiva })

<Button onClick={captura.alternarGrabacion} disabled={captura.estado !== ESTADOS_DETECTOR.LISTO}>
    {captura.grabando ? 'Detener' : 'Entrenar'}
</Button>
<Button onClick={() => captura.exportar()} disabled={captura.muestras.length === 0}>
    Enviar
</Button>
```

```jsx
const { estado, activar } = useCamara(videoRef)
const { oscuro, alternarTema } = useTema()
useCerrarConEscape(abierto, cerrar)
```

> 🧪 `exportar` acepta una función de descarga como parámetro
> (`exportar(miDescarga)`), para poder verificarlo sin tocar el disco.
