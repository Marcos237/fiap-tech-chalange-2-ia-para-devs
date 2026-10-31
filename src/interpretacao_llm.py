"""Geracao segura de explicacoes agregadas para os resultados do modelo."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from typing import Any
from urllib import error as urllib_error
from urllib import request as urllib_request


INSTRUCOES = """Voce explica resultados de modelos de classificacao para profissionais humanos.
Use linguagem clara, cautelosa e objetiva. Nao faca diagnosticos, nao recomende acoes
para individuos e nao trate uma previsao como certeza. Explique que o modelo e apoio a
triagem e que decisao humana e obrigatoria. Baseie-se apenas nos numeros recebidos.
Se houver limitacoes, mencione-as."""


@dataclass(frozen=True)
class Interpretacao:
    """Resposta e metadados para auditoria da explicacao gerada."""

    texto: str
    prompt: str
    modo: str
    modelo: str | None


def montar_prompt(resumo_modelo: dict[str, Any]) -> str:
    """Monta um prompt usando somente valores agregados do experimento."""

    campos_obrigatorios = {"modelo", "accuracy", "recall", "f1_score"}
    ausentes = campos_obrigatorios.difference(resumo_modelo)
    if ausentes:
        raise ValueError(f"Resumo incompleto. Campos ausentes: {sorted(ausentes)}")

    hiperparametros = resumo_modelo.get("hiperparametros", "Nao informado")
    return f"""Explique o resultado agregado abaixo em ate tres paragrafos curtos:

Modelo: {resumo_modelo['modelo']}
Hiperparametros: {hiperparametros}
Accuracy: {resumo_modelo['accuracy']}
Recall: {resumo_modelo['recall']}
F1-score: {resumo_modelo['f1_score']}
Contexto: previsao estatistica de reincidencia para apoio a triagem.
"""


def _explicacao_simulada(resumo_modelo: dict[str, Any]) -> str:
    recall = float(resumo_modelo["recall"])
    f1_score = float(resumo_modelo["f1_score"])
    accuracy = float(resumo_modelo["accuracy"])
    return (
        "[DEMONSTRACAO LOCAL - nenhuma LLM foi chamada]\n\n"
        f"O modelo {resumo_modelo['modelo']} apresentou accuracy de {accuracy:.3f}, "
        f"recall de {recall:.3f} e F1-score de {f1_score:.3f}. "
        "No contexto deste projeto, o recall indica a capacidade de identificar "
        "registros positivos na base de avaliacao.\n\n"
        "Essas metricas descrevem desempenho agregado e nao representam certeza para "
        "casos individuais. O resultado deve ser usado apenas como apoio a triagem, "
        "com revisao humana e considerando possiveis falsos positivos e falsos negativos."
    )


def _obter_chave_api() -> str | None:
    """Le a chave do processo ou, no Windows, da variavel de usuario persistida.

    O fallback permite usar uma chave criada com ``setx`` mesmo quando o
    kernel do Jupyter foi iniciado antes da atualizacao do ambiente.
    """

    chave = os.environ.get("OPENAI_API_KEY")
    if chave:
        return chave

    if os.name != "nt":
        return None

    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as chave_registro:
            valor, _ = winreg.QueryValueEx(chave_registro, "OPENAI_API_KEY")
            return str(valor) if valor else None
    except (FileNotFoundError, OSError):
        return None


def gerar_interpretacao_ollama(
    resumo_modelo: dict[str, Any],
    *,
    modelo: str = "llama3.2:3b",
    endpoint: str = "http://localhost:11434/api/generate",
    timeout: int = 120,
) -> Interpretacao:
    """Gera uma explicacao por uma LLM local servida pelo Ollama.

    Nao requer chave de API nem envia dados para um servico externo. O Ollama
    deve estar instalado, em execucao, e conter o modelo indicado.
    """

    prompt = montar_prompt(resumo_modelo)
    corpo = json.dumps(
        {
            "model": modelo,
            "prompt": prompt,
            "system": INSTRUCOES,
            "stream": False,
            "options": {"temperature": 0.2},
        }
    ).encode("utf-8")
    requisicao = urllib_request.Request(
        endpoint,
        data=corpo,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib_request.urlopen(requisicao, timeout=timeout) as resposta:
            dados = json.loads(resposta.read().decode("utf-8"))
    except urllib_error.URLError as erro:
        raise RuntimeError(
            "Nao foi possivel conectar ao Ollama local. Instale o Ollama, execute "
            f"`ollama pull {modelo}` no terminal e tente novamente."
        ) from erro

    texto = str(dados.get("response", "")).strip()
    if not texto:
        raise RuntimeError("O Ollama respondeu sem texto. Verifique o modelo local e execute novamente.")

    return Interpretacao(texto, prompt, "ollama_local", modelo)


def gerar_interpretacao(
    resumo_modelo: dict[str, Any],
    *,
    usar_api: bool = False,
    modelo: str = "gpt-4.1-mini",
) -> Interpretacao:
    """Gera explicacao local ou usa a API quando explicitamente habilitada.

    A chave e lida pelo cliente oficial a partir de OPENAI_API_KEY. Nenhum dado
    individual deve ser incluido em ``resumo_modelo``.
    """

    prompt = montar_prompt(resumo_modelo)
    if not usar_api:
        return Interpretacao(_explicacao_simulada(resumo_modelo), prompt, "demonstracao", None)

    try:
        from openai import OpenAI
    except ImportError as erro:
        raise RuntimeError(
            "Dependencia ausente. Execute `pip install -r requirements.txt` antes de usar a API."
        ) from erro

    chave_api = _obter_chave_api()
    if not chave_api:
        raise RuntimeError(
            "OPENAI_API_KEY nao foi encontrada. Configure-a com setx e execute novamente."
        )

    cliente = OpenAI(api_key=chave_api)
    try:
        resposta = cliente.responses.create(
            model=modelo,
            instructions=INSTRUCOES,
            input=prompt,
        )
    except Exception as erro:
        # O fallback permite demonstrar o fluxo local sem apresentar uma
        # resposta simulada como se ela tivesse vindo da API.
        if erro.__class__.__name__ == "RateLimitError":
            texto_local = _explicacao_simulada(resumo_modelo).replace(
                "[DEMONSTRACAO LOCAL - nenhuma LLM foi chamada]\n\n", ""
            )
            return Interpretacao(
                "[API NAO EXECUTADA - saldo ou limite indisponivel]\n\n"
                "A chamada a API foi autenticada, mas a conta nao possui creditos "
                "disponiveis no momento. A explicacao abaixo foi gerada localmente.\n\n"
                + texto_local,
                prompt,
                "demonstracao_sem_creditos",
                None,
            )
        raise
    return Interpretacao(resposta.output_text, prompt, "api", modelo)
