# 📷 `camara/` — Vídeo en vivo

| Archivo | Qué es |
|---|---|
| `CameraFeed.jsx` | Recuadro con el vídeo de la cámara (espejado), borde resaltable y capa superpuesta |
| `AvisoEstadoCamara.jsx` | Mensaje y botón "Activar cámara" mientras no hay vídeo |

```jsx
<CameraFeed videoRef={videoRef} onEstado={setEstado} resaltado={grabando}>
  <canvas ref={canvasRef} />   {/* se pinta encima del vídeo */}
</CameraFeed>
```

La lógica de permisos y del flujo vive en el hook `useCamara`.
