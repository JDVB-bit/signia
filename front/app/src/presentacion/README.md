# 🎨 `presentacion/` — Interfaz en React

La capa exterior: todo lo que el usuario ve y toca. Usa las demás capas, ninguna la usa a ella.

| Elemento | Qué contiene |
|---|---|
| `AplicacionRaiz.jsx` | Intro (primera visita) o las rutas del sitio |
| `rutas.js` | Única fuente de URLs y de los enlaces del menú |
| [`paginas/`](paginas/) | Inicio, Traducción y Entrenamiento |
| [`componentes/`](componentes/) | Piezas visuales reutilizables, agrupadas por tema |
| [`hooks/`](hooks/) | Estado y efectos de React (cámara, captura, tema...) |
| [`estados/`](estados/) | Constantes de estado compartidas (cámara, detector) |
| [`textos/`](textos/) | Mensajes para el usuario |
| [`estilos/`](estilos/) | Animaciones CSS globales |

## ➕ Añadir una página

```js
// 1. rutas.js
export const RUTAS = Object.freeze({ ..., AYUDA: '/ayuda' })
export const ENLACES_DE_NAVEGACION = [..., { etiqueta: 'Ayuda', ruta: RUTAS.AYUDA }]
```

```jsx
// 2. AplicacionRaiz.jsx
<Route path={RUTAS.AYUDA} element={<Ayuda />} />
```
