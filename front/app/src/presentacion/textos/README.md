# 💬 `textos/` — Mensajes para el usuario

Separados de la lógica: el dominio devuelve **códigos** y aquí se convierten en frases.

| Archivo | Qué contiene |
|---|---|
| `textosDeCaptura.js` | Avisos de la captura y texto por motivo de descarte |
| `mensajeDeEstadoDeCaptura.js` | Elige la única línea de estado de Entrenamiento según prioridad |

```js
mensajeDeEstadoDeCaptura({ aviso: null, camaraActiva: false, estadoDetector, sesion })
// → 'Activa la cámara para empezar a grabar.'
```

🌍 Tener los textos aquí deja preparado el camino para traducir la interfaz.
