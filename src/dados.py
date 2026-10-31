"""Preparacao reproduzivel dos dados para os modelos de classificacao.

As regras deste modulo foram extraidas do notebook de modelagem inicial.
O conjunto de teste e separado antes da imputacao para evitar vazamento de
informacao entre treino e teste.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.model_selection import train_test_split


COLUNAS_MODELO = [
    "NU_IDADE_N", "CS_RACA", "CS_ESCOL_N", "SIT_CONJUG", "CS_GESTANT",
    "DEF_TRANS", "DEF_FISICA", "DEF_MENTAL", "DEF_VISUAL", "DEF_AUDITI",
    "TRAN_MENT", "SG_UF", "LOCAL_OCOR", "VIOL_FISIC", "VIOL_PSICO",
    "VIOL_SEXU", "VIOL_NEGLI", "VIOL_FINAN", "VIOL_TORT", "LES_AUTOP",
    "AG_FORCA", "AG_CORTE", "AG_FOGO", "AG_AMEACA", "REL_CONJ",
    "REL_EXCON", "REL_NAMO", "REL_PAI", "REL_MAE", "AUTOR_SEXO",
    "AUTOR_ALCO", "NUM_ENVOLV", "OUT_VEZES",
]

CODIGOS_IGNORADOS = {
    "CS_RACA": [9], "CS_ESCOL_N": [9], "SIT_CONJUG": [9],
    "CS_GESTANT": [9], "DEF_TRANS": [9], "DEF_FISICA": [9],
    "DEF_MENTAL": [9], "DEF_VISUAL": [9], "DEF_AUDITI": [9],
    "TRAN_MENT": [9], "LOCAL_OCOR": [9, 99], "VIOL_FISIC": [9],
    "VIOL_PSICO": [9], "VIOL_SEXU": [9], "VIOL_NEGLI": [9],
    "VIOL_FINAN": [9], "VIOL_TORT": [9], "LES_AUTOP": [9],
    "AG_FORCA": [9], "AG_CORTE": [9], "AG_FOGO": [9], "AG_AMEACA": [9],
    "REL_CONJ": [9], "REL_EXCON": [9], "REL_NAMO": [9], "REL_PAI": [9],
    "REL_MAE": [9], "AUTOR_SEXO": [9], "AUTOR_ALCO": [9],
    "NUM_ENVOLV": [9],
}

MAPA_ALVO = {1: 1, 2: 0}
IDADE_MINIMA = 0
IDADE_MAXIMA = 120
LIMITE_NULOS_EXCLUSAO = 30.0


@dataclass
class DadosPreparados:
    """Conjuntos prontos para treinamento e informacoes de rastreabilidade."""

    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series
    colunas_removidas: list[str]
    valores_imputacao: dict[str, Any]


def caminho_base_padrao() -> Path:
    """Retorna o CSV bruto a partir da raiz do projeto, sem depender do CWD."""

    return Path(__file__).resolve().parents[1] / "data" / "raw" / "VIOLBR25_ptbr.csv"


def carregar_base(caminho: str | Path | None = None) -> pd.DataFrame:
    """Carrega a base bruta e valida se o arquivo e as colunas existem."""

    arquivo = Path(caminho) if caminho is not None else caminho_base_padrao()
    if not arquivo.exists():
        raise FileNotFoundError(f"Base nao encontrada: {arquivo}")

    base = pd.read_csv(arquivo, sep=";", low_memory=False)
    colunas_necessarias = {"CS_SEXO", *COLUNAS_MODELO}
    colunas_ausentes = sorted(colunas_necessarias.difference(base.columns))
    if colunas_ausentes:
        raise ValueError(f"A base nao possui as colunas esperadas: {colunas_ausentes}")
    return base


def limpar_base(base_bruta: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Aplica as mesmas regras de selecao e limpeza usadas no notebook."""

    colunas_necessarias = {"CS_SEXO", *COLUNAS_MODELO}
    colunas_ausentes = sorted(colunas_necessarias.difference(base_bruta.columns))
    if colunas_ausentes:
        raise ValueError(f"DataFrame sem colunas esperadas: {colunas_ausentes}")

    base = base_bruta.loc[base_bruta["CS_SEXO"] == "F", COLUNAS_MODELO].copy()

    for coluna, codigos in CODIGOS_IGNORADOS.items():
        base[coluna] = base[coluna].replace(codigos, pd.NA)

    base = base.loc[base["OUT_VEZES"].isin(MAPA_ALVO)].copy()
    base["OUT_VEZES"] = base["OUT_VEZES"].map(MAPA_ALVO).astype("int64")

    if "NU_IDADE_N" in base:
        idade_invalida = base["NU_IDADE_N"].lt(IDADE_MINIMA) | base["NU_IDADE_N"].gt(IDADE_MAXIMA)
        base.loc[idade_invalida, "NU_IDADE_N"] = pd.NA

    percentuais_nulos = base.isna().mean().mul(100)
    colunas_removidas = percentuais_nulos[percentuais_nulos > LIMITE_NULOS_EXCLUSAO].index.tolist()
    base = base.drop(columns=colunas_removidas)

    if base.empty:
        raise ValueError("A limpeza removeu todos os registros validos da base.")
    if base["OUT_VEZES"].nunique() != 2:
        raise ValueError("A base limpa precisa conter as duas classes de OUT_VEZES.")

    return base, colunas_removidas


def dividir_e_imputar(
    base_limpa: pd.DataFrame,
    *,
    test_size: float = 0.2,
    random_state: int = 42,
) -> DadosPreparados:
    """Divide a base estratificadamente e imputa usando apenas o treino."""

    X = base_limpa.drop(columns="OUT_VEZES")
    y = base_limpa["OUT_VEZES"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    X_train = X_train.copy()
    X_test = X_test.copy()
    valores_imputacao: dict[str, Any] = {}
    for coluna in X_train.columns:
        if coluna == "NU_IDADE_N":
            valor = X_train[coluna].median()
        else:
            moda = X_train[coluna].mode(dropna=True)
            valor = moda.iloc[0] if not moda.empty else 0

        valores_imputacao[coluna] = valor
        X_train[coluna] = X_train[coluna].fillna(valor)
        X_test[coluna] = X_test[coluna].fillna(valor)

    if X_train.isna().any().any() or X_test.isna().any().any():
        raise ValueError("A imputacao nao eliminou todos os valores ausentes.")

    return DadosPreparados(
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
        colunas_removidas=[],
        valores_imputacao=valores_imputacao,
    )


def preparar_dados(
    caminho: str | Path | None = None,
    *,
    test_size: float = 0.2,
    random_state: int = 42,
) -> DadosPreparados:
    """Executa o pipeline completo de leitura, limpeza, divisao e imputacao."""

    base_limpa, colunas_removidas = limpar_base(carregar_base(caminho))
    resultado = dividir_e_imputar(
        base_limpa, test_size=test_size, random_state=random_state
    )
    resultado.colunas_removidas = colunas_removidas
    return resultado
