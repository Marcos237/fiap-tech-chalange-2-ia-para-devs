import unittest

import pandas as pd

from src.dados import COLUNAS_MODELO, dividir_e_imputar, limpar_base


def criar_base_minima() -> pd.DataFrame:
    linhas = []
    for indice in range(20):
        linha = {coluna: 1 for coluna in COLUNAS_MODELO}
        linha["CS_SEXO"] = "F"
        linha["OUT_VEZES"] = 1 if indice % 2 == 0 else 2
        linha["NU_IDADE_N"] = 30 if indice != 0 else 999
        linha["CS_RACA"] = 9 if indice == 1 else 1
        linhas.append(linha)
    return pd.DataFrame(linhas)


class LimpezaDadosTest(unittest.TestCase):
    def test_limpeza_mapeia_alvo_e_substitui_codigos_ignorados(self):
        base_limpa, _ = limpar_base(criar_base_minima())

        self.assertEqual(set(base_limpa["OUT_VEZES"].unique()), {0, 1})
        self.assertTrue(pd.isna(base_limpa.loc[1, "CS_RACA"]))
        self.assertTrue(pd.isna(base_limpa.loc[0, "NU_IDADE_N"]))

    def test_divisao_e_imputacao_nao_deixam_nulos(self):
        base_limpa, _ = limpar_base(criar_base_minima())
        dados = dividir_e_imputar(base_limpa, test_size=0.2, random_state=42)

        self.assertEqual(len(dados.X_train) + len(dados.X_test), len(base_limpa))
        self.assertFalse(dados.X_train.isna().any().any())
        self.assertFalse(dados.X_test.isna().any().any())
        self.assertEqual(set(dados.y_train.unique()), {0, 1})
        self.assertEqual(set(dados.y_test.unique()), {0, 1})


if __name__ == "__main__":
    unittest.main()
