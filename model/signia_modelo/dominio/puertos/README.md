# 🔌 `puertos/` — Interfaces del dominio

`Protocol` de Python: quien los implementa no hereda de nada (**DIP**) y cada uno es pequeño (**ISP**).

| Archivo | Puerto | Implementación actual |
|---|---|---|
| `remuestreador.py` | `Remuestreador.indices(n_frames, destino)` | `aplicacion/remuestreo.py → RemuestreadorPorIndices` |
| `repositorio_muestras.py` | `LectorMuestras`, `EscritorMuestras`, `RepositorioMuestras` | `infra/repo_ficheros.py → RepositorioMuestrasEnDisco` |

```python
from signia_modelo.dominio.puertos import RepositorioMuestras

def contar_aisladas(repo: RepositorioMuestras) -> int:
    return sum(1 for _ in repo.listar(tipo="aislada"))   # sirve con disco, GCS, memoria...
```
