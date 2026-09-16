# 🧠 `model/` — Etapa 1 de SignIA: señas → glosas

Convierte **landmarks de MediaPipe** en **glosas** (palabras sueltas en orden LSE). No redacta español: eso es la etapa 2 (LLM en el backend).

📜 El contrato de datos, que fija todo lo demás: [`contrato.md`](contrato.md).
🗺️ El plan completo: [`.claude/plan-implementacion.md`](../.claude/plan-implementacion.md).

## 📁 Contenido

| Elemento | Qué es |
|---|---|
| [`signia_modelo/`](signia_modelo/) | El paquete Python, en capas de Clean Architecture |
| [`tests/`](tests/) | Suite de pytest (164 tests) y fixtures de conformidad JS ↔ Python |
| [`scripts/`](scripts/) | Utilidades de línea de comandos |
| `contrato.md` | Formato de las muestras, remuestreo, tensor y features |
| `pyproject.toml` | Paquete instalable + configuración de pytest y sus marcadores |
| `requirements.txt` | Dependencias fijadas (torch con CUDA 13, ONNX, pytest...) |
| `.gitignore` | Ignora `data/`, `artefactos/` y cachés |

## 🏛️ Capas

```
signia_modelo/
  dominio/       entidades, contrato y puertos       (python puro)
  aplicacion/    remuestreo y tensor crudo            (numpy)
  infra/         JSON, disco, torch/ONNX              (frameworks)
```

**Las capas de dentro no importan nada de las de fuera.** Cambiar disco por la nube o torch por otra cosa es escribir otro adaptador en `infra/`.

## ▶️ Uso

```bash
# instalar (Windows)
python -m venv venv
venv/Scripts/pip install -r requirements.txt

# todos los tests
venv/Scripts/python -m pytest

# solo lo que no necesita torch (~3 s)
venv/Scripts/python -m pytest -m "not torch"

# regenerar los fixtures de conformidad JS <-> Python
venv/Scripts/python scripts/generar_fixtures.py
```

```python
from signia_modelo.aplicacion.preprocess import construir_entrada
from signia_modelo.infra.repo_ficheros import RepositorioMuestrasEnDisco

repo = RepositorioMuestrasEnDisco()            # usa DATOS_DIR o ./data
for muestra in repo.listar(tipo="aislada"):
    entrada = construir_entrada(muestra)       # lm (48,2,21,3) + presencia (48,2)
```

## 📈 Estado

- [x] **Fase 0** — contrato, remuestreo, tensor crudo, normalización en el grafo ONNX, repositorio y tests.
- [x] **Fase 1** — captura en el front (`front/app/src/`, capas dominio/aplicacion/infra/presentacion).
- [ ] Fase 2 — dataset (aisladas + `reposo` + frases de evaluación).
- [ ] Fase 3 — baseline DTW.
- [ ] Fase 4 — modelo, WER por frase y artefacto.
