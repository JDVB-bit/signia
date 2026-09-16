# 🧪 `tests/` — Suite de pytest

Refleja las capas del paquete: una carpeta por capa.

| Elemento | Qué es |
|---|---|
| [`dominio/`](dominio/) | Validación de entidades |
| [`aplicacion/`](aplicacion/) | Remuestreo y tensor crudo |
| [`infra/`](infra/) | JSON, ficheros, rutas, normalización y ONNX |
| [`fixtures/`](fixtures/) | Casos compartidos con el test de conformidad de JS |
| `test_conformidad.py` | Verifica que los fixtures siguen coincidiendo con el código Python |
| `conftest.py` | Fixtures comunes (`muestra_aislada`, `muestra_frase`) y `sys.path` |
| `factorias.py` | Fábricas de manos, frames y muestras válidas para los tests |

## ▶️ Ejecutar

```bash
venv/Scripts/python -m pytest                     # todo (164 tests)
venv/Scripts/python -m pytest -m "not torch"      # sin torch
venv/Scripts/python -m pytest tests/infra -k onnx # un subconjunto
```

Marcadores: `torch` (necesita torch) y `onnx` (necesita onnx + onnxruntime).
