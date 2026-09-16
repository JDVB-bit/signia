# 🧩 `entidades/` — Lo que es una muestra

Una entidad por archivo, **inmutables** (`frozen=True`) y **autovalidadas**: si existe la instancia, cumple el contrato.

| Archivo | Entidad | Regla clave |
|---|---|---|
| `lado.py` | `Lado` | `izquierda` / `derecha` según el handedness (mano real, no la del espejo) |
| `mano.py` | `Mano` | 21 landmarks de 3 coordenadas, `score` en [0, 1] |
| `frame.py` | `Frame` | 0, 1 o 2 manos; `mano(lado)` elige la de mayor score si hay duplicadas |
| `muestra.py` | `Muestra` | Base: al menos un frame y una `sesion` identificada |
| `muestra_aislada.py` | `MuestraAislada` | Una seña. **Única unidad de entrenamiento** |
| `muestra_frase.py` | `MuestraFrase` | Varias señas. **Nunca entrena**: mide WER y calibra |
| `__init__.py` | — | Reexporta todas para importar desde un único sitio |

```python
from signia_modelo.dominio.entidades import Frame, Lado, Mano, MuestraAislada

mano = Mano(lado=Lado.DERECHA, score=0.97, lm=[(0.1, 0.2, 0.0)] * 21)
muestra = MuestraAislada(frames=[Frame(t=0, manos=[mano])], sesion="2026-09-20-snt", etiqueta="hola")
muestra.glosas        # ('hola',)
```
