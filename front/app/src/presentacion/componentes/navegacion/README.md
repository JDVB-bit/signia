# 🧭 `componentes/navegacion/` — Moverse por el sitio

## 📖 Introducción

El menú del sitio. Un icono hamburguesa que se convierte en ✕ y despliega los
enlaces a las tres páginas, pensado para funcionar igual con ratón, con dedo y
con teclado.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Responsabilidad |
|---|---|
| `BurgerMenu.jsx` | 🍔 Botón animado + panel con los enlaces de `ENLACES_DE_NAVEGACION` |

---

## 🎯 Qué problema resuelve

1. **Tres páginas sin forma de saltar entre ellas.** El menú es la única
   navegación del sitio.
2. **Menús que atrapan al usuario.** Uno que solo se cierra pulsando otra vez el
   icono es incómodo; este se cierra con clic fuera, con `Escape` y al elegir un
   enlace.
3. **Enlaces que se desincronizan de las rutas.** Si el menú tuviera su propia
   lista, un cambio de URL dejaría un enlace roto.
4. **Navegación con teclado.** Abrir un panel y dejar el foco donde estaba
   obliga a tabular a ciegas.

---

## 🔗 Qué dependencias tiene

| Dependencia | Para qué |
|---|---|
| `react-router-dom` (`Link`) | Navegar sin recargar la página |
| [`../../rutas.js`](../../rutas.js) | `ENLACES_DE_NAVEGACION`: la única lista de enlaces |
| [`../../hooks/useCerrarConEscape`](../../hooks/) | Cerrar con `Escape` |
| `react` | `useState`, `useId`, `useRef`, `useEffect`, `useCallback` |

---

## 🧠 Cómo soluciona el problema

### 🔗 Una sola fuente de rutas

```js
import { ENLACES_DE_NAVEGACION } from '../../rutas'
```

El router y el menú leen la misma constante: **no puede existir** un enlace que
apunte a una ruta inexistente.

### 🍔 El icono explica su estado

Tres barras que se transforman con `transition-transform`: la primera baja y
rota 45°, la del medio desaparece, la tercera sube y rota -45°. El resultado es
una ✕, sin cambiar de icono ni cargar un SVG.

### ♿ Accesibilidad

| Detalle | Implementación |
|---|---|
| Estado del botón | `aria-expanded` + `aria-label` que cambia (*Abrir* / *Cerrar menú*) |
| Relación botón-panel | `aria-controls` con un `useId()` |
| El panel es navegación | `<nav aria-label="Menú principal">` con lista `<ul>` |
| Foco al abrir | Va al **primer enlace**, para tabular desde ahí |
| Cierre con teclado | `Escape` |

### 🖱️ Fondo que cierra

El overlay es un `<button>` con `aria-label="Cerrar menú"`, no un `<div>` con
`onClick`: así también es alcanzable y accionable con teclado.

---

## 🔍 Qué tiene el archivo

| Prop | Por defecto | Para qué |
|---|---|---|
| `enlaces` | `ENLACES_DE_NAVEGACION` | Permite inyectar otra lista (por ejemplo, en pruebas) |

| Estado interno | Para qué |
|---|---|
| `abierto` | Si el panel está desplegado |
| `panelId` | Id único para `aria-controls` |
| `primerEnlaceRef` | Destino del foco al abrir |

El panel se posiciona con `absolute right-0 mt-2 w-48` y el overlay con
`fixed inset-0 z-40`, por debajo del panel (`z-50`).

---

## 💡 Ejemplos de uso

```jsx
// En el Header, sin configurar nada
<BurgerMenu />
```

```jsx
// Con una lista propia
<BurgerMenu enlaces={[{ etiqueta: 'Inicio', ruta: '/' }]} />
```

Para añadir una entrada al menú **no se toca este componente**: se añade a
`rutas.js`.

```js
export const ENLACES_DE_NAVEGACION = [
    { etiqueta: 'Inicio', ruta: RUTAS.INICIO },
    { etiqueta: 'Traductor', ruta: RUTAS.TRADUCCION },
    { etiqueta: 'Entrenamiento', ruta: RUTAS.ENTRENAMIENTO },
]
```
