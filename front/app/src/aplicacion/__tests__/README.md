# 🧪 Tests de la capa de aplicación

| Test | Qué verifica |
|---|---|
| `conformidad.test.js` | ⭐ Lee los fixtures de `model/tests/fixtures/` y exige que JS y Python produzcan los mismos índices y tensores (a 1e-5) |
| `remuestreo.test.js` | Longitud T, extremos, monotonía, redondeo hacia arriba, errores |
| `construirEntrada.test.js` | Ranuras fijas, mano ausente en ceros, orden temporal |
| `crearMuestra.test.js` | Formato del contrato, reindexado de `t`, validaciones |
| `fpsDeGrabacion.test.js` | Cálculo de fps y duración inválida |
| `sesionDeGrabacion.test.js` | Formato de la sesión |
| `paqueteDeMuestras.test.js` | Envoltorio con `schema` y nombre del fichero |

```bash
pnpm test -- conformidad
```

> 🚨 Si falla la conformidad **no regeneres los fixtures sin pensar**: significa que el navegador y el entrenamiento ya no calculan lo mismo.
