# 🎬 `componentes/intro/` — Pantalla de carga inicial

## 📖 Introducción

La primera impresión del sitio: la marca **SignIA** aparece centrada, se sostiene
un momento y viaja hasta la esquina donde vive el logo real del header, mientras
una barra de carga avanza con una mano que va cambiando de seña.

Se ve **una sola vez**: recargar la página no la vuelve a disparar.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Responsabilidad |
|---|---|
| `IntroSplash.jsx` | ⏱️ Máquina de fases: calcula el progreso, decide la fase y avisa al terminar |
| `IntroSplash.css` | 🎨 El aspecto y las transiciones de cada fase |

---

## 🎯 Qué problema resuelve

1. **Dar identidad desde el primer segundo.** Un proyecto académico con una
   entrada cuidada se recuerda distinto.
2. **Que no compita con el resto.** Mientras la intro está en pantalla no se
   monta ninguna página, así ninguna otra animación corre a la vez.
3. **Que no moleste.** Se muestra una vez por navegador, dura menos de 5 s y
   respeta `prefers-reduced-motion`.

---

## 🔗 Qué dependencias tiene

- `react` (`useState`, `useEffect`, `useRef`).
- Su propio CSS, importado por el componente.
- Quien decide cuándo mostrarla es
  [`../../hooks/useIntroInicial`](../../hooks/), apoyado en
  [`infra/navegador/registroDeIntro.js`](../../../infra/navegador/).

Las variables de color (`--color-bg`, `--color-brand`, `--color-surface`) vienen
de `src/index.css`: la intro nace ya con el tema correcto.

---

## 🧠 Cómo soluciona el problema

### ⏱️ Cuatro fases encadenadas

| Fase | Duración | Qué ocurre |
|---|---|---|
| `aparicion` | 850 ms | La marca aparece centrada y crece hasta su tamaño |
| `espera` | 400 ms | Se sostiene, para que se lea |
| `succion` | 2800 ms | Viaja a la esquina superior izquierda y se reduce a la mitad |
| `crossfade` | 350 ms | El fondo pasa a `surface` y el componente se desmonta |

Más un retraso inicial de 250 ms: **total ≈ 4,65 s**, cómodamente por debajo del
límite de 6 s que se fijó para la animación completa.

### 🔗 Un solo reloj para JS y CSS

Las duraciones se declaran una vez en el JSX y se pasan al CSS como variables
(`--intro-duracion-aparicion`, etc.). Así no hay dos juegos de números que
puedan desincronizarse: si se cambia una fase, la transición la sigue.

### 📍 Destino calculado, no adivinado

La posición final (`top: 2.1rem; left: 1.5rem`, y `2.5rem` a partir de `sm`)
coincide con la del título real del header. Por eso la transición se percibe
como si la marca "se convirtiera" en el logo del sitio.

### ♿ Movimiento reducido

Con `prefers-reduced-motion: reduce`, todas las duraciones bajan a `1 ms`: quien
lo tenga activado ve la pantalla pasar sin animación.

---

## 🔍 Qué tienen los archivos

### `IntroSplash.jsx`

| Elemento | Detalle |
|---|---|
| `FASES` | `aparicion`, `espera`, `succion`, `crossfade` (congelado) |
| `faseEn(transcurridoMs)` | Fase actual, o `null` cuando ya terminó |
| `SENAS_POR_PROGRESO` | Emojis por umbral: 🖐️ 0 %, 🤟 25 %, 🤙 75 %, 👌 99 % |
| `senaActual(progreso)` | El último umbral superado |
| `onFinishRef` | Ref al callback: cambiarlo no reinicia la animación |

El progreso se calcula con `requestAnimationFrame` sobre `performance.now()`, no
con `setInterval`: así va al ritmo real de repintado del navegador.

| Prop | Para qué |
|---|---|
| `onFinish` | Se llama al terminar; quien la usa decide qué hacer (guardar que ya se vio) |

El overlay lleva `role="presentation"` y `aria-hidden="true"`: es decoración, y
no debe leerse en voz alta.

### `IntroSplash.css`

Clases por fase (`.intro-marca--succion`, `.intro-carga--crossfade`…), la barra
de progreso y la media query de movimiento reducido.

---

## 💡 Ejemplos de uso

```jsx
// AplicacionRaiz.jsx
const { mostrarIntro, finalizarIntro } = useIntroInicial()

if (mostrarIntro) return <IntroSplash onFinish={finalizarIntro} />
return <Routes>{/* … */}</Routes>
```

Para volver a verla durante el desarrollo, basta con borrar la marca del
navegador:

```js
localStorage.removeItem('signia-intro-vista')
```

> 🖐️ Los emojis son provisionales. Cuando haya assets reales de manos, se
> sustituye `SENAS_POR_PROGRESO` sin tocar el resto del componente.
