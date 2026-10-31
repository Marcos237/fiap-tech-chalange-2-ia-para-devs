"""Execucao e registro dos experimentos de otimizacao genetica."""

from __future__ import annotations

from pathlib import Path
from time import perf_counter
from typing import Any

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, recall_score
from sklearn.tree import DecisionTreeClassifier

from src.algoritmo_genetico import ConfiguracaoAG, EspacoBusca, executar_ag
from src.avaliacao import avaliar_arvore_cv, calcular_fitness


ESPACO_ARVORE: EspacoBusca = {
    "max_depth": [3, 4, 5, 6, 8, 10, 12, 15, None],
    "min_samples_split": [2, 5, 10, 20, 30],
    "min_samples_leaf": [1, 2, 5, 10],
    "criterion": ["gini", "entropy", "log_loss"],
    "class_weight": [None, "balanced"],
}

CONFIGURACOES_PADRAO = {
    "E1_referencia": ConfiguracaoAG(10, 8, 0.10, random_state=42),
    "E2_diversidade": ConfiguracaoAG(20, 12, 0.20, random_state=42),
    "E3_exploracao": ConfiguracaoAG(30, 15, 0.05, random_state=42),
}


def executar_experimentos(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    *,
    diretorio_resultados: str | Path = "resultados",
    configuracoes: dict[str, ConfiguracaoAG] | None = None,
) -> pd.DataFrame:
    """Roda os experimentos, avalia no teste reservado e grava arquivos CSV."""

    configuracoes = configuracoes or CONFIGURACOES_PADRAO
    destino = Path(diretorio_resultados)
    destino.mkdir(parents=True, exist_ok=True)
    linhas_resultado: list[dict[str, Any]] = []
    linhas_historico: list[dict[str, Any]] = []

    for nome, configuracao in configuracoes.items():
        inicio = perf_counter()

        def fitness(parametros: dict[str, Any]) -> float:
            return calcular_fitness(avaliar_arvore_cv(parametros, X_train, y_train))

        resultado_ag = executar_ag(configuracao, ESPACO_ARVORE, fitness)
        modelo = DecisionTreeClassifier(random_state=42, **resultado_ag.melhor_individuo)
        modelo.fit(X_train, y_train)
        previsoes = modelo.predict(X_test)
        linhas_resultado.append(
            {
                "experimento": nome,
                "duracao_segundos": round(perf_counter() - inicio, 2),
                "melhor_fitness_cv": resultado_ag.melhor_fitness,
                "accuracy_teste": accuracy_score(y_test, previsoes),
                "recall_teste": recall_score(y_test, previsoes, zero_division=0),
                "f1_teste": f1_score(y_test, previsoes, zero_division=0),
                **resultado_ag.melhor_individuo,
            }
        )
        linhas_historico.extend({"experimento": nome, **linha} for linha in resultado_ag.historico)

    resultados = pd.DataFrame(linhas_resultado)
    resultados.to_csv(destino / "experimentos_ag.csv", index=False)
    pd.DataFrame(linhas_historico).to_csv(destino / "historico_ag.csv", index=False)
    return resultados
