# Plano de Implementacao - Algoritmo Genetico para Otimizacao de Modelos

## 1. Objetivo e escopo

Este documento descreve como evoluir o projeto atual de predicao de reincidencia para atender a etapa de otimizacao por algoritmo genetico (AG).

O ponto de partida e o notebook `notebooks/02_modelagem_inicial.ipynb`, que ja realiza:

- leitura e limpeza da base;
- separacao estratificada entre treino e teste;
- imputacao de valores ausentes;
- treinamento de uma Arvore de Decisao e uma Regressao Logistica;
- avaliacao por accuracy, recall e F1-score.

O objetivo imediato e otimizar os hiperparametros da Arvore de Decisao, que foi o melhor modelo-base pelo recall e F1-score. A otimizacao da Regressao Logistica pode ser incluida como extensao posterior.

> Importante: o AG nao deve usar o conjunto de teste para decidir quais hiperparametros sao melhores. O teste deve permanecer reservado para a comparacao final.

---

## 2. Estrutura proposta

Manter o notebook como demonstracao e mover a logica reutilizavel para modulos Python.

```text
projeto/
|- data/
|  |- raw/VIOLBR25_ptbr.csv
|- docs/
|  |- 13-plano-implementacao-algoritmo-genetico.md
|- notebooks/
|  |- 02_modelagem_inicial.ipynb
|  |- 03_otimizacao_algoritmo_genetico.ipynb
|- src/
|  |- dados.py
|  |- avaliacao.py
|  |- algoritmo_genetico.py
|  `- experimentos.py
|- tests/
|  |- test_algoritmo_genetico.py
|  `- test_dados.py
|- resultados/
|  |- experimentos_ag.csv
|  `- melhor_modelo.json
|- requirements.txt
`- README.md
```

Os novos diretorios e arquivos serao criados somente na etapa de implementacao. Nesta fase, este documento serve como guia.

---

## 3. Parte 1 - Tornar o pipeline atual reutilizavel

### Objetivo

Evitar duplicar o codigo de limpeza e preparacao dentro do algoritmo genetico.

### Implementacao

Criar `src/dados.py` com uma funcao principal, por exemplo:

```python
def carregar_e_preparar_dados(caminho_base, random_state=42):
    """Retorna X_train, X_test, y_train e y_test ja tratados."""
```

A funcao deve reproduzir exatamente as regras ja usadas no notebook:

1. Ler `VIOLBR25_ptbr.csv`.
2. Manter registros com `CS_SEXO == "F"`.
3. Selecionar as colunas definidas no notebook.
4. Converter codigos ignorados em valores ausentes.
5. Transformar `OUT_VEZES`: `1 -> 1` e `2 -> 0`.
6. Remover colunas acima do limite definido de nulos.
7. Criar a divisao estratificada de treino e teste.
8. Calcular a imputacao exclusivamente com dados de treino e aplicala ao treino e ao teste.

### Criterio de aceite

- O notebook continua reproduzindo as metricas-base aproximadamente.
- O modulo retorna conjuntos sem valores nulos.
- A mesma `random_state` gera a mesma divisao.

---

## 4. Parte 2 - Criar protocolo correto de avaliacao

### Objetivo

Separar escolha de hiperparametros e avaliacao final.

### Implementacao

Dentro de `X_train` e `y_train`, usar validacao cruzada estratificada, por exemplo `StratifiedKFold(n_splits=3, shuffle=True, random_state=42)`.

Criar `src/avaliacao.py` com uma funcao como:

```python
def avaliar_arvore_cv(parametros, X_train, y_train, cv):
    """Retorna media e desvio das metricas em validacao cruzada."""
```

Para cada dobra:

1. Criar uma `DecisionTreeClassifier` com os parametros recebidos.
2. Treinar somente na parte de treino da dobra.
3. Prever a parte de validacao.
4. Calcular `accuracy`, `recall` e `f1_score`.

### Funcao fitness

Usar inicialmente o recall medio da classe positiva como fitness, pois o projeto considera mais grave deixar de identificar um caso de reincidencia.

