# 🧪 `tests/` — La suite de la API

## 📖 Introducción

**26 tests** que levantan la aplicación entera con el `TestClient` de FastAPI y
la ejercitan por HTTP. Tardan menos de un segundo y **ninguno escribe en el
dataset real**.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Qué cubre |
|---|---|
| `test_muestras.py` | `POST /muestras`: lo que sube acaba en el dataset, y un lote malo no entra a medias |
| `test_senas.py` | `GET /senas`: el vocabulario sale del dataset; las frases no son clases |
| `test_salud.py` | `GET /salud`: versión del contrato y dataset escribible |
| `test_cors.py` | Que el navegador pueda hacer el `POST` desde el front |
| `conftest.py` | App, cliente y repositorio sobre `tmp_path` |
| `factorias.py` | Muestras mínimas válidas para cruzar la frontera HTTP |

---

## 🎯 Qué problema resuelve

El backend es el único sitio por donde el dataset puede **ensuciarse desde
fuera**. Estos tests fijan las dos garantías que lo impiden:

1. **Lo que entra cumple el contrato** — un lote con una muestra mala se rechaza
   entero, con un 422 que dice cuál y por qué.
2. **Lo que entra se guarda de verdad** — no basta con responder `201`: los
   tests vuelven a leer el repositorio y comprueban que está.

Y una tercera, menos obvia: **CORS**. Sin él todo funciona con `curl` y nada
funciona desde el navegador, que es el único cliente real.

---

## 🔗 Qué dependencias tiene

| Dependencia | Para qué |
|---|---|
| `pytest` | Ejecutar |
| `httpx` | Lo usa el `TestClient` de FastAPI por debajo |
| `signia_modelo` | Construir muestras válidas y leer el repositorio |

---

## 🧠 Cómo soluciona el problema

### 🧪 Un dataset de usar y tirar por test

```python
aplicacion.dependency_overrides[repositorio] = lambda: repo   # sobre tmp_path
```

Es posible **porque las rutas piden el repositorio por inyección**. Si lo
construyeran ellas, la suite escribiría en `./data`.

### 🏭 Fábricas propias, no las del modelo

`factorias.py` no reutiliza las del paquete `model`: allí la mano canónica
existe para que los tensores de los fixtures sean exactos, y aquí solo hace
falta un cuerpo válido. Atarse a aquella mano haría que un cambio pensado para
el preprocesado rompiera estos tests sin motivo.

### 🔁 Se comprueba el efecto, no la respuesta

```python
cliente.post("/muestras", json=lote([...]))
assert repo.contar() == {"hola": 2}
```

Un `201` solo dice que el servidor no se cayó.

---

## 💡 Ejemplos de uso

```bash
cd back
venv/Scripts/python -m pytest              # los 26
venv/Scripts/python -m pytest -k muestras  # solo el endpoint de subida
venv/Scripts/python -m pytest -v           # leer los nombres
```

Un test nuevo empieza por la fixture `cliente`:

```python
def test_mi_endpoint(cliente, repo):
    respuesta = cliente.get("/mi-ruta")
    assert respuesta.status_code == 200
```
