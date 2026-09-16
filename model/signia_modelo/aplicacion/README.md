# ⚙️ `aplicacion/` — Preprocesado

Depende solo del dominio y de numpy. **Aquí no se normaliza nada**: eso ocurre dentro del grafo ONNX.

| Archivo | Responsabilidad |
|---|---|
| `remuestreo.py` | De `n` frames a `T` índices con `int(x + 0.5)` (gemelo de `front/app/src/aplicacion/remuestreo.js`) |
| `preprocess.py` | Muestra → `EntradaCruda(lm (T,2,21,3), presencia (T,2))` con ranuras fijas |

```python
from signia_modelo.aplicacion.preprocess import construir_entrada
from signia_modelo.aplicacion.remuestreo import indices_remuestreo

indices_remuestreo(3, 5)                 # [0, 1, 1, 2, 2]
entrada = construir_entrada(muestra)     # remuestreador inyectable (DIP)
entrada.lm.shape                         # (48, 2, 21, 3)
```
