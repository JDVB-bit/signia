# 🎯 `dominio/` — Qué entra y qué sale de la API

## 📖 Introducción

Los contratos **de la API**, que no son el contrato **de los datos**. Aquí se
describe la forma de las peticiones y las respuestas HTTP; qué es una muestra
válida lo define [`model/contrato.md`](../../../model/contrato.md) y lo verifica
el paquete del modelo.

---

## 📂 Qué archivos y carpetas tiene

| Elemento | Qué es |
|---|---|
| [`esquemas/`](esquemas/) | 📐 Un modelo Pydantic por recurso |

---

## 🎯 Qué problema resuelve

Que la API tenga documentación automática y respuestas tipadas **sin reescribir
el contrato de datos**. Si las muestras se describieran aquí con Pydantic habría
dos definiciones de lo mismo, y con el tiempo dirían cosas distintas — que es
justo lo que el test de contrato cruzado JS ↔ Python existe para impedir.

---

## 🔗 Qué dependencias tiene

`pydantic` v2. Nada más: estos modelos no llaman a nadie.

---

## 🧠 Cómo soluciona el problema

La frontera se parte en dos:

| Quién valida | Qué |
|---|---|
| Pydantic (aquí) | Que el cuerpo sea un sobre con `schema` y una lista no vacía |
| `signia_modelo` | Que cada muestra cumpla el contrato de datos |

Así un error de forma sale como el 422 estándar de FastAPI y un error de
contrato sale con el mensaje del modelo, que dice la posición exacta dentro del
lote.

---

## 💡 Ejemplos de uso

```python
from app.dominio.esquemas import LoteEntrante

lote = LoteEntrante(schema=1, muestras=[{"etiqueta": "hola", "frames": []}])
lote.como_dict()   # el dict original, para el validador del contrato
```
