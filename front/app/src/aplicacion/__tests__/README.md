# 🧪 `aplicacion/__tests__/` — Tests del preprocesado

## 📖 Introducción

Tests de la capa de aplicación. Aquí está **el test más importante del
repositorio**: el de conformidad, que compara lo que calcula el navegador con lo
que calcula Python usando los mismos ficheros de referencia.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Qué verifica |
|---|---|
| `conformidad.test.js` | ⭐ Lee los fixtures de `model/tests/fixtures/` y exige que JS y Python produzcan **los mismos índices y tensores** (a `1e-5`) |
| `remuestreo.test.js` | Longitud `T`, extremos conservados, monotonía, identidad, redondeo hacia arriba, errores |
| `construirEntrada.test.js` | Ranuras fijas, mano ausente en ceros, orden temporal preservado |
| `crearMuestra.test.js` | Formato del contrato, reindexado de `t`, validaciones que lanzan |
| `fpsDeGrabacion.test.js` | Cálculo de fps y duración inválida (`null`) |
| `sesionDeGrabacion.test.js` | Formato `AAAA-MM-DD-dispositivo` |
| `paqueteDeMuestras.test.js` | Envoltorio con `schema` y nombre del fichero (lote simple y mixto) |

---

## 🎯 Qué problema resuelve

**La deriva silenciosa.** Si el preprocesado del navegador y el del
entrenamiento dejan de coincidir, no hay error visible: el modelo simplemente
acierta menos, y el bug se descubre semanas después del entrenamiento.

Estos tests convierten ese fallo invisible en un fallo rojo e inmediato.

---

## 🔗 Qué dependencias tiene

- `vitest` en entorno **node**.
- `node:fs` y `node:url` para leer los fixtures.
- 📁 **`model/tests/fixtures/*.json`** — generados por
  `model/scripts/generar_fixtures.py`. Es la única dependencia entre las dos
  mitades del proyecto.

---

## 🧠 Cómo soluciona el problema

```
Python                                        JavaScript
──────                                        ──────────
construir_entrada(muestra)                    construirEntrada(muestra)
        │                                             │
        └──────► model/tests/fixtures/*.json ◄────────┘
                 muestra cruda + índices + presencia + lm
                 verificados a 1e-5 por AMBOS lados
```

Seis casos límite, elegidos porque son donde el remuestreo se rompe:

| Fixture | Qué pone a prueba |
|---|---|
| `un_frame` | Una grabación de un solo frame se repite 48 veces |
| `corta_12` | Faltan frames: hay que repetir sin saltarse ninguno |
| `exacta_48` | Longitud exacta: debe ser la identidad |
| `larga_120` | Sobran frames: reparto uniforme sin tirones |
| `sin_manos` | Presencia `0` en todo el tensor |
| `intermitente` | Manos que entran, salen y cambian de lado |

---

## 🔍 Qué tienen los archivos

`conformidad.test.js` comprueba, por cada fixture:

1. Que declara la misma `T` que este código.
2. Que `indicesRemuestreo` elige **exactamente** los mismos índices que Python.
3. Que la `presencia` coincide **valor a valor** (es binaria: no admite tolerancia).
4. Que los landmarks coinciden con diferencia máxima `< 1e-5`.
5. Que el tensor tiene la forma del contrato: `(48, 2, 21, 3)` y `(48, 2)`.

`remuestreo.test.js` incluye el caso que distingue los dos redondeos:

```js
it('redondea hacia arriba, como int(x+0.5) en Python', () => {
    // Con round() de Python (al par) saldría [0, 0, 1, 2, 2]
    expect(indicesRemuestreo(3, 5)).toEqual([0, 1, 1, 2, 2])
})
```

---

## 💡 Ejemplos de uso

```bash
pnpm test                      # toda la suite del front (166 tests, <1 s)
pnpm test -- conformidad       # solo el test de conformidad
```

Si tocas el preprocesado **a propósito**, el ciclo completo es:

```bash
cd model
venv/Scripts/python scripts/generar_fixtures.py     # regenerar la referencia
venv/Scripts/python -m pytest                       # 379 tests
cd ../front/app && pnpm test                        # 166 tests
```

> 🚨 Si la conformidad falla **no regeneres los fixtures sin pensar**. Significa
> que los tensores han cambiado: hay que **reentrenar** el modelo y actualizar
> los dos lados a la vez. La red tiene dientes — cambiar `Math.round` por
> `Math.floor` tumba la suite entera.
