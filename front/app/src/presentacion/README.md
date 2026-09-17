# 🎨 `presentacion/` — Interfaz en React

## 📖 Introducción

La capa exterior: **todo lo que el usuario ve y toca**. Usa las demás capas
(`dominio`, `aplicacion`, `infra`) y ninguna la usa a ella, así que se puede
rehacer la interfaz entera sin tocar una sola regla del negocio.

---

## 📂 Qué archivos y carpetas tiene

| Elemento | Qué contiene |
|---|---|
| `AplicacionRaiz.jsx` | 🚦 La intro (primera visita) o las rutas del sitio |
| `rutas.js` | 🧭 Única fuente de URLs y de los enlaces del menú |
| [`paginas/`](paginas/) | 📄 Inicio, Traducción y Entrenamiento |
| [`componentes/`](componentes/) | 🧩 Piezas visuales reutilizables, agrupadas por tema |
| [`hooks/`](hooks/) | 🪝 Estado y efectos de React (cámara, captura, tema…) |
| [`estados/`](estados/) | 🚥 Constantes de estado compartidas (cámara, detector) |
| [`textos/`](textos/) | 💬 Mensajes que lee el usuario |
| [`estilos/`](estilos/) | ✨ Animaciones CSS globales |

---

## 🎯 Qué problema resuelve

1. **Que la interfaz no se quede con las reglas dentro.** Aquí no se decide
   cuándo una muestra es mala ni cómo se remuestrea: eso se pide a las capas de
   abajo y se traduce a píxeles y texto.
2. **Que el sitio se sienta uno solo**: mismo layout, misma cabecera, mismos
   botones y la misma rejilla en Traducción y Entrenamiento.
3. **Que la app sea usable de verdad**: teclado, `aria-*`, mensajes que explican
   qué pasa y por qué un botón está apagado.

---

## 🔗 Qué dependencias tiene

| Dependencia | Para qué |
|---|---|
| `react` 19 | Componentes y hooks |
| `react-router-dom` 7 | Rutas y enlaces |
| Tailwind v4 | Estilos por clases + la paleta de `index.css` |
| [`../aplicacion/`](../aplicacion/) | Crear muestras, empaquetar el lote |
| [`../infra/`](../infra/) | Cámara, detector, canvas, almacenamiento |
| [`../dominio/`](../dominio/) | Reglas y motivos de descarte (para traducirlos a texto) |

---

## 🧠 Cómo soluciona el problema

### 🧭 Rutas en un único sitio

`rutas.js` exporta `RUTAS` (congelado) y `ENLACES_DE_NAVEGACION`. El router y el
menú leen de ahí, así que **no pueden desincronizarse**: no existe el caso de un
enlace que apunte a una ruta inexistente.

### 🧅 Reparto de responsabilidades dentro de la capa

```
paginas/       ── componen la vista y su estado local
   ├── componentes/   piezas visuales, sin conocimiento del dominio
   ├── hooks/         estado y efectos (cámara, captura, tema)
   ├── estados/       constantes compartidas (evitan strings sueltos)
   └── textos/        lo que se lee en pantalla
```

Los **estados** están separados a propósito: `ESTADOS_CAMARA.ACTIVA` se compara
en la página, en el hook y en el componente de aviso; como string literal
acabaría escrito de tres formas distintas.

Los **textos** también: el dominio devuelve `'sin-manos'` y la presentación
decide que eso se lee *"No se vio ninguna mano: la muestra se descartó."*. Se
puede cambiar el mensaje sin tocar la regla.

---

## 🔍 Qué tienen los archivos

### `AplicacionRaiz.jsx`

Pregunta a `useIntroInicial()` si toca mostrar la intro. Mientras esté activa
**no monta ninguna página**, para que ninguna otra animación compita con ella.
Después declara las tres rutas.

### `rutas.js`

| Export | Contenido |
|---|---|
| `RUTAS` | `{ INICIO: '/', TRADUCCION: '/traduccion', ENTRENAMIENTO: '/entrenamiento' }` |
| `ENLACES_DE_NAVEGACION` | `[{ etiqueta, ruta }]` en el orden del menú |

---

## 💡 Ejemplos de uso

Añadir una página nueva son tres pasos:

```js
// 1. rutas.js
export const RUTAS = Object.freeze({ …, AYUDA: '/ayuda' })
export const ENLACES_DE_NAVEGACION = […, { etiqueta: 'Ayuda', ruta: RUTAS.AYUDA }]
```

```jsx
// 2. paginas/Ayuda.jsx
import PageLayout from '../componentes/layout/PageLayout'
import TituloPagina from '../componentes/layout/TituloPagina'

export default function Ayuda() {
    return (
        <PageLayout>
            <TituloPagina>Ayuda</TituloPagina>
        </PageLayout>
    )
}
```

```jsx
// 3. AplicacionRaiz.jsx
<Route path={RUTAS.AYUDA} element={<Ayuda />} />
```

El enlace del menú aparece solo: `BurgerMenu` lee `ENLACES_DE_NAVEGACION`.
