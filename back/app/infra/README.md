# 🔌 `infra/` — Dónde vive el dataset

## 📖 Introducción

Los adaptadores del backend. Hoy hay uno solo, y es deliberadamente corto: el
repositorio del dataset **ya existe** en el paquete del modelo, y está probado.
Aquí se construye con la configuración del entorno, y nada más.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Responsabilidad |
|---|---|
| `repositorio_en_disco.py` | 🗂️ `repositorio_de(datos_dir)` y `es_escribible(raiz)` |

---

## 🎯 Qué problema resuelve

**No reescribir lo que ya está escrito.** El dataset en carpetas, el saneado de
etiquetas y el consecutivo de ficheros son del paquete del modelo. Si el backend
tuviera su propia versión, el script de consola y la API acabarían guardando
distinto.

Y un problema de operación: un permiso mal puesto o un disco lleno tiene que
verse en `GET /salud`, no al subir la primera tanda de 40 muestras.

---

## 🔗 Qué dependencias tiene

| Dependencia | Para qué |
|---|---|
| `signia_modelo.infra.repo_ficheros` | El adaptador de disco |
| `signia_modelo.dominio.puertos` | El tipo que se devuelve es el **puerto** |

---

## 🧠 Cómo soluciona el problema

`repositorio_de()` devuelve un `RepositorioMuestras`, no un
`RepositorioMuestrasEnDisco`: quien lo recibe no puede depender de que haya
carpetas debajo.

> El día que el dataset viva en almacenamiento de objetos, **cambia este archivo
> y ningún otro**.

`es_escribible()` comprueba creando la carpeta. Así responder `true` significa
de verdad que se puede escribir, y arrancar en una máquina limpia funciona sin
preparar nada a mano.

---

## 💡 Ejemplos de uso

```python
from pathlib import Path

from app.infra.repositorio_en_disco import es_escribible, repositorio_de

repo = repositorio_de("D:/signia-data")
repo.contar()                        # {"hola": 31, "reposo": 60}
es_escribible(Path("D:/signia-data"))
```