Opcao mais equilibrada, caso haja muitos falsos positivos:

```python
fitness = 0.7 * recall_medio + 0.3 * f1_medio
```

Registrar a justificativa da metrica no relatorio final.

### Criterio de aceite

- Nenhuma previsao do conjunto de teste ocorre durante a busca genetica.
- Cada individuo recebe uma fitness reproduzivel.
- O retorno inclui media e desvio-padrao das metricas.

---

## 5. Parte 3 - Definir cromossomo e espaco de busca

### Objetivo

Representar uma configuracao de hiperparametros como um individuo do AG.

### Cromossomo inicial: Arvore de Decisao

Representar o individuo como dicionario:

```python
{
    "max_depth": 5,
    "min_samples_split": 10,
    "min_samples_leaf": 2,
    "criterion": "gini",
    "class_weight": None,
}
```

Espaco de busca inicial:

| Gene | Valores permitidos |
| --- | --- |
| `max_depth` | `3, 4, ..., 15, None` |
| `min_samples_split` | `2, 5, 10, 20, 30` |
| `min_samples_leaf` | `1, 2, 5, 10` |
| `criterion` | `gini`, `entropy`, `log_loss` |
| `class_weight` | `None`, `balanced` |

Todos os individuos devem conter apenas combinacoes validas para `DecisionTreeClassifier`.

### Criterio de aceite

- A criacao de um individuo aleatorio sempre retorna parametros validos.
- Os valores do cromossomo podem ser passados diretamente ao classificador.

---

## 6. Parte 4 - Implementar o algoritmo genetico

### Objetivo

Criar `src/algoritmo_genetico.py`, sem depender de bibliotecas de AG. A implementacao manual deixa claros os operadores exigidos pelo desafio.

### Funcoes previstas

```python
def criar_individuo(espaco_busca, rng): ...
def criar_populacao(tamanho, espaco_busca, rng): ...
def avaliar_populacao(populacao, funcao_fitness): ...
def selecao_torneio(populacao_avaliada, tamanho_torneio, rng): ...
def crossover_uniforme(pai_a, pai_b, rng): ...
def mutar(individuo, espaco_busca, taxa_mutacao, rng): ...
def executar_ag(configuracao_ag, funcao_fitness, espaco_busca): ...
```

### Operadores escolhidos

1. **Selecao por torneio:** selecionar aleatoriamente alguns individuos e escolher o de maior fitness. E simples e funciona bem para este problema.
2. **Crossover uniforme:** para cada gene, o descendente recebe o valor do pai A ou B. Como os genes nao representam uma rota, esse operador e mais apropriado que crossover de TSP.
3. **Mutacao por substituicao:** com determinada probabilidade, trocar um gene por outro valor valido do seu espaco de busca.
4. **Elitismo:** carregar o melhor individuo de cada geracao para a proxima, evitando perder a melhor solucao ja encontrada.

### Fluxo da execucao

```text
Criar populacao inicial
        |
Avaliar fitness por validacao cruzada
        |
Registrar melhor individuo da geracao
        |
Selecionar pais -> crossover -> mutacao -> nova populacao
        |
Repetir ate atingir numero de geracoes ou criterio de estagnacao
        |
Retornar melhor configuracao e historico
```

### Criterio de aceite

- O historico informa melhor fitness, fitness medio e parametros do melhor individuo em cada geracao.
- A mutacao nunca gera valores fora do espaco definido.
- O elitismo preserva o melhor fitness global.

---

## 7. Parte 5 - Executar tres experimentos obrigatorios

Usar a mesma base, protocolo de validacao e espaco de busca nos tres experimentos. Mudar somente os parametros do AG.

| Experimento | Populacao | Geracoes | Taxa de mutacao | Objetivo |
| --- | ---: | ---: | ---: | --- |
| E1 - referencia | 10 | 8 | 0.10 | estabelecer comportamento inicial |
| E2 - diversidade | 20 | 12 | 0.20 | testar busca mais ampla |
| E3 - exploracao controlada | 30 | 15 | 0.05 | testar mais individuos com menor mutacao |

