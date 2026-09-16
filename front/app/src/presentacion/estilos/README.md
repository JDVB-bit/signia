# ✨ `estilos/` — CSS global

| Archivo | Qué contiene |
|---|---|
| `animaciones.css` | `animate-dust-in` (títulos) y `animate-modal-drop-in` (diálogos), con soporte de `prefers-reduced-motion` |

Se importa una vez en `src/main.jsx`, así cualquier componente puede usar las clases:

```jsx
<span className="animate-dust-in">Hola</span>
```
