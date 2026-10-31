import json
import unittest
from unittest.mock import patch

from src.interpretacao_llm import gerar_interpretacao, gerar_interpretacao_ollama, montar_prompt


RESUMO = {
    "modelo": "Arvore de Decisao",
    "hiperparametros": {"max_depth": 5},
    "accuracy": 0.65,
    "recall": 0.88,
    "f1_score": 0.73,
}


class InterpretacaoLlmTest(unittest.TestCase):
    def test_prompt_contem_apenas_resumo_agregado(self):
        prompt = montar_prompt(RESUMO)

        self.assertIn("Arvore de Decisao", prompt)
        self.assertIn("0.88", prompt)

    def test_modo_demonstracao_nao_precisa_de_chave(self):
        resposta = gerar_interpretacao(RESUMO)

        self.assertEqual(resposta.modo, "demonstracao")
        self.assertIn("DEMONSTRACAO LOCAL", resposta.texto)
        self.assertIn("revisao humana", resposta.texto)

    @patch("src.interpretacao_llm.urllib_request.urlopen")
    def test_ollama_retorna_texto_do_modelo_local(self, urlopen):
        class RespostaFalsa:
            def read(self):
                return json.dumps({"response": "Explicacao local."}).encode("utf-8")

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

        urlopen.return_value = RespostaFalsa()
        resposta = gerar_interpretacao_ollama(RESUMO)

        self.assertEqual(resposta.modo, "ollama_local")
        self.assertEqual(resposta.texto, "Explicacao local.")


if __name__ == "__main__":
    unittest.main()
