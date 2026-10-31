"""Avaliacao de candidatos do algoritmo genetico sem usar o teste final."""

from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, recall_score
from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier


def avaliar_arvore_cv(
    parametros: dict[str, Any],
    X_train: pd.DataFrame,
    y_train: pd.Series,
    *,
    n_splits: int = 3,
    random_state: int = 42,
) -> dict[str, float]:
    """Avalia parametros por validacao cruzada apenas no conjunto de treino."""

    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    resultados: list[dict[str, float]] = []

    for indices_treino, indices_validacao in cv.split(X_train, y_train):
        modelo = DecisionTreeClassifier(random_state=random_state, **parametros)
        modelo.fit(X_train.iloc[indices_treino], y_train.iloc[indices_treino])
        previsoes = modelo.predict(X_train.iloc[indices_validacao])
        esperado = y_train.iloc[indices_validacao]
        resultados.append(
            {
                "accuracy": accuracy_score(esperado, previsoes),
                "recall": recall_score(esperado, previsoes, zero_division=0),
                "f1_score": f1_score(esperado, previsoes, zero_division=0),
            }
        )

    metricas = pd.DataFrame(resultados)
    return {
        "accuracy_media": float(metricas["accuracy"].mean()),
        "accuracy_desvio": float(metricas["accuracy"].std(ddof=0)),
        "recall_media": float(metricas["recall"].mean()),
        "recall_desvio": float(metricas["recall"].std(ddof=0)),
        "f1_media": float(metricas["f1_score"].mean()),
        "f1_desvio": float(metricas["f1_score"].std(ddof=0)),
    }


def calcular_fitness(metricas: dict[str, float]) -> float:
    """Combina recall e F1, priorizando identificar reincidencias reais."""

    return 0.7 * metricas["recall_media"] + 0.3 * metricas["f1_media"]
