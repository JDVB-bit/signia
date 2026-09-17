# 🧩 `presentacion/componentes/` — Piezas visuales reutilizables

## 📖 Introducción

Los componentes de React del sitio, **agrupados por tema** en vez de por tipo.
Ninguno conoce el dominio: reciben props y pintan. Eso los hace intercambiables
y fáciles de leer.

---

## 📂 Qué carpetas tiene y qué hace cada una

| Carpeta | Para qué | Componentes |
|---|---|---|
| [`layout/`](layout/) | 🏗️ Esqueleto común de toda página | `PageLayout`, `Header`, `TituloPagina`, `TituloAnimado` |
| [`camara/`](camara/) | 🎥 El recuadro de vídeo y sus avisos | `CameraFeed`, `AvisoEstadoCamara` |
| [`captura/`](captura/) | 📸 Indicadores de la grabación | `ContadorDeMuestras`, `IndicadorDeGrabacion`, `IndicadorDeManos` |
| [`contenido/`](contenido/) | 📰 Bloques de la página de Inicio | `SectionCard`, `Typewriter`, `InfoBubble`, `ImageBelt`, `CarouselImage` |
| [`navegacion/`](navegacion/) | 🧭 Moverse por el sitio | `BurgerMenu` |
| [`tema/`](tema/) | 🌗 Cambiar la paleta | `ThemeToggle` |
| [`comunes/`](comunes/) | 🔘 Lo que usan todas las páginas | `Button` |
| [`intro/`](intro/) | 🎬 Pantalla de carga inicial | `IntroSplash` + su CSS |

---

## 🎯 Qué problema resuelve

1. **Coherencia.** El sitio se ve igual en las tres páginas porque el layout, la
   cabecera y los botones **son los mismos objetos**, no copias parecidas.
2. **Encontrar las cosas.** Agrupar por tema (`camara/`, `captura/`) dice de qué
   va cada pieza; una carpeta plana con quince componentes, no.
3. **Accesibilidad de serie.** Los controles llevan `aria-*`, foco gestionado y
   cierre con `Escape` desde el primer día, no como parche posterior.

---

## 🔗 Qué dependencias tiene

| Dependencia | Para qué |
|---|---|
| `react` | Componentes y hooks |
| `react-router-dom` | `Link` en `BurgerMenu` |
| Tailwind v4 | Clases de estilo y la paleta de `index.css` |
| [`../hooks/`](../hooks/) | `useCamara`, `useTema`, `useCerrarConEscape` |
| [`../estados/`](../estados/) | Comparar estados de cámara |
| [`../rutas.js`](../rutas.js) | Enlaces del menú |

---

## 🧠 Cómo soluciona el problema

### 🧱 Componentes tontos, hooks listos

El estado y los efectos viven en `hooks/`; el componente solo dice **cómo se
ve**. `CameraFeed` no pide la cámara: la pide `useCamara`, y el componente pinta
lo que ese hook informa.

### 🪆 Composición antes que props booleanas

`CameraFeed` acepta `children` como capa superpuesta, así Entrenamiento le pone
su `<canvas>` sin que el componente sepa qué es un esqueleto de mano. Del mismo
modo, `PageLayout` recibe el contenido entero como `children`.

### 🎨 Solo la paleta de cinco colores

Ningún componente inventa colores: usan `bg-surface`, `text-brand`,
`bg-secondary`, `text-brand-inverso`, `bg-bg`. Cambiar la paleta en
`src/index.css` repinta el sitio entero.

---

## 🔍 Qué hay en cada grupo

| Componente | Detalle destacable |
|---|---|
| `PageLayout` | Fondo + `Header` + `<main>` con el ancho estándar (`max-w-[110rem]`) |
| `TituloPagina` / `TituloAnimado` | Comparten `ESTILOS_TITULO_PAGINA`: mismo tamaño en todas las páginas |
| `CameraFeed` | `videoRef` externa, `children` como overlay, `resaltado` para grabación |
| `AvisoEstadoCamara` | Un mensaje por estado y el botón solo donde tiene sentido |
| `IndicadorDeManos` / `IndicadorDeGrabacion` | Realimentación en vivo sobre el vídeo |
| `ContadorDeMuestras` | El número grande: lo que confirma que la muestra se guardó |
| `InfoBubble` | Diálogo accesible: `role="dialog"`, `aria-modal`, cierre triple |
| `ImageBelt` + `CarouselImage` | Carrusel sin salto al volver al inicio |
| `BurgerMenu` | Icono animado a ✕, foco al primer enlace, cierre con `Escape` |
| `ThemeToggle` | `aria-pressed` y el icono del tema **al que se pasa** |
| `Button` | Dos variantes, dos tamaños, siempre `type="button"` |

---

## 💡 Ejemplos de uso

```jsx
import PageLayout from './layout/PageLayout'
import TituloPagina from './layout/TituloPagina'
import Button from './comunes/Button'
import CameraFeed from './camara/CameraFeed'

<PageLayout>
    <TituloPagina>Entrenamiento</TituloPagina>

    <CameraFeed videoRef={videoRef} onEstado={alCambiarEstado} resaltado={grabando}>
        <canvas ref={canvasRef} className="h-full w-full object-cover" />
    </CameraFeed>

    <Button variant="primary" onClick={alternarGrabacion} disabled={!listo}>
        Entrenar
    </Button>
</PageLayout>
```

Para añadir un componente: elegir el grupo por **tema**, un archivo por
componente con el nombre de lo que hace, y sin lógica de dominio dentro.
