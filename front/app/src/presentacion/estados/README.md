# 🚦 `estados/` — Estados compartidos

Constantes congeladas para no escribir cadenas sueltas (`'activa'`, `'listo'`) por la interfaz.

| Archivo | Estados |
|---|---|
| `estadosDeCamara.js` | `INICIAL`, `SOLICITANDO`, `ACTIVA`, `DENEGADA`, `NO_SOPORTADA` |
| `estadosDelDetector.js` | `INACTIVO`, `CARGANDO`, `LISTO`, `ERROR` |

```js
import { ESTADOS_CAMARA } from '../estados/estadosDeCamara'
const activa = estado === ESTADOS_CAMARA.ACTIVA
```
