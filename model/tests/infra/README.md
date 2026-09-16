# 🧪 Tests de infraestructura

| Test | Qué verifica |
|---|---|
| `test_json_contrato.py` | Validación del JSON de entrada e ida y vuelta dict ↔ entidad |
| `test_ficheros_json.py` | Guardar/cargar en disco y errores que nombran el fichero |
| `test_repo_ficheros.py` | Saneado de rutas, guardado, listado, conteo y `DATOS_DIR` |
| `test_normalizacion_torch.py` | Invariancias de la forma, ceros exactos sin mano, sin `NaN` |
| `test_exportacion_onnx.py` | Paridad torch ↔ onnxruntime a 1e-5 con 0/1/2 manos y 1/12/48/120 frames |
