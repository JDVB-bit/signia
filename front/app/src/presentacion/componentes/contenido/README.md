# 📰 `componentes/contenido/` — Bloques de la página de Inicio

## 📖 Introducción

Las piezas con las que se cuenta **qué es SignIA**: tarjetas de sección, texto
que se escribe solo, una burbuja para el detalle y un carrusel de imágenes.

Todas son genéricas: reciben su contenido por props y no saben nada de lengua de
señas.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Responsabilidad |
|---|---|
| `SectionCard.jsx` | 🗂️ Tarjeta con título sobre `surface` |
| `Typewriter.jsx` | ⌨️ Revela un texto carácter a carácter, con cursor parpadeante |
| `InfoBubble.jsx` | 💬 Botón *i* que abre un diálogo centrado con el detalle |
| `ImageBelt.jsx` | 🎞️ Carrusel "cinturón": cada imagen empuja a la anterior |
| `CarouselImage.jsx` | 🖼️ Una sola imagen del cinturón |

---

## 🎯 Qué problema resuelve

1. **Dos velocidades de lectura.** Quien pasa por encima lee tres frases; quien
   quiere más abre la burbuja. Sin ese reparto, la portada sería un muro de
   texto o sería insuficiente.
2. **Explicar sin tecnicismos.** El contenido habla de personas y situaciones, no
   de MediaPipe ni de tensores: la portada es para el usuario final.
3. **Enseñar de qué va antes de leer.** Tres fotos en rotación dicen "lengua de
   señas" más rápido que cualquier párrafo.

---

## 🔗 Qué dependencias tiene

- `react` (`useState`, `useEffect`, `useId`, `useCallback`).
- [`../../hooks/useCerrarConEscape`](../../hooks/) — lo usa `InfoBubble`.
- La animación `animate-modal-drop-in` de [`../../estilos/`](../../estilos/).
- Las imágenes de [`src/assets/`](../../../assets/), que pasa la página.

---

## 🧠 Cómo soluciona el problema

### 💬 Burbuja accesible de verdad

| Detalle | Implementación |
|---|---|
| Es un diálogo | `role="dialog"` + `aria-modal="true"` |
| El botón lo anuncia | `aria-haspopup="dialog"`, `aria-expanded`, `aria-controls` |
| Se cierra de tres formas | Botón ✕, tecla `Escape`, clic en el fondo |
| El clic dentro no cierra | `stopPropagation` en el panel |
| El id es único | `useId()`, aunque haya tres burbujas en la misma página |

### 🎞️ Carrusel sin salto

El problema clásico de un carrusel es el tirón al volver de la última a la
primera. Aquí se añade **una copia de la primera imagen al final**:

```
[ 1 ][ 2 ][ 3 ][ 1' ]
                 ▲ al llegar, se salta al índice 0 sin transición (invisible)
```

Y la transición se reactiva en el frame siguiente, con `requestAnimationFrame`,
para que el salto no se vea.

### ⌨️ Escritura que no marea

25 ms por carácter: se percibe que se escribe, pero nadie espera. El cursor ▌
solo aparece mientras queda texto.

---

## 🔍 Qué tienen los archivos

### `SectionCard.jsx`

| Prop | Para qué |
|---|---|
| `title` | Encabezado `<h3>` de la tarjeta |
| `className` | Ajustes de columna o altura desde la página |
| `children` | Contenido |

### `Typewriter.jsx`

| Prop | Por defecto | Para qué |
|---|---|---|
| `text` | — | Texto a revelar |
| `speed` | `25` ms (`MS_POR_CARACTER`) | Velocidad |
| `className` | `''` | Estilos del párrafo |

### `InfoBubble.jsx`

| Prop | Por defecto | Para qué |
|---|---|---|
| `label` | `'Más información'` | Texto junto al icono *i* |
| `children` | — | Contenido del panel |

### `ImageBelt.jsx` y `CarouselImage.jsx`

| Constante | Valor |
|---|---|
| `TIEMPO_VISIBLE_MS` | `7500` |
| `DURACION_TRANSICION_MS` | `700` |
| `CURVA_TRANSICION` | `cubic-bezier(0.65, 0, 0.35, 1)` |

`ImageBelt` recibe `images: [{ src, alt }]`. `CarouselImage` existe aparte para
que el cinturón se ocupe solo de la posición, no de cómo se pinta cada imagen.

---

## 💡 Ejemplos de uso

```jsx
<SectionCard title="¿Qué es?">
    <Typewriter className="mt-3 leading-relaxed" text="SignIA es una aplicación web que…" />
    <InfoBubble label="Más sobre qué es SignIA">
        <p>Explicación larga, con el espacio y el interlineado para leerla a gusto.</p>
    </InfoBubble>
</SectionCard>
```

```jsx
const IMAGENES = [senas1, senas2, senas3].map((src) => ({
    src,
    alt: 'Persona haciendo una seña en LSE',
}))

<ImageBelt images={IMAGENES} />
```

> ♿ El `alt` de las imágenes es parte del dato (`{ src, alt }`), no un detalle
> del componente: quien añade una imagen tiene que describirla.
