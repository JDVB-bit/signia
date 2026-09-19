"""Fixtures comunes: una app limpia por test y un dataset en `tmp_path`.

**Ningun test escribe en el dataset real.** El repositorio se sustituye por uno
sobre el directorio temporal de pytest, aprovechando que las rutas lo piden por
inyeccion en vez de construirlo ellas.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from signia_modelo.infra.json_lote import lote_desde_muestras
from signia_modelo.infra.repo_ficheros import RepositorioMuestrasEnDisco

from app.api.dependencias import repositorio
from app.config import Ajustes
from app.main import crear_app

#: Origen del front en desarrollo, para las pruebas de CORS.
ORIGEN_DE_PRUEBA = "http://localhost:5173"


@pytest.fixture
def raiz_de_datos(tmp_path):
    """Raiz aislada del dataset para este test."""
    return tmp_path / "datos"


@pytest.fixture
def repo(raiz_de_datos):
    return RepositorioMuestrasEnDisco(raiz_de_datos)


@pytest.fixture
def app(raiz_de_datos, repo):
    """Aplicacion con el dataset apuntando al temporal."""
    aplicacion = crear_app(
        Ajustes(datos_dir=str(raiz_de_datos), origenes_cors=(ORIGEN_DE_PRUEBA,))
    )
    aplicacion.dependency_overrides[repositorio] = lambda: repo
    return aplicacion


@pytest.fixture
def cliente(app):
    return TestClient(app)


@pytest.fixture
def lote():
    """Construye el cuerpo de `POST /muestras` a partir de entidades."""
    return lote_desde_muestras
