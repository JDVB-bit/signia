# 📦 `signia_modelo/` — Paquete Python del modelo

## 📖 Introducción

El paquete instalable que implementa la **etapa 1** de SignIA: convertir
landmarks de MediaPipe en glosas. Hoy contiene el contrato de datos, el
preprocesado, la normalización exportable a ONNX y el repositorio del dataset;
el modelo entrenado llegará en la Fase 4.

Está organizado en **tres capas de Clean Architecture**, y la regla es una sola:
*nadie de dentro importa nada de fuera*.

---

## 📂 Qué carpetas y archivos tiene

| Capa | Carpeta | Depende de | Contiene |
|---|---|---|---|
| 🎯 Dominio | [`dominio/`](dominio/) | nada | contrato, entidades, errores, puertos |
| ⚙️ Aplicación | [`aplicacion/`](aplicacion/) | dominio + numpy | remuestreo y construcción del tensor |
| 🔌 Infraestructura | [`infra/`](infra/) | todo + frameworks | JSON, disco, torch, ONNX |

| Archivo | Qué hace |
|---|---|
| `__init__.py` | Documenta las capas y reexporta `contrato` para acceso rápido |

---

## 🎯 Qué problema resuelve

1. **Que el proyecto sobreviva a sus decisiones.** Hoy el dataset está en disco
   y el entrenamiento en torch; mañana podrían ser otra cosa. Con capas, eso es
   sustituir un adaptador.
2. **Que el contrato no se disperse.** Front, backend y entrenamiento hablan del
   mismo formato porque hay **un** módulo que lo define.
3. **Que se pueda probar sin GPU.** 161 de los 187 tests no necesitan torch.
4. **Que el backend no cargue con el peso del entrenamiento.** El paquete
   funciona con solo `numpy`; torch y ONNX son extras opcionales.

---

## 🔗 Qué dependencias tiene

| Dependencia | Cuándo hace falta |
|---|---|
| Python ≥ 3.12 | Siempre |
| `numpy >= 2.0` | Siempre (capa de aplicación) |
| `torch`, `onnx`, `onnxruntime` | Extra `entrenamiento`: entrenar y exportar |
| `pytest` | Extra `dev` |

Declaradas en [`../pyproject.toml`](../pyproject.toml) y fijadas en
[`../requirements.txt`](../requirements.txt).

---

## 🧠 Cómo soluciona el problema

### 🧅 La regla de dependencia

```
        infra/  ──►  aplicacion/  ──►  dominio/
     (frameworks)      (numpy)        (python puro)
```

Las flechas van **hacia dentro**. El dominio no sabe que existen los ficheros, ni
torch, ni la API. Consecuencias prácticas:

- El dominio se importa desde cualquier sitio sin arrastrar dependencias.
- Cambiar disco por almacenamiento en nube es escribir otro adaptador en
  `infra/`, sin tocar el resto.
- Los tests de dominio y aplicación corren en segundos.

### 🧬 Gemelo del front

| Capa aquí | Capa gemela en el front |
|---|---|
| `dominio/contrato.py` | `src/dominio/contrato.js` |
| `aplicacion/remuestreo.py` | `src/aplicacion/remuestreo.js` |
| `aplicacion/preprocess.py` | `src/aplicacion/construirEntrada.js` |

Los dos lados se verifican contra los **mismos fixtures**. Es la única forma de
que el navegador y el entrenamiento no diverjan en silencio.

---

## 🔍 Qué tiene el archivo raíz

### `__init__.py`

Documenta las tres capas y reexporta el módulo `contrato`, que es lo que más se
consulta desde fuera:

```python
from .dominio import contrato as contrato
__all__ = ["contrato"]
```

---

## 💡 Ejemplos de uso

```python
from signia_modelo import contrato

contrato.T, contrato.F          # (48, 128) → la entrada del modelo
contrato.SCHEMA                 # 1
```

```python
from signia_modelo.aplicacion.preprocess import construir_entrada
from signia_modelo.infra.repo_ficheros import RepositorioMuestrasEnDisco

repo = RepositorioMuestrasEnDisco()              # DATOS_DIR o ./data
for muestra in repo.listar(tipo="aislada"):
    entrada = construir_entrada(muestra)         # lm (48,2,21,3) + presencia (48,2)
```

```bash
# Instalación en desarrollo, con lo necesario para entrenar
venv/Scripts/pip install -e ".[entrenamiento,dev]"
```

> 📌 Al añadir código, la pregunta es siempre la misma: *¿esto seguiría siendo
> verdad si cambiáramos de framework o de almacenamiento?* Si sí, va al dominio;
> si no, a `infra/`.
