# 🎬 `intro/` — Pantalla de carga inicial

| Archivo | Qué es |
|---|---|
| `IntroSplash.jsx` | Marca que aparece, barra de carga con emojis de señas y "succión" hacia el header |
| `IntroSplash.css` | Animaciones de cada fase; las **duraciones llegan como variables CSS** desde el JSX |

Fases: `aparicion → espera → succion → crossfade` (~4,65 s en total). Solo se muestra en la primera visita (`useIntroInicial`).

```jsx
<IntroSplash onFinish={finalizarIntro} />
```
