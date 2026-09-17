# 📎 `tests/fixtures/` — Casos de conformidad JS ↔ Python

## 📖 Introducción

Seis ficheros JSON que son **la referencia compartida entre las dos mitades del
proyecto**. Cada uno contiene una muestra cruda y el tensor exacto que Python
produce a partir de ella.

Los lee `tests/test_conformidad.py` (Python) y también
`front/app/src/aplicacion/__tests__/conformidad.test.js` (JavaScript). Son el
único punto donde el modelo y el front se tocan directamente.

---

## 📂 Qué archivos tiene y qué caso cubre cada uno

| Fixture | Caso límite | Por qué está |
|---|---|---|
| `un_frame.json` | Una grabación de un solo frame | Se repite 48 veces: el caso degenerado |
| `corta_12.json` | Menos frames que `T` | Hay que repetir sin saltarse ninguno |
| `exacta_48.json` | Exactamente `T` frames | Debe ser la identidad |
| `larga_120.json` | Más frames que `T`, con dos manos | Se saltan frames; reparto uniforme |
| `sin_manos.json` | Ningún frame con manos | Todo ceros y presencia 0 |
| `intermitente.json` | La mano entra, cambia de lado y aparecen las dos | El caso realista más difícil |

---

## 🎯 Qué problema resuelve

**La deriva silenciosa.** El remuestreo está escrito dos veces —en Python para
entrenar y en JavaScript para inferir— y no hay ningún mecanismo del lenguaje
que garantice que calculan lo mismo.

Sin estos ficheros, una diferencia de redondeo no produciría ningún error: el
modelo simplemente acertaría menos, y el fallo se descubriría semanas después,
con el dataset ya grabado y el modelo ya entrenado.

---

## 🔗 Qué dependencias tiene

| Elemento | Relación |
|---|---|
| `scripts/generar_fixtures.py` | Los **genera** |
| `tests/test_conformidad.py` | Los verifica desde Python |
| `front/app/src/aplicacion/__tests__/conformidad.test.js` | Los verifica desde JavaScript |
| `tests/factorias.py` | La mano canónica con la que se construyen |

---

## 🧠 Cómo soluciona el problema

```
Python                                        JavaScript
──────                                        ──────────
construir_entrada(muestra)                    construirEntrada(muestra)
        │                                             │
        └──────► tests/fixtures/*.json ◄──────────────┘
                 verificados a 1e-5 por AMBOS lados
```

Ninguno de los dos lados confía en el otro: los dos comparan contra el mismo
fichero. Y el generador reutiliza las **fábricas de los tests**, para que la mano
canónica esté definida en un único sitio.

El test de Python comprueba además que el generador es **reproducible**:
regenerar sin tocar nada tiene que producir exactamente el mismo contenido.

---

## 🔍 Qué tienen los archivos

```json
{
  "nombre": "corta_12",
  "version_preprocesado": "1",
  "T": 48,
  "muestra":  { "schema": 1, "tipo": "aislada", "etiqueta": "hola", "frames": [ … ] },
  "esperado": {
    "indices":   [0, 0, 1, 1, 2, …],
    "presencia": [0, 1, 0, 1, …],
    "lm":        [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, …]
  }
}
```

| Campo | Contenido |
|---|---|
| `nombre` | Identifica el caso en el informe de los tests |
| `version_preprocesado` | Si cambia, los tensores ya no son comparables |
| `T` | Longitud de la ventana con la que se generó |
| `muestra` | Muestra cruda completa, en el formato del contrato |
| `esperado.indices` | Los `T` índices elegidos por el remuestreo |
| `esperado.presencia` | `(T, 2)` aplanado en orden C |
| `esperado.lm` | `(T, 2, 21, 3)` aplanado en orden C, redondeado a 6 decimales |

Los tensores van **aplanados** porque es como los produce `.ravel()` de numpy y
como los consume `Float32Array` en JavaScript: comparar es recorrer dos listas.

---

## 💡 Ejemplos de uso

```bash
# Regenerar (solo si el preprocesado cambió A PROPÓSITO)
venv/Scripts/python scripts/generar_fixtures.py

# Verificar los dos lados
venv/Scripts/python -m pytest tests/test_conformidad.py
cd ../front/app && pnpm test -- conformidad
```

> 🔁 **No se editan a mano.** Son salida de código, no dato de entrada.

> 🚨 Si el test de conformidad falla, la pregunta correcta no es *"¿cómo
> actualizo los fixtures?"* sino *"¿qué cambió en el preprocesado y qué implica?"*.
> La respuesta casi siempre incluye **reentrenar**.
