# 📎 `fixtures/` — Casos de conformidad JS ↔ Python

Cada `.json` contiene una **muestra cruda** y el **tensor esperado** que produce Python. Los leen `tests/test_conformidad.py` y `front/app/src/aplicacion/__tests__/conformidad.test.js`.

| Fixture | Caso límite |
|---|---|
| `un_frame.json` | Una grabación de un solo frame (se repite 48 veces) |
| `corta_12.json` | Menos frames que `T` (se repiten) |
| `exacta_48.json` | Exactamente `T` frames (identidad) |
| `larga_120.json` | Más frames que `T` y dos manos (se saltan) |
| `sin_manos.json` | Ningún frame con manos (todo ceros) |
| `intermitente.json` | La mano entra, cambia de lado y aparecen las dos |

```json
{ "nombre": "corta_12", "version_preprocesado": "1", "T": 48,
  "muestra": { "...": "contrato" },
  "esperado": { "indices": [0, 0, ...], "presencia": [...], "lm": [...] } }
```

🔁 Se generan con `scripts/generar_fixtures.py`. **No se editan a mano.**
