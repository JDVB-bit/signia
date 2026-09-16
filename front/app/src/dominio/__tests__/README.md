# 🧪 Tests del dominio

Un archivo por módulo de `dominio/`. No necesitan navegador.

| Test | Qué verifica |
|---|---|
| `manoDelFrame.test.js` | Mano ausente, frame vacío, gana el mayor score, desempate por orden |
| `etiquetaDeSena.test.js` | Limpieza de espacios/mayúsculas y texto ausente |
| `reglasDeGrabacion.test.js` | Tope de duración, grabación corta, grabación sin manos |

```bash
pnpm test -- dominio
```
