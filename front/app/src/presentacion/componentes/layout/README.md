# 📐 `layout/` — Estructura común de las páginas

| Archivo | Qué es |
|---|---|
| `PageLayout.jsx` | Fondo + `Header` + `<main>` con ancho y márgenes estándar |
| `Header.jsx` | Marca "SignIA", lema, botón de tema y menú |
| `TituloPagina.jsx` | `<h2>` principal con el estilo del sitio |
| `TituloAnimado.jsx` | Igual, pero aparece palabra a palabra (efecto "polvo") |

```jsx
<PageLayout>
  <TituloPagina>Entrenamiento</TituloPagina>
  {/* contenido */}
</PageLayout>
```
