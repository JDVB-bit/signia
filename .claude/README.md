# 📘 `.claude/` — Reglas, plan y seguimiento del proyecto

## 📖 Introducción

Esta carpeta **no contiene código de la aplicación**: contiene las reglas con las
que se escribe ese código, el plan por fases y el historial de decisiones. Es lo
primero que hay que leer antes de tocar `front/`, `model/` o `back/`.

Guía también al asistente de IA que participa en el desarrollo.

---

## 📂 Qué archivos tiene y qué hace cada uno

| Archivo | Para qué sirve |
|---|---|
| `claude.md` | 🧭 **Reglas fundamentales**: rol del asistente, lista viva de mejoras, SOLID, Clean Architecture, visión de producto |
| `rules.md` | 📏 **Reglas de código**: buenas prácticas, README por directorio, estilo de comentarios, sin números mágicos, commits atómicos |
| `guia_docs.md` | 📝 **Formato de los README**: qué secciones lleva cada uno y cómo se presentan |
| `plan-implementacion.md` | 🗺️ **Plan por fases** (0 → 8) del modelo, el backend y el traductor, con los principios no negociables |
| `mejoras.md` | ✅ **Lista viva** de lo hecho por sesión, lo pendiente y las ideas futuras |
| `launch.json` | ▶️ Cómo arrancar el servidor de desarrollo del front desde el editor |

---

## 🎯 Qué problema resuelve

Un proyecto largo **pierde el porqué de sus decisiones**. Sin este registro:

- Se reescribe algo que ya se había descartado, con los mismos argumentos.
- Se cambia una constante sin saber que invalida el dataset o el modelo.
- Cada sesión de trabajo empieza reconstruyendo el contexto desde cero.

Aquí viven esas razones, fuera del código y sin caducar con él.

---

## 🔗 Qué dependencias tiene

Ninguna: son documentos Markdown y un JSON de configuración.

`launch.json` lo lee el entorno de desarrollo para levantar el front
(`pnpm --dir front/app run dev`, puerto `5173`).

---

## 🧠 Cómo soluciona el problema

### 🗂️ Un documento por tipo de decisión

| Pregunta | Documento |
|---|---|
| ¿Cómo trabajamos? | `claude.md` |
| ¿Cómo se escribe el código? | `rules.md` |
| ¿Cómo se documenta? | `guia_docs.md` |
| ¿Qué construimos y en qué orden? | `plan-implementacion.md` |
| ¿Qué se hizo y qué falta? | `mejoras.md` |

### 🧱 Principios no negociables

El plan los enumera y todo lo demás se resuelve contra ellos, no por gusto:

1. Los **landmarks crudos** son la fuente de verdad.
2. El preprocesado existe **una sola vez** (la normalización va dentro del ONNX).
3. El entrenamiento es un **job por lotes**, nunca un paso dentro de un request.
4. Un modelo nuevo **no reemplaza** al activo si sus métricas son peores.
5. La persistencia va **detrás de una interfaz**.
6. El modelo aprende **señas**, nunca frases.
7. La métrica que manda es el **WER sobre glosas**.

### 🔁 Un ciclo de trabajo explícito

1. Antes de programar: leer `claude.md`, `rules.md` y la fase actual del plan.
2. Al terminar: anotar lo hecho y lo pendiente en `mejoras.md`.
3. Al crear una carpeta: escribir su `README.md` siguiendo `guia_docs.md`.

---

## 🔍 Qué tienen los archivos

### `plan-implementacion.md`

De la Fase 0 (contrato) a la Fase 8 (robustez), más el roadmap v2 (del umbral a
CTC), cómo escalar a `n` señas y la independencia del despliegue. Cada fase lista
sus **ficheros** y sus **decisiones tomadas**.

### `mejoras.md`

Un bloque por sesión (`## Hecho (sesión N)`), seguido de *Pendiente / próximos
pasos* e *Ideas futuras*. Es el historial de cómo llegó el proyecto hasta aquí.

### `guia_docs.md`

Las siete secciones de un README (introducción, archivos, problema,
dependencias, solución, contenido de los archivos, ejemplos) y la indicación de
usar títulos, separadores visuales y emojis.

### `launch.json`

```json
{ "name": "signia-front", "runtimeExecutable": "pnpm",
  "runtimeArgs": ["--dir", "front/app", "run", "dev"], "port": 5173 }
```

---

## 💡 Ejemplos de uso

```bash
# Los principios de diseño, antes de tocar el preprocesado
sed -n '/## Principios de diseño/,/^---/p' .claude/plan-implementacion.md

# Qué queda pendiente
sed -n '/## Pendiente/,$p' .claude/mejoras.md
```

Al cerrar una sesión de trabajo se añade un bloque a `mejoras.md`:

```markdown
## Hecho (sesión N) — título corto
- [x] Qué se hizo y por qué.
```
