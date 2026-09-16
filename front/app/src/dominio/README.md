# 🎯 `dominio/` — Reglas del negocio (JavaScript puro)

La capa más interna. **No importa React, ni el DOM, ni MediaPipe**: solo datos y reglas. Es gemela de `model/signia_modelo/dominio/` en Python.

## 📄 Archivos

| Archivo | Responsabilidad |
|---|---|
| `contrato.js` | Constantes del contrato de datos: `SCHEMA`, `T=48`, 21 landmarks, 2 manos, lados... |
| `manoDelFrame.js` | Regla única para elegir la mano de un lado si MediaPipe reporta dos iguales |
| `etiquetaDeSena.js` | Normaliza el nombre de una seña (`" Hola "` → `"hola"`) |
| `reglasDeGrabacion.js` | Cuándo se cierra una grabación (4 s) y por qué se descarta (corta / sin manos) |
| `unidadesDeTiempo.js` | Conversión compartida `MS_POR_SEGUNDO` |

## 💡 Ejemplos

```js
import { motivoDeDescarte, MOTIVOS_DE_DESCARTE } from './reglasDeGrabacion.js'

motivoDeDescarte([])                          // 'demasiado-corta'
motivoDeDescarte(framesSinManos)              // 'sin-manos'
motivoDeDescarte(framesBuenos)                // null → la muestra sirve
```

```js
import { manoDelFrame } from './manoDelFrame.js'
manoDelFrame({ manos: [floja, buena] }, 'derecha')   // → la de mayor score
```

> ⚠️ Si cambias un valor de `contrato.js`, cambia también `model/signia_modelo/dominio/contrato.py`: el test de conformidad lo detectará.
