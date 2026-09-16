# 🖼️ `assets/` — Imágenes de la interfaz

Se importan desde los componentes; Vite las optimiza y les añade hash para cachearlas.

| Archivo | Dónde se usa |
|---|---|
| `senas-persona1.jpg` | Carrusel de la página de Inicio |
| `senas-persona2.jpg` | Carrusel de la página de Inicio |
| `senas-persona3.jpg` | Carrusel de la página de Inicio |

```jsx
import senasPersona1 from '../../assets/senas-persona1.jpg'
<img src={senasPersona1} alt="Persona haciendo una seña en LSE" />
```

> ⚡ `senas-persona3.jpg` pesa ~940 KB: conviene exportarla a WebP/AVIF.
