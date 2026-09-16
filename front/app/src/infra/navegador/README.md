# 🌐 `infra/navegador/` — APIs del navegador

| Archivo | Responsabilidad |
|---|---|
| `almacenamientoSeguro.js` | Leer/guardar en `localStorage` y `sessionStorage` **sin lanzar** (modo privado, cuota llena) |
| `preferenciaDeTema.js` | Tema claro/oscuro: preferencia guardada, del sistema y clase `.dark` |
| `registroDeIntro.js` | Recuerda si ya se vio la intro |
| `permisoDeCamara.js` | Recuerda durante la visita si se concedió la cámara |
| `camara.js` | `getUserMedia`: abrir y cerrar el flujo de vídeo |
| `descargarJson.js` | Descarga un objeto como fichero `.json` |

## 💡 Ejemplos

```js
import { leerLocal, guardarLocal } from './almacenamientoSeguro.js'
guardarLocal('clave', 'valor')      // nunca lanza
leerLocal('clave')                  // 'valor' o null

import { abrirCamara, cerrarCamara } from './camara.js'
const flujo = await abrirCamara()
cerrarCamara(flujo)                 // apaga la luz de la cámara
```
