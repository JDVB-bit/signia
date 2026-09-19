# 🤟 SignIA — Traductor de Lengua de Signos Española con IA

> **Manos que hablan. Tecnología que escucha.**

## 📖 Introducción

**SignIA** traduce **frases en LSE** hechas delante de la cámara a **texto en
español**, directamente en el navegador: sin instalar nada, sin registro y sin
intérprete presente.

No es un modelo, son **dos etapas** con responsabilidades separadas:

```
vídeo ──► ETAPA 1: reconocimiento ──► glosas ──► ETAPA 2: redacción ──► texto
          modelo propio (ONNX)        ["hola","como","estar","tu"]   LLM en el backend
          corre en el navegador                                      "Hola, ¿cómo estás?"
```

- 🧠 El modelo aprende **señas**, nunca frases: con `n` señas se traduce cualquier
  combinación de ellas.
- 🗂️ Los **landmarks crudos** de MediaPipe son la fuente de verdad; todo lo demás
  (features, pesos, métricas) es derivado y reconstruible.

---

## 📂 Qué carpetas tiene el repositorio

| Carpeta | Qué es | Estado |
|---|---|---|
| [`front/`](front/) | Web en React: Inicio, Entrenamiento (captura de muestras) y Traductor | ✅ Captura funcionando |
| [`model/`](model/) | Paquete Python: contrato, preprocesado, normalización ONNX, dataset e inspector | ✅ Fases 0 y 1; Fase 2 en curso |
| [`back/`](back/) | API FastAPI: muestras, modelos y redacción | 🟢 Recibe muestras (`POST /muestras`) |
| [`.claude/`](.claude/) | Reglas del proyecto, plan de implementación y lista de mejoras | 📘 Documentación |

| Archivo raíz | Para qué sirve |
|---|---|
| `README.md` | Este documento: puerta de entrada al proyecto |
| `.gitignore` | Ignora dependencias, builds, entornos, logs y notas de borrador |

---

## 🔁 El bucle de captura, hoy

```
[Entrenamiento]  grabas la seña
      │
      ▼  "Enviar"
  POST /muestras ──► valida el lote entero ──► model/data/crudo/...   ✅
      │                                              │
      │ (si el backend no responde)                  ▼
      └─► descarga el JSON ─► scripts/importar_lote.py
                                                inspeccionar.py  ✅ ¿ya se puede entrenar?
                                                     │
                                                     ▼  ⛔ falta train.py (Fase 4)
                                             artefacto .onnx + métricas
```

Lo que falta para cerrar el reentrenamiento completo es el **entrenador**
(`model/train.py`) y, encima de él, `POST /entrenamientos`.

---

## 🎯 Qué problema resuelve

Una persona sorda y una oyente que no conoce LSE **no pueden conversar sin un
intérprete**. SignIA quita esa dependencia: se abre una página web, se hace la
seña frente a la cámara y aparece el texto.

Problemas técnicos concretos que resuelve el repositorio:

1. 🎥 **Capturar señas** de forma barata y reproducible: landmarks, no vídeo.
2. 🔒 **Que el navegador y el entrenamiento vean el mismo tensor**, mediante un
   contrato de datos y un test de conformidad entre JavaScript y Python.
3. 📦 **No perder nunca el dato crudo**, que es lo único irrecuperable.
4. ⚡ **Traducir sin servidor**: la inferencia corre en el navegador, así que el
   vídeo nunca sale del dispositivo.

---

## 🔗 Qué dependencias tiene

| Entorno | Necesita | Para qué |
|---|---|---|
| Front | Node.js 24 LTS + pnpm 11 | React 19, Vite 8, Tailwind v4, MediaPipe |
| Modelo | Python ≥ 3.12 | numpy (siempre); torch + ONNX solo para entrenar y exportar |
| Backend | Python ≥ 3.12 | FastAPI, Pydantic, uvicorn y el paquete `model` instalado en editable |
| Despliegue | Docker (opcional) | Front estático detrás de nginx |

