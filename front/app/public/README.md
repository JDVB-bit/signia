# 🌍 `public/` — Archivos estáticos servidos tal cual

Vite copia esta carpeta **sin procesar** a la raíz del build. Lo que está aquí se pide por URL absoluta (`/favicon.svg`, `/mediapipe/...`).

| Elemento | Qué es |
|---|---|
| `favicon.svg` | Icono 🤟 de la pestaña del navegador |
| [`mediapipe/`](mediapipe/) | Runtime WASM y modelo de MediaPipe, alojados por nosotros |

> 💡 No pongas aquí imágenes que use un componente: van en `src/assets/` para que Vite las optimice y les ponga hash.
