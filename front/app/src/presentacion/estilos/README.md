# ✨ `presentacion/estilos/` — Animaciones CSS globales

## 📖 Introducción

Las animaciones que **no se pueden expresar con clases de Tailwind** y que usa
más de un componente. Se importan una sola vez en `main.jsx` y quedan
disponibles en todo el sitio.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Contenido |
|---|---|
| `animaciones.css` | 🎞️ `@keyframes dust-in` (aparición "polvo" del título) y `@keyframes modal-drop-in` (entrada del panel de `InfoBubble`), con sus clases `.animate-*` |

> La intro tiene su CSS aparte
> ([`../componentes/intro/IntroSplash.css`](../componentes/intro/)): sus
> transiciones encadenadas solo las usa ella, así que viven junto a su
> componente.

---

## 🎯 Qué problema resuelve

1. **Animaciones que Tailwind no cubre.** Un desenfoque que se asienta mientras
   el texto sube y se escala necesita `@keyframes` propios.
2. **Repetirlas en cada componente.** `dust-in` la usa `TituloAnimado`; `modal-drop-in`,
   `InfoBubble`. Definirlas dos veces sería duplicar y desincronizar.
3. **Que el movimiento tenga intención.** Cada animación existe por una razón de
   producto: el título se materializa (marca), el panel cae suave (no asusta).

---

## 🔗 Qué dependencias tiene

Ninguna. Es CSS estándar (`@keyframes` + una clase por animación). Se carga
desde `main.jsx`:

```js
import './presentacion/estilos/animaciones.css'
```

Las variables de color que puedan usar vienen de `src/index.css`, que define la
paleta del sitio.

---

## 🧠 Cómo soluciona el problema

### 🌫️ `dust-in` — el título se materializa

| Momento | Estado |
|---|---|
| `0 %` | Invisible, `blur(14px)`, desplazado 14 px y un 6 % más grande |
| `60 %` | Ya opaco, `blur(3px)`: el texto "cuaja" |
| `100 %` | Nítido y en su sitio |

Dura `1500 ms` con `ease-out` y `both`, para que el elemento conserve el estado
final. `TituloAnimado` la aplica **palabra a palabra** con un retraso de 90 ms
entre palabras, que es lo que produce el efecto de barrido.

### 🪂 `modal-drop-in` — el panel desciende

De `opacity: 0` y `-32px` a su posición, con `cubic-bezier(0.16, 1, 0.3, 1)`:
una curva que frena al final, así el panel "aterriza" en vez de golpear.

---

## 🔍 Qué tienen los archivos

```css
@keyframes dust-in { … }
.animate-dust-in { animation: dust-in 1500ms ease-out both; }

@keyframes modal-drop-in { … }
.animate-modal-drop-in { animation: modal-drop-in 2000ms cubic-bezier(0.16, 1, 0.3, 1) both; }
```

Las clases se nombran `animate-*` para leerse igual que las utilidades de
Tailwind cuando aparecen mezcladas en un `className`.

---

## 💡 Ejemplos de uso

```jsx
// TituloAnimado.jsx — una palabra cada 90 ms
<span className="animate-dust-in inline-block" style={{ animationDelay: `${indice * 90}ms` }}>
    {palabra}
</span>
```

```jsx
// InfoBubble.jsx — el panel del diálogo
<div role="dialog" className="animate-modal-drop-in rounded-xl bg-surface p-8 …">
```

Para añadir una animación nueva: definir el `@keyframes`, exponer una clase
`.animate-<nombre>` y usarla desde el componente. Si solo la usa un componente,
mejor un CSS junto a él, como hace la intro.
