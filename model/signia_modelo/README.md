# 📦 `signia_modelo/` — Paquete Python del modelo

| Capa | Carpeta | Depende de | Contiene |
|---|---|---|---|
| 🎯 Dominio | [`dominio/`](dominio/) | nada | contrato, entidades, errores, puertos |
| ⚙️ Aplicación | [`aplicacion/`](aplicacion/) | dominio + numpy | remuestreo y construcción del tensor |
| 🔌 Infra | [`infra/`](infra/) | todo + frameworks | JSON, disco, torch, ONNX |

| Archivo | Qué hace |
|---|---|
| `__init__.py` | Documenta las capas y reexporta `contrato` |

```python
from signia_modelo import contrato
contrato.T, contrato.F      # (48, 128)
```
