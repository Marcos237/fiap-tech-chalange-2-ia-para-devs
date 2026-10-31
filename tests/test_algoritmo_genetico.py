import unittest
from random import Random

from src.algoritmo_genetico import (
    ConfiguracaoAG,
    criar_individuo,
    crossover_uniforme,
    executar_ag,
    mutar,
)


ESPACO = {"a": [1, 2, 3], "b": ["x", "y"]}


class AlgoritmoGeneticoTest(unittest.TestCase):
    def test_individuo_e_mutacao_respeitam_espaco_de_busca(self):
        rng = Random(42)
        individuo = criar_individuo(ESPACO, rng)
        mutante = mutar(individuo, ESPACO, 1.0, rng)

        self.assertTrue(all(mutante[gene] in valores for gene, valores in ESPACO.items()))

    def test_crossover_usa_genes_dos_pais(self):
        filho = crossover_uniforme({"a": 1, "b": "x"}, {"a": 3, "b": "y"}, Random(42))

        self.assertIn(filho["a"], [1, 3])
        self.assertIn(filho["b"], ["x", "y"])

    def test_elitismo_preserva_melhor_fitness_global(self):
        resultado = executar_ag(
            ConfiguracaoAG(tamanho_populacao=6, geracoes=4, elitismo=1, random_state=42),
            ESPACO,
            lambda individuo: individuo["a"],
        )

        melhores = [linha["melhor_fitness"] for linha in resultado.historico]
        self.assertEqual(resultado.melhor_fitness, max(melhores))
        self.assertEqual(resultado.melhor_individuo["a"], 3)


if __name__ == "__main__":
    unittest.main()
