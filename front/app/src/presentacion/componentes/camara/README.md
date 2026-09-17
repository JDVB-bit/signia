# 🎥 `componentes/camara/` — El recuadro de vídeo en vivo

## 📖 Introducción

El componente que pide la cámara y muestra el vídeo, con todos sus estados
intermedios resueltos: aún no se ha pedido, se está pidiendo, se denegó o el
navegador no la soporta.

Lo usan **las dos páginas con cámara**: Entrenamiento (con overlay) y Traducción.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Responsabilidad |
|---|---|
| `CameraFeed.jsx` | 📹 El recuadro: `<video>`, capa superpuesta, borde de resaltado y aviso de estado |
| `AvisoEstadoCamara.jsx` | 💬 Lo que ocupa el recuadro mientras no hay vídeo: mensaje + botón de activar |

---

## 🎯 Qué problema resuelve

1. **Repetir el permiso en cada página.** La lógica de cámara es idéntica en
   Traducción y Entrenamiento; duplicarla garantizaría que una de las dos se
   quedara desactualizada.
2. **Estados que confunden.** "No se ve nada" puede ser tres cosas distintas
   (denegado, no soportado, aún sin pedir) y cada una necesita otra respuesta.
3. **Pintar encima del vídeo.** Entrenamiento necesita superponer el esqueleto y
   unos indicadores, **sin** que el componente de cámara sepa qué son.

---

## 🔗 Qué dependencias tiene

- `react` (`useRef`, `useEffect`).
- [`../../hooks/useCamara`](../../hooks/) — permiso, flujo y apagado.
- [`../../estados/estadosDeCamara`](../../estados/) — los cinco estados.
- Tailwind y la paleta del sitio.

No importa `getUserMedia` directamente: eso es cosa de
[`infra/navegador/camara.js`](../../../infra/navegador/).

---

## 🧠 Cómo soluciona el problema

### 🎛️ Un componente, cinco estados

```
inicial ──► solicitando ──► activa
   │              │
   └──────────────┴──► denegada  (vuelve a ofrecer el botón)
no-soportada (sin getUserMedia)
```

`AvisoEstadoCamara` mapea cada estado a su mensaje y decide si mostrar el botón:
solo en `inicial` y `denegada`, porque son los únicos desde los que reintentar
tiene sentido.

### 🎬 El `<video>` existe siempre

Se renderiza incluso cuando no hay flujo (oculto con `hidden`), para que la
`ref` esté lista en el momento en que se conceda el permiso. Si se montara
después, el flujo llegaría antes que el elemento.

### 🪟 La capa superpuesta no estorba

```jsx
{activa && children && <div className="pointer-events-none absolute inset-0">{children}</div>}
```

`pointer-events-none`: el overlay se ve pero no intercepta clics, así el `<video>`
sigue mandando. Y solo se monta con la cámara activa, para no dibujar sobre un
recuadro vacío.

### 🪞 Espejo por CSS

`-scale-x-100` voltea el vídeo para que el usuario se vea como en un espejo, que
es lo natural al hacer señas. El overlay del esqueleto se espeja **por su
cuenta**, invirtiendo la coordenada — así los rótulos siguen legibles.

---

## 🔍 Qué tienen los archivos

### `CameraFeed.jsx`

| Prop | Por defecto | Para qué |
|---|---|---|
| `className` | `''` | Tamaño desde fuera (las páginas usan `h-full w-full`) |
| `mirrored` | `true` | Espejar el vídeo |
| `videoRef` | `null` | Ref externa, para quien necesite leer los frames |
| `onEstado` | `null` | Se notifica cada cambio de estado |
| `resaltado` | `false` | Anillo `ring-4 ring-secondary` (se usa al grabar) |
| `children` | `null` | Capa superpuesta al vídeo |

Si no se pasa `videoRef`, usa una interna: así la página de Traducción lo usa sin
saber nada de refs.

### `AvisoEstadoCamara.jsx`

| Constante | Contenido |
|---|---|
| `MENSAJE_POR_ESTADO` | Un texto para `no-soportada`, `denegada` y `solicitando` |
| `ESTADOS_CON_BOTON` | `Set` con `inicial` y `denegada` |

| Prop | Para qué |
|---|---|
| `estado` | Cuál de los cinco estados pintar |
| `alActivar` | Qué hacer al pulsar *Activar cámara* |

---

## 💡 Ejemplos de uso

```jsx
// Traducción: lo mínimo
<CameraFeed className="h-full w-full" />
```

```jsx
// Entrenamiento: con overlay, ref externa y aviso de estado
<CameraFeed
    className="h-full w-full"
    videoRef={videoRef}
    onEstado={(estado) => setCamaraActiva(estado === ESTADOS_CAMARA.ACTIVA)}
    resaltado={captura.grabando}
>
    <canvas ref={canvasRef} className="h-full w-full object-cover" />
    <div className="absolute inset-x-0 top-0 flex justify-between p-3">
        <IndicadorDeManos cantidad={captura.manosDetectadas} />
        {captura.grabando && <IndicadorDeGrabacion segundos={captura.segundos} />}
    </div>
</CameraFeed>
```

> 🔐 `getUserMedia` solo funciona en **origen seguro**: `https://` o `localhost`.
> Al abrir la app por la IP de la red local sin TLS, el navegador bloquea el
> permiso y el componente mostrará el estado `denegada`.
