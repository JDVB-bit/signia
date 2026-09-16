# 🎯 `dominio/` — Núcleo sin dependencias

Python puro: ni numpy, ni torch, ni ficheros. Todo lo demás depende de esto.

| Elemento | Responsabilidad |
|---|---|
| `contrato.py` | 📜 Constantes del contrato: `SCHEMA`, `T=48`, `F=128`, índices de muñeca y nudillo, rango de `score`... |
| `errores.py` | 🚨 Jerarquía de errores (`ErrorDeSignia` → `ErrorDeContrato`, `ErrorDeRemuestreo`) |
| [`entidades/`](entidades/) | 🧩 `Lado`, `Mano`, `Frame`, `Muestra`, `MuestraAislada`, `MuestraFrase` |
| [`puertos/`](puertos/) | 🔌 Interfaces `Remuestreador` y repositorio de muestras |

```python
from signia_modelo.dominio.contrato import T, F
from signia_modelo.dominio.errores import ErrorDeContrato
```
