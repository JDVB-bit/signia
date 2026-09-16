# 🛠️ `scripts/` — Utilidades de línea de comandos

| Script | Qué hace |
|---|---|
| `generar_fixtures.py` | Regenera `tests/fixtures/*.json`: muestras límite + el tensor que produce Python |

```bash
cd model
venv/Scripts/python scripts/generar_fixtures.py
```

⚠️ Regenerar los fixtures solo cuando cambie **a propósito** el preprocesado; después, el test de conformidad de JS debe seguir pasando.
