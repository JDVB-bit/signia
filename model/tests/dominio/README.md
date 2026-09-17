# 🧪 `tests/dominio/` — Tests de las entidades

## 📖 Introducción

Verifican que las entidades **se validan a sí mismas**: que ninguna instancia
puede existir incumpliendo el contrato, que son inmutables y que la regla de las
manos duplicadas es determinista.

24 tests, sin dependencias externas: son los más rápidos de la suite.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Qué verifica |
|---|---|
| `test_entidades.py` | `Lado`, `Mano`, `Frame`, `MuestraAislada` y `MuestraFrase`: validaciones, inmutabilidad y desempate por `score` |
| `__init__.py` | Hace de la carpeta un paquete de tests |

Organizado en clases (`TestLado`, `TestMano`, `TestFrame`, `TestMuestra`) para
que el informe de pytest se lea como un índice del dominio.

---

## 🎯 Qué problema resuelve

Las entidades son **la primera línea de defensa del dataset**. Si `Mano` aceptara
19 landmarks, ese dato llegaría al tensor, se entrenaría con él y el fallo
aparecería como "el modelo acierta poco", sin ninguna pista.

Estos tests fijan que:

- Lo inválido **lanza en el constructor**, no más tarde.
- El mensaje del error dice **qué** está mal y **dónde** (`landmark 7`).
- Nadie puede modificar una muestra después de crearla.

---

## 🔗 Qué dependencias tiene

- `pytest`.
- `signia_modelo.dominio` (entidades, contrato y errores).
- `tests.factorias` para construir manos y muestras válidas.

Ni numpy, ni torch, ni disco.

---

## 🧠 Cómo soluciona el problema

### ❌ Probar lo que debe fallar

La mitad de los tests comprueban rechazos, con `pytest.raises` y el mensaje
esperado:

```python
@pytest.mark.parametrize("n", [0, 20, 22])
def test_rechaza_numero_de_landmarks_incorrecto(self, n):
    with pytest.raises(ErrorDeContrato, match="landmarks"):
        Mano(Lado.DERECHA, 1.0, [(0, 0, 0)] * n)
```

Comprobar el `match` evita el falso positivo clásico: que el test pase porque
saltó **otro** error distinto.

### 🔒 Inmutabilidad comprobada

```python
with pytest.raises(dataclasses.FrozenInstanceError):
    mano.score = 0.1
```

### ⚖️ Desempate en los dos órdenes

La regla se prueba con las manos en un orden y en el contrario, para garantizar
que gana el `score` y no la posición en la lista.

---

## 🔍 Qué tienen los archivos

| Clase | Casos destacados |
|---|---|
| `TestLado` | Texto válido → `Lado`; texto inválido → error que enumera los válidos |
| `TestMano` | Normaliza a tuplas de `float`; acepta el lado como texto; rechaza landmarks y `score` fuera de contrato; es inmutable |
| `TestFrame` | Sin manos → `None`; devuelve la mano del lado pedido; gana el mayor `score`; rechaza `t` negativo |
| `TestMuestra` | `tipo` y `glosas` de aislada y frase; rechaza sin frames, sin sesión, con `schema` desconocido, con `fps` no positivo, sin etiqueta(s) |

---

## 💡 Ejemplos de uso

```bash
venv/Scripts/python -m pytest tests/dominio -v
venv/Scripts/python -m pytest tests/dominio -k "score"
```

```python
# Patrón que siguen estos tests
def test_rechaza_muestra_sin_sesion():
    with pytest.raises(ErrorDeContrato, match="sesion"):
        MuestraAislada(frames=(Frame(0),), sesion="", etiqueta="hola")
```

> 💡 Al añadir una validación a una entidad, el test va aquí **antes** que el
> código: es la forma más rápida de comprobar que el mensaje de error resulta
> accionable para quien lo lea en producción.
