"""Cria uma amostra estratificada da base bruta para experimentos locais."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from src.dados import caminho_base_padrao


def criar_amostra(
    tamanho: int = 50_000,
    random_state: int = 42,
    origem: str | Path | None = None,
    destino: str | Path | None = None,
) -> Path:
    """Salva uma amostra de mulheres com alvo valido, estratificada por alvo.

    O arquivo original nao e alterado. A amostra preserva as colunas brutas,
    permitindo reutilizar o mesmo pipeline de limpeza e modelagem.
    """

    arquivo_origem = Path(origem) if origem is not None else caminho_base_padrao()
    arquivo_destino = (
        Path(destino)
        if destino is not None
        else arquivo_origem.parents[1] / "samples" / f"VIOLBR25_amostra_{tamanho}.csv"
    )
    base = pd.read_csv(arquivo_origem, sep=";", low_memory=False)
    elegiveis = base.loc[
        (base["CS_SEXO"] == "F") & (base["OUT_VEZES"].isin([1, 2]))
    ].copy()
    if tamanho > len(elegiveis):
        raise ValueError(f"A amostra solicitada ({tamanho}) excede os registros elegiveis ({len(elegiveis)}).")

    amostra, _ = train_test_split(
        elegiveis,
        train_size=tamanho,
        random_state=random_state,
        stratify=elegiveis["OUT_VEZES"],
    )
    arquivo_destino.parent.mkdir(parents=True, exist_ok=True)
    amostra.to_csv(arquivo_destino, sep=";", index=False)
    return arquivo_destino


if __name__ == "__main__":
    print(criar_amostra())
