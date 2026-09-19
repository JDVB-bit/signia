"""`GET /senas`: el vocabulario sale del dataset, nunca de una constante."""

from __future__ import annotations

from tests import factorias

RUTA = "/senas"
OK = 200


class TestVocabulario:
    def test_un_dataset_vacio_no_tiene_clases(self, cliente):
        datos = cliente.get(RUTA).json()
        assert datos == {"n_clases": 0, "senas": []}

    def test_cuenta_las_muestras_de_cada_sena(self, cliente, repo):
        for etiqueta in ("hola", "hola", "reposo"):
            repo.guardar(factorias.muestra(etiqueta))
        datos = cliente.get(RUTA).json()
        assert datos["n_clases"] == 2
        assert datos["senas"] == [
            {"etiqueta": "hola", "muestras": 2},
            {"etiqueta": "reposo", "muestras": 1},
        ]

    def test_las_frases_no_son_clases(self, cliente, repo):
        """Principio 6: la unidad de entrenamiento es la sena, nunca la frase."""
        repo.guardar(factorias.frase(("hola", "tu")))
        assert cliente.get(RUTA).json()["n_clases"] == 0

    def test_lo_que_se_sube_aparece_aqui(self, cliente, lote):
        """Es como el front confirmara que su envio llego."""
        cliente.post("/muestras", json=lote([factorias.muestra("comer")]))
        assert cliente.get(RUTA).json()["senas"] == [{"etiqueta": "comer", "muestras": 1}]