Para cada experimento, registrar:

- configuracao do AG;
- semente aleatoria;
- melhor cromossomo;
- fitness por geracao;
- accuracy, recall e F1 medios na validacao;
- tempo de execucao;
- resultado final no teste, feito somente uma vez para o melhor individuo de cada experimento.

Salvar a tabela consolidada em `resultados/experimentos_ag.csv`.

---

## 8. Parte 6 - Comparar com os modelos-base

### Baselines

Reproduzir as configuracoes atuais:

```python
DecisionTreeClassifier(max_depth=5, random_state=42)
LogisticRegression(random_state=42, max_iter=1000)
```

### Comparacao final

Treinar a arvore-base e a melhor arvore encontrada pelo AG usando todo o conjunto de treino. Avaliar ambas uma unica vez no mesmo conjunto de teste reservado.

Tabela esperada:

| Modelo | Accuracy teste | Recall teste | F1 teste | Observacao |
| --- | ---: | ---: | ---: | --- |
| Arvore-base | ... | ... | ... | `max_depth=5` |
| Melhor AG - E1 | ... | ... | ... | parametros encontrados |
| Melhor AG - E2 | ... | ... | ... | parametros encontrados |
| Melhor AG - E3 | ... | ... | ... | parametros encontrados |

Incluir tambem matriz de confusao e explicabilidade da melhor configuracao final.

---

## 9. Parte 7 - Testes e rastreabilidade

### Testes automatizados minimos

- `test_criar_individuo_gera_parametros_validos`;
- `test_mutacao_mantem_dominio_dos_genes`;
- `test_crossover_mantem_dominio_dos_genes`;
- `test_elitismo_nao_perde_melhor_individuo`;
- `test_pipeline_nao_retorna_nulos`.

### Logging

Usar o modulo `logging` da biblioteca padrao para registrar:

- inicio e fim de cada experimento;
- configuracao utilizada;
- resultados de cada geracao;
- excecoes ou parametros invalidos;
- duracao de cada execucao.

Nao incluir identificadores pessoais ou linhas brutas da base nos logs.

---

## 10. Parte 8 - Notebook de demonstracao e documentacao

Criar `notebooks/03_otimizacao_algoritmo_genetico.ipynb` para demonstrar:

1. carregamento pelo modulo reutilizavel;
2. configuracao do espaco de busca;
3. execucao dos tres experimentos;
4. grafico da evolucao do fitness por geracao;
5. tabela comparativa com baselines;
6. matriz de confusao do melhor modelo;
7. interpretacao dos resultados e limitacoes.

Atualizar o README com instrucoes de execucao e criar um diagrama simples da arquitetura:

```text
Base bruta -> Preparacao de dados -> Treino/validacao -> Algoritmo genetico
                                                       |
                                                       v
                                                Melhor configuracao
                                                       |
                                                       v
                                      Treino final -> Teste reservado -> Relatorio
```

---

## 11. Ordem sugerida de implementacao

1. Extrair a preparacao de dados do notebook para `src/dados.py`.
2. Confirmar que a linha de base continua reproduzivel.
3. Criar a avaliacao por validacao cruzada em `src/avaliacao.py`.
4. Implementar cromossomo, populacao e operadores em `src/algoritmo_genetico.py`.
5. Escrever os testes dos operadores.
6. Rodar um experimento pequeno para validar o fluxo.
7. Rodar E1, E2 e E3 e salvar os resultados.
8. Comparar os melhores individuos com o baseline no teste reservado.
9. Documentar a conclusao e preparar a integracao com LLM como proxima etapa.

---

## 12. Fora do escopo desta primeira entrega

Os itens abaixo pertencem a Fase 2, mas podem ser implementados depois que a otimizacao estiver pronta:

- integracao com LLM e avaliacao de prompts;
- API ou interface visual;
- implantacao em nuvem e infraestrutura como codigo;
- video de demonstracao;
- otimizacao genetica da Regressao Logistica ou de outros modelos.

