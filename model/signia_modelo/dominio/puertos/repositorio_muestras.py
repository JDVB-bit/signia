"""🗄️ Puertos de persistencia del dataset crudo, sin saber donde vive."""

from __future__ import annotations

from typing import Iterator, Protocol, runtime_checkable

from ..entidades import Muestra


@runtime_checkable
class LectorMuestras(Protocol):
    """Lectura del dataset crudo, sin saber donde vive."""

    def listar(self, *, tipo: str | None = None, etiqueta: str | None = None) -> Iterator[Muestra]:
        """Recorre las muestras, opcionalmente filtradas por tipo o etiqueta."""
        ...

    def etiquetas(self) -> list[str]:
        """Clases presentes en el dataset, en orden estable.

        Forma parte del puerto y no del adaptador porque "que senas hay" es
        una pregunta del dominio: `n_clases` sale de aqui y nunca del codigo.
        """
        ...

    def contar(self) -> dict[str, int]:
        """Muestras por etiqueta. Recorrer el dataset entero para contarlo
        seria caro en cuanto crezca, asi que cada adaptador lo resuelve como
        pueda -en disco, contando ficheros; en una base de datos, con un
        COUNT-."""
        ...


@runtime_checkable
class EscritorMuestras(Protocol):
    """Escritura del dataset crudo, sin saber donde vive."""

    def guardar(self, muestra: Muestra) -> str:
        """Persiste la muestra y devuelve su identificador estable."""
        ...


@runtime_checkable
class RepositorioMuestras(LectorMuestras, EscritorMuestras, Protocol):
    """Puerto completo, para quien necesita las dos mitades."""
