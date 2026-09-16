# 🔌 `infra/` — Adaptadores a tecnologías externas

Aquí vive todo lo que depende de una librería o API del navegador. Si mañana cambia MediaPipe o el almacenamiento, **solo se toca esta capa**.

| Carpeta | Adapta... |
|---|---|
| [`mediapipe/`](mediapipe/) | El detector de manos de Google a frames del contrato |
| [`canvas/`](canvas/) | El dibujo del esqueleto sobre el vídeo |
| [`navegador/`](navegador/) | Cámara, `localStorage`/`sessionStorage`, descargas y tema |
