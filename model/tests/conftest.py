"""Configuracion comun de los tests."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:  # permite ejecutar pytest sin instalar el paquete
    sys.path.insert(0, str(RAIZ))

from tests import factorias  # noqa: E402


@pytest.fixture
def muestra_aislada():
    return factorias.muestra()


@pytest.fixture
def muestra_frase():
    return factorias.frase()


@pytest.fixture
def repo_vacio(tmp_path):
    from signia_modelo.infra.repo_ficheros import RepositorioMuestrasEnDisco

    return RepositorioMuestrasEnDisco(tmp_path)
