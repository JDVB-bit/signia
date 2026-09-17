# 🧠 `model/` — Etapa 1 de SignIA: señas → glosas

## 📖 Introducción

El paquete Python que convierte **landmarks de MediaPipe** en **glosas**:
palabras sueltas, sin conjugar, en el orden de la LSE. No redacta español — eso
es la etapa 2 (un LLM en el backend, Fase 6b).

Hoy están cerradas la **Fase 0** (contrato, preprocesado, normalización ONNX,
repositorio y tests) y la **Fase 1** (captura en el front). En curso la **Fase 2**
(dataset): la red de contrato cruzado ya está puesta; falta grabar.

📜 El contrato de datos, que fija todo lo demás: [`contrato.md`](contrato.md) en
prosa y [`contrato.json`](contrato.json) para las máquinas.
🗺️ El plan completo: [`../.claude/plan-implementacion.md`](../.claude/plan-implementacion.md).

---

## 📂 Qué archivos y carpetas tiene

| Elemento | Qué es |
|---|---|
| [`signia_modelo/`](signia_modelo/) | 📦 El paquete, en capas de Clean Architecture |
| [`tests/`](tests/) | 🧪 Suite de pytest (187 tests) y fixtures de conformidad JS ↔ Python |
| [`scripts/`](scripts/) | 🛠️ Utilidades de línea de comandos |
| `contrato.md` | 📜 **Fuente de verdad**: formato de las muestras, remuestreo, tensor y features |
| `contrato.json` | 🤖 Gemelo generado de `contrato.md`: las constantes que el front tiene que declarar igual |
| `pyproject.toml` | ⚙️ Paquete instalable + configuración de pytest y sus marcadores |
| `requirements.txt` | 📌 Dependencias fijadas (torch con CUDA 13, ONNX, pytest…) |
| `.gitignore` | 🚫 Ignora `data/`, `artefactos/` y cachés |

---

## 🎯 Qué problema resuelve

1. **Reconocer señas con poquísimo dato.** Entrenar con vídeo exigiría miles de
   muestras; con 21 landmarks por mano, decenas por seña pueden bastar.
2. **Que el navegador y el entrenamiento no diverjan.** El preprocesado se
   escribe una sola vez, salvo el remuestreo, que se vigila con fixtures.
3. **Que nada de lo grabado se pierda.** El dataset se guarda **crudo**: features,
   pesos y métricas son derivados y reconstruibles.
4. **Que el vocabulario pueda crecer.** `n_clases` sale del dataset, nunca de una
   constante en el código.

---

## 🔗 Qué dependencias tiene

| Dependencia | Cuándo |
|---|---|
| Python ≥ 3.12 | Siempre |
| `numpy >= 2.0` | Siempre |
| `torch`, `onnx`, `onnxruntime` | Entrenar y exportar (extra `entrenamiento`) |
| `pytest >= 8` | Tests (extra `dev`) |

`requirements.txt` fija además el índice de PyTorch con **CUDA 13.0**, para que
torch use la GPU y no la versión CPU-only.

Su contraparte es [`../front/`](../front/): comparten el contrato y los fixtures.

---

## 🧠 Cómo soluciona el problema

### 🏛️ Capas

```
signia_modelo/
  dominio/       entidades, contrato y puertos       (python puro)
  aplicacion/    remuestreo y tensor crudo           (numpy)
  infra/         JSON, disco, torch/ONNX             (frameworks)
```

**Las capas de dentro no importan nada de las de fuera.** Cambiar disco por la
nube, o torch por otra cosa, es escribir otro adaptador en `infra/`.

### 🔀 Reparto entre JS y el grafo ONNX

```
JS y Python (idéntico y trivial):  elegir 48 índices → (48,2,21,3) + presencia
Dentro del grafo ONNX:             restar muñeca, escala, dividir → (48,128)
                                   → Encoder → Cabeza → logits
```

Meter la normalización **dentro del grafo** es lo único que garantiza que el
navegador y el entrenamiento ejecuten literalmente el mismo código.

### 📊 La unidad de aprendizaje es la seña

| | Aislada | Frase |
|---|---|---|
| Para qué | **Entrenar** | **Evaluar** (WER) y calibrar umbrales |
| Cuántas señas | Una | Varias |
| Entra al entrenamiento | Sí | **Nunca** |

Con `n` señas aprendidas se traduce cualquier combinación de ellas; entrenar con
frases enteras exigiría un dataset imposible.

---

## 🔍 Qué tienen los archivos de configuración

### `pyproject.toml`

| Sección | Contenido |
|---|---|
| `[project]` | `signia-modelo`, Python ≥ 3.12, dependencia base `numpy` |
| `optional-dependencies` | `entrenamiento` (torch, onnx, onnxruntime) y `dev` (pytest) |
| `[tool.pytest.ini_options]` | `testpaths`, `pythonpath`, `-q --strict-markers` y los marcadores `torch` y `onnx` |

### `.gitignore`

| Ignora | Por qué |
|---|---|
| `data/` | El dataset crudo son cientos de MB: backup aparte (plan, Fase 8) |
| `artefactos/` | Pesos y manifiesto: se publican por la API, no por git |
| `__pycache__/`, `.pytest_cache/`, `*.egg-info/` | Cachés |

### `contrato.md`

Documento en prosa con el formato de transporte, el remuestreo, el tensor crudo,
las 128 features y —lo más útil— la tabla de **qué rompe qué**: qué cambios
obligan a regrabar, a reentrenar o a tocar el JS.

---

## 💡 Ejemplos de uso

```bash
# Instalar (Windows)
python -m venv venv
venv/Scripts/pip install -r requirements.txt

# Tests
venv/Scripts/python -m pytest                     # 187 tests
venv/Scripts/python -m pytest -m "not torch"      # 138, sin torch (~3 s)

# Regenerar los fixtures de conformidad JS <-> Python
venv/Scripts/python scripts/generar_fixtures.py
```

```python
from signia_modelo.aplicacion.preprocess import construir_entrada
from signia_modelo.infra.repo_ficheros import RepositorioMuestrasEnDisco

repo = RepositorioMuestrasEnDisco()            # usa DATOS_DIR o ./data
for muestra in repo.listar(tipo="aislada"):
    entrada = construir_entrada(muestra)       # lm (48,2,21,3) + presencia (48,2)

repo.etiquetas()                               # ['hola', 'reposo', …] → n_clases
```

---

## 📈 Estado

- [x] **Fase 0** — contrato, remuestreo, tensor crudo, normalización en el grafo ONNX, repositorio y tests.
- [x] **Fase 1** — captura en el front (`front/app/src/`, capas dominio/aplicacion/infra/presentacion).
- [ ] **Fase 2** — dataset (aisladas + `reposo` + frases de evaluación).
- [ ] **Fase 3** — baseline DTW + k-NN, para medir si las clases son separables.
- [ ] **Fase 4** — modelo, WER por frase y artefacto con `manifest.json`.
