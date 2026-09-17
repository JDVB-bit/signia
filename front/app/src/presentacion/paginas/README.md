# 📄 `presentacion/paginas/` — Las tres vistas del sitio

## 📖 Introducción

Cada archivo es una **página con ruta propia**. Una página no contiene lógica de
dominio: monta el layout, mantiene el estado de la vista y conecta los
componentes con los hooks.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Ruta | Estado | Qué hace |
|---|---|---|---|
| `Inicio.jsx` | `/` | ✅ Completa | Presenta el producto: título animado, *¿Qué es?*, *Misión*, *Herramientas* y carrusel |
| `Entrenamiento.jsx` | `/entrenamiento` | ✅ Funcional | **Modo aislado**: graba una muestra por seña, lleva el contador y exporta el lote |
| `Traduccion.jsx` | `/traduccion` | 🟡 A la espera del modelo | **Modo continuo**: cámara + botón (deshabilitado) + explicación honesta |

---

## 🎯 Qué problema resuelve

Los **dos modos de uso** del producto, que existen por razones distintas y no
deben mezclarse:

| | Entrenamiento | Traducción |
|---|---|---|
| Para qué | Grabar dataset | Usar el producto |
| Unidad | Una seña por grabación | Una frase seguida |
| Quién lo usa | El equipo (Fase 2) | El usuario final |
| Etiqueta | La escribe la persona | La predice el modelo |

Reconocer una seña por pulsación sería un *diccionario inteligente*; el producto
es el **traductor**. Por eso el modo continuo es una página aparte, y no un
botón más dentro de Entrenamiento.

---

## 🔗 Qué dependencias tiene

| Dependencia | Para qué |
|---|---|
| `../componentes/layout/` | `PageLayout`, `TituloPagina`, `TituloAnimado` |
| `../componentes/camara/` | `CameraFeed` |
| `../componentes/captura/` | Contador e indicadores sobre el vídeo |
| `../componentes/contenido/` | `SectionCard`, `Typewriter`, `InfoBubble`, `ImageBelt` |
| `../hooks/useCapturaSenas` | Todo el ciclo de captura (solo Entrenamiento) |
| `../estados/` y `../textos/` | Estados comparables y mensajes |
| `../../assets/` | Imágenes del carrusel |

---

## 🧠 Cómo soluciona el problema

### 🎥 Entrenamiento: una pulsación, una muestra

```
CameraFeed ──► videoRef ──► useCapturaSenas ──► muestras[]
     ▲                            │
  canvasRef ◄── overlay ──────────┘
```

- `CameraFeed` informa de su estado; la página lo traduce a `camaraActiva`, y
  eso arranca o para el detector (el modelo pesa MB: no se descarga hasta que
  hace falta).
- **Dos bloques del mismo tamaño** (`h-[27rem]`): cámara a la izquierda; nombre
  de la seña, contador, estado y botones a la derecha.
- Sobre el vídeo: cuántas manos se ven y, mientras graba, un punto rojo con los
  segundos. El marco se resalta para que se note sin leer.
- Una **sola línea de estado** (`aria-live="polite"`) con altura mínima fija: el
  texto cambia sin mover el resto del bloque.

| Control | Qué hace | Cuándo se apaga |
|---|---|---|
| **Entrenar / Detener** | Abre y cierra la grabación (también se cierra sola a los 4 s) | Si el detector no está listo |
| **Enviar** | Descarga el lote como JSON (Fase 5: `POST /muestras`) | Si no hay muestras |
| **Borrar última muestra** | Deshace la última grabación | Si no hay muestras |

### 💬 Traducción: no fingir

No hay modelo entrenado todavía, así que la página **no simula traducir**: el
botón está deshabilitado y el panel explica por qué y qué se puede hacer
mientras tanto (grabar señas en Entrenamiento). Cuando exista el pipeline
(Fases 6 y 6b), *Traducir* pasará a ser un interruptor de sesión y la caja
mostrará las glosas.

### 🏠 Inicio: explicar sin tecnicismos

Texto que se escribe solo (`Typewriter`) para lo esencial y `InfoBubble` para el
detalle: quien tiene prisa lee tres frases; quien quiere más, abre la burbuja.

---

## 🔍 Qué tienen los archivos

### `Entrenamiento.jsx`

| Estado local | Para qué |
|---|---|
| `nombreSena` | Etiqueta que se está grabando |
| `camaraActiva` | Derivado de `CameraFeed`; activa o no el detector |
| `videoRef` / `canvasRef` | El `<video>` que lee el detector y el `<canvas>` del overlay |

Deriva `detectorListo` y `hayMuestras` para decidir qué botones se apagan, y
delega el mensaje de estado en `mensajeDeEstadoDeCaptura(...)`.

### `Inicio.jsx`

`TITULO` y `IMAGENES_CARRUSEL` son constantes del módulo; el texto alternativo
de las imágenes se define una vez y se reutiliza. El contenido visible (qué es,
misión, herramientas) es **contenido de producto**, no técnico.

### `Traduccion.jsx`

Misma rejilla que Entrenamiento para que el sitio se sienta uno solo. Sin estado
todavía: el panel es informativo y accesible (`aria-live="polite"`).

---

## 💡 Ejemplos de uso

Grabar cinco muestras de la seña *hola*:

1. Ir a `/entrenamiento` y pulsar **Activar cámara**.
2. Escribir `hola` en *Nombre de la seña*.
3. **Entrenar** → hacer la seña → **Detener**. El contador sube a 1.
4. Repetir cinco veces y pulsar **Enviar**.

Se descarga `signia-hola-2026-09-20-local.json`, que Python valida tal cual:

```bash
cd model
venv/Scripts/python -c "import json,sys; from signia_modelo.infra.json_contrato import muestra_desde_dict; \
paquete=json.load(open(sys.argv[1],encoding='utf-8')); \
print([muestra_desde_dict(m).n_frames for m in paquete['muestras']])" \
  ~/Downloads/signia-hola-2026-09-20-local.json
```
