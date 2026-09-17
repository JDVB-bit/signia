# 🎯 `dominio/` — Núcleo sin dependencias

## 📖 Introducción

La capa más interna del paquete. **Python puro**: ni numpy, ni torch, ni
ficheros, ni red. Define qué es una muestra, qué valores fija el contrato y qué
interfaces necesita el sistema.

Todo lo demás depende de aquí; aquí no se depende de nada.

---

## 📂 Qué archivos y carpetas tiene

| Elemento | Responsabilidad |
|---|---|
| `contrato.py` | 📜 Constantes del contrato: `SCHEMA`, `T = 48`, `F = 128`, índices de muñeca y nudillo, rango de `score`… |
| `errores.py` | 🚨 Jerarquía de errores: `ErrorDeSignia` → `ErrorDeContrato`, `ErrorDeRemuestreo` |
| [`entidades/`](entidades/) | 🧩 `Lado`, `Mano`, `Frame`, `Muestra`, `MuestraAislada`, `MuestraFrase` |
| [`puertos/`](puertos/) | 🔌 Interfaces `Remuestreador`, `LectorMuestras`, `EscritorMuestras`, `RepositorioMuestras` |
| `__init__.py` | Documenta la capa |

---

## 🎯 Qué problema resuelve

1. **Que el contrato tenga un único sitio.** `T = 48` aparece en el remuestreo,
   en los tests, en los fixtures y en el grafo ONNX. Escrito una vez, cambiarlo
   es una decisión; escrito cinco veces, es un bug esperando.
2. **Que los datos inválidos no circulen.** Si existe una instancia de `Mano`,
   tiene 21 landmarks de 3 coordenadas y un `score` en rango. Las capas de
   arriba no vuelven a comprobarlo.
3. **Que las decisiones no dependan de la tecnología.** Cambiar disco por nube o
   torch por otra cosa no puede tocar esta carpeta.

---

## 🔗 Qué dependencias tiene

**Ninguna externa.** Solo biblioteca estándar: `dataclasses`, `enum`, `typing`.

Esa ausencia es un requisito, no una casualidad: permite importar el dominio
desde cualquier sitio (tests, backend, scripts) sin arrastrar numpy ni torch.

---

## 🧠 Cómo soluciona el problema

### 🛡️ Entidades inmutables y autovalidadas

```python
@dataclass(frozen=True, slots=True)
class Mano:
    ...
    def __post_init__(self) -> None:
        # valida y lanza ErrorDeContrato si algo no cumple
```

`frozen=True` impide mutarlas después de construirlas; `slots=True` reduce la
memoria, que importa cuando se cargan miles de muestras para entrenar.

### 🚨 Una jerarquía de errores, no excepciones sueltas

```
ErrorDeSignia
├── ErrorDeContrato     ← un dato crudo no cumple el contrato
└── ErrorDeRemuestreo   ← no se puede remuestrear (p. ej. 0 frames)
```

La API, los scripts y los tests pueden capturar `ErrorDeSignia` sin conocer el
detalle de quién lo lanzó.

### 🔌 Puertos como `Protocol`

Quien los implementa **no hereda de nada**: el repositorio de disco vive en
`infra/` y no importa el dominio para "ser" un repositorio. Eso es inversión de
dependencias de verdad, no herencia disfrazada.

---

## 🔍 Qué tienen los archivos

### `contrato.py`

| Grupo | Constantes |
|---|---|
| Versionado | `SCHEMA = 1`, `VERSION_PREPROCESADO = "1"` |
| Geometría | `N_LANDMARKS = 21`, `N_DIMS = 3`, `N_MANOS = 2`, `IDX_MUNECA = 0`, `IDX_NUDILLO_MEDIO = 9` |
| Confianza | `SCORE_MINIMO = 0.0`, `SCORE_MAXIMO = 1.0` |
| Ventana | `T = 48` (~1,6 s a 30 fps) |
| Features | `VALORES_PRESENCIA = 1`, `VALORES_POSICION = 2`, `VALORES_ESCALA = 1`, `VALORES_FORMA = 60`, `VALORES_POR_MANO = 64`, `F = 128` |
| Robustez | `EPS_ESCALA = 1e-6` |
| Vocabulario | `LADOS_CANONICOS = ("izquierda", "derecha")`, `TIPO_AISLADA`, `TIPO_FRASE` |

Todas son `Final`: el tipador avisa si alguien intenta reasignarlas.

### `errores.py`

Tres clases, sin lógica: la jerarquía es el mensaje.

---

## 💡 Ejemplos de uso

```python
from signia_modelo.dominio.contrato import F, T
from signia_modelo.dominio.errores import ErrorDeContrato

T, F        # (48, 128) → la entrada del modelo
```

```python
from signia_modelo.dominio.entidades import Frame, Lado, Mano, MuestraAislada

mano = Mano(lado=Lado.DERECHA, score=0.97, lm=[(0.1, 0.2, 0.0)] * 21)
muestra = MuestraAislada(frames=[Frame(t=0, manos=[mano])], sesion="2026-09-20-snt", etiqueta="hola")
muestra.glosas       # ('hola',)
```

```python
try:
    Mano(lado=Lado.DERECHA, score=1.5, lm=[(0, 0, 0)] * 21)
except ErrorDeContrato as error:
    print(error)     # score fuera de [0, 1]: 1.5
```

> ⚠️ Cambiar un valor de `contrato.py` **obliga a reentrenar** y a tocar
> `front/app/src/dominio/contrato.js` a la vez. Lo que nunca invalida es el
> dataset crudo ya grabado: por eso se guarda sin normalizar.