Cada carpeta declara las suyas: [`front/app/package.json`](front/app/package.json),
[`model/pyproject.toml`](model/pyproject.toml),
[`model/requirements.txt`](model/requirements.txt),
[`back/requirements.txt`](back/requirements.txt).

---

## 🧠 Cómo lo resuelve

1. **MediaPipe HandLandmarker** extrae 21 puntos por mano, en el navegador.
2. El front los empaqueta como **muestra cruda** del contrato (`schema: 1`), sin
   normalizar.
3. El **remuestreo temporal** lleva la grabación a `T = 48` frames fijos. Es la
   única pieza escrita dos veces (JS y Python), y un **test de conformidad**
   sobre fixtures compartidos garantiza que ambas calculan lo mismo a `1e-5`.
4. La **normalización viaja dentro del grafo ONNX**, no en JS ni en Python: así
   entrenamiento e inferencia ejecutan literalmente el mismo código.
5. El modelo recibe `(48, 128)` y emite glosas; la etapa 2 las redacta.

### 📐 Principios de desarrollo

- **SOLID** y **Clean Architecture** en front y modelo (capas
  `dominio → aplicacion → infra → presentacion`).
- **Un archivo = una responsabilidad**, indicada en su nombre.
- **Conventional Commits** atómicos: cada commit compila y pasa los tests.
- Un `README.md` en **cada** directorio.

Detalle en [`.claude/claude.md`](.claude/claude.md) y [`.claude/rules.md`](.claude/rules.md).

---

## 🔍 Qué hay en cada parte

| Parte | Contenido destacable |
|---|---|
| `front/app/src/dominio/` | Contrato en JS, reglas de grabación, elección de mano |
| `front/app/src/aplicacion/` | Remuestreo, tensor crudo, creación de muestras y lotes |
| `front/app/src/infra/` | MediaPipe, canvas y APIs del navegador |
| `front/app/src/presentacion/` | Páginas, componentes, hooks, estados y textos |
| `model/signia_modelo/dominio/` | Constantes del contrato, entidades inmutables y puertos |
| `model/signia_modelo/aplicacion/` | Remuestreo y construcción del tensor |
| `model/signia_modelo/infra/` | JSON, dataset en disco, normalización torch y ONNX |
| `model/tests/` | 379 tests, incluidos los fixtures de conformidad |

**Estado de los tests:** 166 en el front (Vitest), 379 en el modelo (pytest;
353 sin torch) y 26 en el backend (pytest + TestClient).

---

## 💡 Ejemplos de uso

### Arranque rápido

```bash
# Front
cd front/app && pnpm install && pnpm dev          # http://localhost:5173

# Modelo (tests)
cd model && python -m venv venv && venv/Scripts/pip install -r requirements.txt
venv/Scripts/python -m pytest
```

### Grabar muestras de una seña

1. Abrir `/entrenamiento` y pulsar **Activar cámara**.
2. Escribir el nombre de la seña (por ejemplo, `hola`).
3. **Entrenar** → hacer la seña → **Detener**. El contador sube.
4. Repetir y pulsar **Enviar**: se descarga el lote en JSON.

### Leer ese lote desde Python

```python
import json
from signia_modelo.infra.json_contrato import muestra_desde_dict
from signia_modelo.aplicacion.preprocess import construir_entrada

paquete = json.load(open("signia-hola-2026-09-20-local.json", encoding="utf-8"))
for cruda in paquete["muestras"]:
    entrada = construir_entrada(muestra_desde_dict(cruda))
    print(entrada.lm.shape, entrada.presencia.shape)   # (48, 2, 21, 3) (48, 2)
```

---

## 📚 Documentación

Cada directorio tiene su propio `README.md` con la misma estructura. Además:

- [`model/contrato.md`](model/contrato.md) — **fuente de verdad** del formato de datos.
- [`.claude/plan-implementacion.md`](.claude/plan-implementacion.md) — plan por fases.
- [`.claude/mejoras.md`](.claude/mejoras.md) — historial y pendientes.

---

## 👥 Autoría

Proyecto académico de **Edy Avila**, **Juan Vieda** y **Andersson Castro**.
