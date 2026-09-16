# 🤟 SignIA — Traductor de Lengua de Signos Española con IA

> **Manos que hablan. Tecnología que escucha.**

SignIA traduce **frases en LSE** hechas delante de la cámara a **texto en español**, directamente en el navegador.

## 🧭 Cómo funciona (dos etapas)

```
vídeo ──► ETAPA 1: reconocimiento ──► glosas ──► ETAPA 2: redacción ──► texto
          modelo propio (ONNX)          ["hola","como","estar","tu"]   LLM en el backend
          corre en el navegador                                        "Hola, ¿cómo estás?"
```

- 🧠 El modelo aprende **señas**, nunca frases: con `n` señas se traduce cualquier combinación.
- 🗂️ Los **landmarks crudos** de MediaPipe son la fuente de verdad; todo lo demás se reconstruye.

## 📁 Estructura del repositorio

| Carpeta | Qué es | Estado |
|---|---|---|
| [`front/`](front/) | Web en React: Inicio, Entrenamiento (captura de muestras) y Traductor | ✅ Captura funcionando |
| [`model/`](model/) | Paquete Python del modelo: contrato, preprocesado, ONNX | ✅ Fase 0 completa |
| [`back/`](back/) | API FastAPI: muestras, modelos y redacción | 🕒 Pendiente (Fase 5) |
| [`.claude/`](.claude/) | Reglas del proyecto, plan de implementación y mejoras | 📘 Documentación |

## 🚀 Arranque rápido

```bash
# Front
cd front/app && pnpm install && pnpm dev          # http://localhost:5173

# Modelo (tests)
cd model && python -m venv venv && venv/Scripts/pip install -r requirements.txt
venv/Scripts/python -m pytest
```

## 📐 Principios de desarrollo

- **SOLID** y **Clean Architecture** en front y modelo (capas `dominio → aplicacion → infra → presentacion`).
- **Un archivo = una responsabilidad**, indicada en su nombre.
- **Conventional Commits** atómicos: cada commit compila y pasa los tests.
- Un `README.md` en cada directorio.

Detalle en [`.claude/claude.md`](.claude/claude.md) y [`.claude/rules.md`](.claude/rules.md).

## 👥 Autoría

Proyecto académico de **Edy Avila**, **Juan Vieda** y **Andersson Castro**.
