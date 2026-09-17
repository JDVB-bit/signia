# 🏗️ `componentes/layout/` — Esqueleto común de las páginas

## 📖 Introducción

Lo que hace que Inicio, Traducción y Entrenamiento se sientan **el mismo sitio**:
el mismo fondo, la misma cabecera, el mismo ancho de contenido y los títulos con
el mismo peso.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Responsabilidad |
|---|---|
| `PageLayout.jsx` | 📐 Base de cualquier página: fondo + `Header` + `<main>` con ancho y espaciado estándar |
| `Header.jsx` | 🔝 Cabecera: marca y lema a la izquierda; tema y menú a la derecha |
| `TituloPagina.jsx` | 🔠 Título principal, y la constante `ESTILOS_TITULO_PAGINA` que lo define |
| `TituloAnimado.jsx` | ✨ El mismo título, revelado palabra a palabra con el efecto "polvo" |

---

## 🎯 Qué problema resuelve

1. **Que cada página reinvente su marco.** Sin un layout común, los márgenes y
   el ancho acaban distintos en cada vista y el sitio parece de dos equipos.
2. **Que el título se desincronice.** Inicio quiere animación y las demás no,
   pero **el tamaño debe ser idéntico**: por eso el estilo se comparte como
   constante y hay dos componentes que lo usan.
3. **Jerarquía de encabezados correcta.** El lema del header es un `<p>`, no un
   `<h3>`: si fuera encabezado rompería el orden `h1 > h2` de cada página.

---

## 🔗 Qué dependencias tiene

- `react` (solo `Fragment` en `TituloAnimado`).
- Hermanos: `../navegacion/BurgerMenu` y `../tema/ThemeToggle`, usados por `Header`.
- La animación `animate-dust-in` de
  [`../../estilos/animaciones.css`](../../estilos/).
- Tailwind y la paleta de `src/index.css`.

---

## 🧠 Cómo soluciona el problema

### 📐 El contenido llega como `children`

```jsx
<PageLayout>
    {/* la página decide su título y su contenido */}
</PageLayout>
```

`PageLayout` **no impone el título**: así Inicio puede usar `TituloAnimado` y las
demás `TituloPagina`, sin que el layout tenga que saber cuál toca ni recibir
banderas.

### 🔠 Un estilo, dos presentaciones

```js
export const ESTILOS_TITULO_PAGINA =
    'text-center text-4xl font-extrabold tracking-tight text-brand drop-shadow-sm sm:text-5xl lg:text-6xl'
```

`TituloAnimado` importa esa constante de `TituloPagina`: si mañana el título
crece, crece en todas las páginas a la vez.

### ✨ El truco de los espacios

`inline-block` se come el espacio entre palabras, así que `TituloAnimado` lo
repone como nodo de texto **fuera** del `<span>` animado. Sin eso, el título
aparecería con las palabras pegadas.

---

## 🔍 Qué tienen los archivos

### `PageLayout.jsx`

| Elemento | Clases clave |
|---|---|
| Contenedor | `min-h-screen bg-bg` + transición de color para el cambio de tema |
| `<main>` | `mx-auto max-w-[110rem] space-y-14 px-6 py-14 sm:px-10 lg:px-16` |

### `Header.jsx`

`<h1>SignIA</h1>` + lema, y un `<nav aria-label="Preferencias y navegación">` con
`ThemeToggle` y `BurgerMenu`.

### `TituloPagina.jsx`

Exporta el componente (por defecto) y `ESTILOS_TITULO_PAGINA` (con nombre).

### `TituloAnimado.jsx`

`RETRASO_ENTRE_PALABRAS_MS = 90`. Divide el texto por espacios y aplica un
`animationDelay` creciente a cada palabra.

---

## 💡 Ejemplos de uso

```jsx
// Una página normal
<PageLayout>
    <TituloPagina>Traductor</TituloPagina>
    {/* … */}
</PageLayout>
```

```jsx
// La portada, con el título que se materializa
<PageLayout>
    <TituloAnimado texto="Traductor de lengua de señas con Inteligencia Artificial" />
    {/* … */}
</PageLayout>
```

> 📌 Toda página nueva debe envolverse en `PageLayout`. Si una vista necesitara
> un marco distinto (por ejemplo, pantalla completa), el camino correcto es
> crear otro layout hermano, no añadir condiciones a este.
