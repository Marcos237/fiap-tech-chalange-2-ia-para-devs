# Checklist antes da execucao - Fase 2

## Objetivo

Antes de executar experimentos demorados, este documento registra o que sera implementado, como os resultados serao validados e quais evidencias deverao aparecer no relatorio e no video.

O projeto parte da modelagem existente de reincidencia e evolui a Arvore de Decisao com um algoritmo genetico (AG).

---

## 1. O que ja existe

- Base bruta em `data/raw/VIOLBR25_ptbr.csv`.
- Notebook de modelos-base: `notebooks/02_modelagem_inicial.ipynb`.
- Preparacao reutilizavel de dados: `src/dados.py`.
- Testes da preparacao de dados: `tests/test_dados.py`.
- Baselines documentados: Arvore de Decisao e Regressao Logistica.

---

## 2. O que sera implementado antes dos experimentos

### 2.1 Avaliacao dos candidatos

- Validacao cruzada estratificada usando somente o conjunto de treino.
- Calculo de accuracy, recall e F1-score por dobra.
- Fitness baseada principalmente em recall, com F1 como criterio complementar.
- Retorno de media e desvio-padrao das metricas.

### 2.2 Algoritmo genetico simples

- Individuo representado por hiperparametros de uma `DecisionTreeClassifier`.
- Populacao inicial aleatoria e valida.
- Selecao por torneio.
- Crossover uniforme.
- Mutacao por substituicao de gene.
- Elitismo para preservar a melhor configuracao.
- Historico de fitness por geracao.

### 2.3 Tres experimentos obrigatorios

| Experimento | Populacao | Geracoes | Mutacao |
| --- | ---: | ---: | ---: |
| E1 | 10 | 8 | 10% |
| E2 | 20 | 12 | 20% |
| E3 | 30 | 15 | 5% |

Cada experimento devera salvar configuracao, semente, melhor individuo, fitness e duracao.

### 2.4 Comparacao final

- Treinar o modelo-base no treino completo.
- Treinar cada melhor configuracao encontrada no treino completo.
- Avaliar todos uma unica vez no mesmo conjunto de teste reservado.
- Salvar uma tabela comparativa de accuracy, recall e F1-score.

---

## 3. Arquivos esperados apos a implementacao

```text
src/
|- dados.py
|- avaliacao.py
|- algoritmo_genetico.py
`- experimentos.py

tests/
|- test_dados.py
`- test_algoritmo_genetico.py

notebooks/
`- 03_otimizacao_algoritmo_genetico.ipynb

resultados/
|- experimentos_ag.csv
|- historico_ag.csv
`- comparacao_modelos.csv
```

---

## 4. Verificacoes antes de executar os tres experimentos

- [ ] Os testes unitarios da preparacao e do AG passam.
- [ ] A funcao fitness nunca usa `X_test` ou `y_test`.
- [ ] A geracao de individuos produz apenas parametros validos.
- [ ] Crossover e mutacao mantem os genes dentro do espaco de busca.
- [ ] O melhor fitness nao diminui quando o elitismo esta ativo.
- [ ] Um experimento pequeno de teste termina e grava historico.
- [ ] Ha memoria e tempo suficientes para os tres experimentos.

---

## 5. Evidencias a gerar para o relatorio e video

1. Diagrama do fluxo: dados -> validacao -> AG -> melhor modelo -> teste final.
2. Tabela dos hiperparametros pesquisados.
3. Grafico de fitness por geracao para E1, E2 e E3.
4. Tabela comparando baseline e melhores modelos otimizados.
5. Matriz de confusao do baseline e do melhor modelo final.
6. Explicabilidade do melhor modelo com importancia de variaveis ou SHAP.
7. Registro dos prompts e exemplos da integracao com LLM.

---

## 6. Integracao com LLM - dependencia externa

A integracao com uma LLM sera preparada no codigo para receber um resumo do modelo e gerar uma explicacao em linguagem simples. Para realizar chamadas reais a uma LLM sera necessario configurar uma credencial valida, por exemplo `OPENAI_API_KEY`.

Sem uma credencial, ainda e possivel implementar e testar localmente:

- a montagem segura do prompt;
- a validacao dos dados enviados;
- um modo demonstracao que deixa claro que a resposta e simulada.

O modo demonstracao nao substitui a integracao real exigida pelo enunciado. Antes do video final, a chamada real e sua avaliacao precisam ser realizadas.

---

## 7. Ordem de execucao

1. Implementar e testar `avaliacao.py`.
2. Implementar e testar `algoritmo_genetico.py`.
3. Implementar `experimentos.py` e fazer uma execucao pequena de validacao.
4. Executar E1, E2 e E3.
5. Gerar resultados, graficos e comparacao final.
6. Preparar a integracao real com LLM.
7. Atualizar notebook, README e relatorio.
8. Somente entao criar roteiro e gravar o video.

