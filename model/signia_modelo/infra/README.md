# 🔌 `infra/` — Adaptadores

Todo lo que es "detalle": formatos, rutas, variables de entorno y frameworks.

| Archivo | Responsabilidad |
|---|---|
| `json_contrato.py` | 🔄 dict JSON ↔ entidades, con validación y mensajes accionables |
| `ficheros_json.py` | 💾 Cargar / guardar una muestra en un `.json` |
| `nombres_de_ruta.py` | 🛡️ Sanear etiquetas y sesiones antes de usarlas como carpeta (`../` bloqueado) |
| `configuracion_datos.py` | ⚙️ Raíz del dataset por `DATOS_DIR` (por defecto `./data`) |
| `repo_ficheros.py` | 🗂️ Dataset en disco: `crudo/aisladas/<etiqueta>/` y `crudo/frases/` |
| `normalizacion_torch.py` | 🧮 Crudo → 128 features como `nn.Module` (viaja dentro del ONNX) |
| `exportacion_onnx.py` | 📦 Exporta a ONNX con lote y tiempo dinámicos |
| `ejecucion_onnx.py` | ▶️ Ejecuta el grafo con onnxruntime (paridad con torch) |

```python
from signia_modelo.infra.repo_ficheros import RepositorioMuestrasEnDisco
repo = RepositorioMuestrasEnDisco("data")
identificador = repo.guardar(muestra)      # '2026-09-20-snt-0000' en data/crudo/aisladas/hola/
repo.contar()                              # {'hola': 1}
```

```python
from signia_modelo.infra.exportacion_onnx import exportar
from signia_modelo.infra.ejecucion_onnx import salida_onnx
from signia_modelo.infra.normalizacion_torch import NOMBRES_ENTRADA, NOMBRE_SALIDA, Normalizacion

ruta = exportar(Normalizacion(), (lm, presencia), "artefactos/norm.onnx",
                nombres_entrada=NOMBRES_ENTRADA, nombre_salida=NOMBRE_SALIDA)
features = salida_onnx(ruta, {"lm": lm_np, "presencia": presencia_np})   # (B, T, 128)
```
