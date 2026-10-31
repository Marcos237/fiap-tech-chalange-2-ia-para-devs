"""Algoritmo genetico generico para buscar hiperparametros discretos."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Any, Callable


Individuo = dict[str, Any]
EspacoBusca = dict[str, list[Any]]
FuncaoFitness = Callable[[Individuo], float]


@dataclass(frozen=True)
class ConfiguracaoAG:
    tamanho_populacao: int = 10
    geracoes: int = 8
    taxa_mutacao: float = 0.10
    tamanho_torneio: int = 3
    elitismo: int = 1
    random_state: int = 42


@dataclass
class ResultadoAG:
    melhor_individuo: Individuo
    melhor_fitness: float
    historico: list[dict[str, Any]]


def validar_espaco_busca(espaco_busca: EspacoBusca) -> None:
    if not espaco_busca:
        raise ValueError("O espaco de busca nao pode estar vazio.")
    if any(not valores for valores in espaco_busca.values()):
        raise ValueError("Todo gene precisa ter ao menos um valor permitido.")


def criar_individuo(espaco_busca: EspacoBusca, rng: Random) -> Individuo:
    validar_espaco_busca(espaco_busca)
    return {gene: rng.choice(valores) for gene, valores in espaco_busca.items()}


def criar_populacao(tamanho: int, espaco_busca: EspacoBusca, rng: Random) -> list[Individuo]:
    if tamanho < 2:
        raise ValueError("A populacao precisa ter ao menos dois individuos.")
    return [criar_individuo(espaco_busca, rng) for _ in range(tamanho)]


def avaliar_populacao(
    populacao: list[Individuo], funcao_fitness: FuncaoFitness
) -> list[tuple[Individuo, float]]:
    avaliados = [(individuo, float(funcao_fitness(individuo))) for individuo in populacao]
    return sorted(avaliados, key=lambda item: item[1], reverse=True)


def selecao_torneio(
    populacao_avaliada: list[tuple[Individuo, float]], tamanho_torneio: int, rng: Random
) -> Individuo:
    if not 1 <= tamanho_torneio <= len(populacao_avaliada):
        raise ValueError("O tamanho do torneio deve estar entre 1 e o tamanho da populacao.")
    participantes = rng.sample(populacao_avaliada, tamanho_torneio)
    vencedor, _ = max(participantes, key=lambda item: item[1])
    return vencedor.copy()


def crossover_uniforme(pai_a: Individuo, pai_b: Individuo, rng: Random) -> Individuo:
    if pai_a.keys() != pai_b.keys():
        raise ValueError("Os pais precisam possuir os mesmos genes.")
    return {gene: rng.choice([pai_a[gene], pai_b[gene]]) for gene in pai_a}


def mutar(
    individuo: Individuo,
    espaco_busca: EspacoBusca,
    taxa_mutacao: float,
    rng: Random,
) -> Individuo:
    if not 0 <= taxa_mutacao <= 1:
        raise ValueError("A taxa de mutacao deve estar entre 0 e 1.")
    if individuo.keys() != espaco_busca.keys():
        raise ValueError("Os genes do individuo devem coincidir com o espaco de busca.")

    mutante = individuo.copy()
    for gene, valores in espaco_busca.items():
        if rng.random() < taxa_mutacao:
            mutante[gene] = rng.choice(valores)
    return mutante


def executar_ag(
    configuracao: ConfiguracaoAG,
    espaco_busca: EspacoBusca,
    funcao_fitness: FuncaoFitness,
) -> ResultadoAG:
    """Executa o AG e devolve o melhor individuo e o resumo por geracao."""

    if configuracao.geracoes < 1:
        raise ValueError("O numero de geracoes deve ser positivo.")
    if not 0 <= configuracao.elitismo < configuracao.tamanho_populacao:
        raise ValueError("O elitismo deve ser menor que o tamanho da populacao.")

    rng = Random(configuracao.random_state)
    populacao = criar_populacao(configuracao.tamanho_populacao, espaco_busca, rng)
    melhor_individuo: Individuo | None = None
    melhor_fitness = float("-inf")
    historico: list[dict[str, Any]] = []

    for geracao in range(1, configuracao.geracoes + 1):
        avaliados = avaliar_populacao(populacao, funcao_fitness)
        melhor_geracao, fitness_geracao = avaliados[0]
        if fitness_geracao > melhor_fitness:
            melhor_individuo = melhor_geracao.copy()
            melhor_fitness = fitness_geracao

        historico.append(
            {
                "geracao": geracao,
                "melhor_fitness": fitness_geracao,
                "fitness_medio": sum(fitness for _, fitness in avaliados) / len(avaliados),
                "melhor_individuo": melhor_geracao.copy(),
            }
        )

        proxima_populacao = [individuo.copy() for individuo, _ in avaliados[: configuracao.elitismo]]
        while len(proxima_populacao) < configuracao.tamanho_populacao:
            pai_a = selecao_torneio(avaliados, configuracao.tamanho_torneio, rng)
            pai_b = selecao_torneio(avaliados, configuracao.tamanho_torneio, rng)
            filho = crossover_uniforme(pai_a, pai_b, rng)
            proxima_populacao.append(mutar(filho, espaco_busca, configuracao.taxa_mutacao, rng))
        populacao = proxima_populacao

    if melhor_individuo is None:
        raise RuntimeError("O algoritmo genetico nao avaliou individuos.")
    return ResultadoAG(melhor_individuo, melhor_fitness, historico)
