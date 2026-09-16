# 🧪 Tests del adaptador de MediaPipe

Usan resultados falsos con la forma que devuelve `detectForVideo`: no necesitan cámara ni WASM.

| Test | Qué verifica |
|---|---|
| `ladoDesdeCategoria.test.js` | Traducción, inversión y categorías desconocidas |
| `frameDesdeDeteccion.test.js` | 0/1/2 manos, `handednesses` en plural, landmarks incompletos, redondeo, `z` ausente |
