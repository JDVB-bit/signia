# 🦴 `infra/canvas/` — Overlay del esqueleto de la mano

| Archivo | Responsabilidad |
|---|---|
| `dibujarManos.js` | Dibuja huesos, articulaciones y el rótulo del lado en un contexto 2D |
| `pintarManosSobreVideo.js` | Ajusta el canvas a la resolución del vídeo y llama a `dibujarManos` |

## 💡 Uso

```js
import { pintarManosSobreVideo } from './pintarManosSobreVideo.js'
pintarManosSobreVideo(canvasRef.current, videoRef.current, frame.manos)
```

🎨 Cada lado tiene su color (`COLOR_POR_LADO`) para detectar de un vistazo si MediaPipe se equivoca de mano. Las coordenadas se espejan igual que el vídeo.
