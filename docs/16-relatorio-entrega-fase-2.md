# Relatorio de Entrega — Projeto 1: Otimizacao de Modelos

## 1. Objetivo

O projeto investiga a predicao estatistica de reincidencia de violencia contra a mulher a partir de registros do SINAN/DATASUS. A variavel-alvo foi `OUT_VEZES`, transformada em classificacao binaria:

- `1`: registro de reincidencia;
- `0`: registro sem reincidencia.

O objetivo desta etapa foi otimizar os hiperparametros de uma Arvore de Decisao por meio de um Algoritmo Genetico (AG), comparar o modelo otimizado com o modelo-base e produzir uma explicacao segura dos resultados com apoio de LLM.

> O modelo e exclusivamente um apoio estatistico a triagem. Ele nao realiza diagnostico, nao define condutas e nao deve ser usado para decisao individual sem avaliacao humana.

## 2. Dados e protocolo experimental

A base original esta em `data/raw/VIOLBR25_ptbr.csv`. Para tornar a execucao local viavel, foi criada uma amostra estratificada de 50.000 registros elegiveis em `data/samples/VIOLBR25_amostra_50000.csv`. A base original nao foi modificada.

Depois da limpeza, foram mantidas 31 variaveis preditoras. A amostra foi dividida estratificadamente em:

| Conjunto | Registros | Classe 0 | Classe 1 |
| --- | ---: | ---: | ---: |
| Treino | 40.000 | 18.073 | 21.927 |
| Teste reservado | 10.000 | 4.518 | 5.482 |

Os valores ausentes foram imputados usando somente estatisticas calculadas no conjunto de treino. O conjunto de teste permaneceu reservado durante a busca genetica. Cada candidato foi avaliado apenas no treino com validacao cruzada estratificada de 3 dobras.

## 3. Modelo-base

O modelo de referencia foi uma `DecisionTreeClassifier` com `max_depth=5` e `random_state=42`.

| Modelo | Accuracy | Recall | F1-score |
| --- | ---: | ---: | ---: |
| Arvore-base | 0,6271 | 0,5410 | 0,6140 |

O recall foi priorizado porque deixar de identificar um registro positivo pode reduzir a capacidade de sinalizacao para revisao humana.

## 4. Algoritmo genetico implementado

O AG foi implementado manualmente, sem bibliotecas especializadas, para tornar seus operadores verificaveis:

- **individuo/cromossomo:** uma configuracao de hiperparametros da Arvore de Decisao;
- **selecao:** torneio com tres candidatos;
- **crossover:** uniforme, escolhendo cada gene de um dos pais;
- **mutacao:** substituicao de gene por valor valido do espaco de busca;
- **elitismo:** preservacao do melhor individuo de cada geracao;
- **fitness:** `0,7 × recall medio + 0,3 × F1 medio`, obtidos na validacao cruzada.

O espaco de busca incluiu `max_depth`, `min_samples_split`, `min_samples_leaf`, `criterion` e `class_weight`.

## 5. Experimentos executados

| Experimento | Populacao | Geracoes | Mutacao | Duracao |
| --- | ---: | ---: | ---: | ---: |
| E1 — referencia | 10 | 8 | 10% | 99,98 s |
| E2 — diversidade | 20 | 12 | 20% | 309,63 s |
| E3 — exploracao | 30 | 15 | 5% | 535,10 s |

Os tres experimentos encontraram a mesma melhor configuracao:

```text
max_depth=3
min_samples_split=2
min_samples_leaf=1
criterion=gini
class_weight=None
```

O melhor fitness medio em validacao cruzada foi `0,7403`. Como a mesma configuracao apareceu em todas as execucoes, o resultado sugere estabilidade dentro do espaco de busca avaliado. O melhor individuo ja estava presente na primeira geracao, e o elitismo preservou essa solucao ao longo das geracoes.

## 6. Comparacao: original versus otimizado

| Modelo | Accuracy | Recall | F1-score |
| --- | ---: | ---: | ---: |
| Arvore-base (`max_depth=5`) | 0,6271 | 0,5410 | 0,6140 |
| Melhor AG — E1 | 0,6028 | 0,9236 | 0,7183 |
| Melhor AG — E2 | 0,6028 | 0,9236 | 0,7183 |
| Melhor AG — E3 | 0,6028 | 0,9236 | 0,7183 |

O modelo otimizado aumentou o recall de **54,1% para 92,4%** e o F1-score de **61,4% para 71,8%**. Em contrapartida, a acuracia caiu de **62,7% para 60,3%**. Essa troca era esperada: uma arvore mais rasa passa a identificar mais positivos, mas tambem pode gerar mais falsos positivos.

Para este projeto, o ganho de recall e relevante porque reduz a quantidade de casos positivos nao sinalizados. Ainda assim, a queda de acuracia reforca que a saida do modelo nao pode ser interpretada como decisao automatica; ela precisa de revisao por profissionais.

Os arquivos reproduziveis dos resultados sao:

- `resultados/experimentos_ag.csv`;
- `resultados/historico_ag.csv`;
- `resultados/comparacao_modelos.csv`.

## 7. Integracao com LLM

Foi implementado o modulo `src/interpretacao_llm.py` para transformar metricas agregadas em uma explicacao curta e segura. O prompt envia apenas:

- nome do modelo;
- hiperparametros;
- accuracy, recall e F1-score;
- contexto de apoio a triagem.

O prompt proibe diagnosticos, recomendacoes individuais e apresentacao de previsoes como certeza. Nenhuma linha da base, identificador de pessoa ou dado sensivel e enviado para a LLM.

No notebook foi executado o **modo demonstracao local**, que produziu uma explicacao coerente para o melhor modelo. A verificacao de qualidade considerou:

| Criterio | Resultado no modo demonstracao |
| --- | --- |
| Fidelidade | As metricas citadas correspondem aos resultados calculados. |
| Clareza | A explicacao usa linguagem direta e nao tecnica. |
| Seguranca | Nao faz diagnostico nem recomenda conduta individual. |
| Limitacoes | Informa possibilidade de erros e necessidade de revisao humana. |
| Privacidade | Utiliza somente dados agregados. |

**Pendencia para uma entrega que exija chamada real:** configurar `OPENAI_API_KEY` e executar `gerar_interpretacao(..., usar_api=True)`. O modo demonstracao evidencia o fluxo e a seguranca do prompt, mas nao substitui uma chamada real a uma LLM quando isso for exigido pela avaliacao.

## 8. Desafios enfrentados e solucoes

| Desafio | Solucao adotada |
| --- | --- |
| Base completa tornou a busca genetica muito demorada | Criacao de amostra estratificada de 50 mil registros, sem alterar a fonte original. |
| Risco de vazamento de dados | Separacao treino/teste antes da imputacao e uso exclusivo do treino na validacao cruzada. |
| Necessidade de explicar o AG | Implementacao manual de selecao, crossover, mutacao, elitismo e historico por geracao. |
| Dados sensiveis | LLM recebe somente metricas e hiperparametros agregados. |
| Trade-off entre metricas | Recall foi priorizado; accuracy e F1-score foram reportados para evitar uma avaliacao unilateral. |

## 9. Arquitetura e reproducibilidade

```text
CSV bruto -> amostra estratificada -> limpeza/imputacao -> treino + teste reservado
                                                    |
                                                    v
                                    validacao cruzada no treino -> AG
                                                    |
                                                    v
                              melhor hiperparametro -> teste reservado -> comparacao
                                                    |
                                                    v
                               metricas agregadas -> LLM -> explicacao supervisionada
```

Para reproduzir a analise, execute `notebooks/03_otimizacao_algoritmo_genetico.ipynb` usando o ambiente virtual do projeto. Os testes automatizados cobrem limpeza, imputacao, criacao de individuos, crossover, mutacao, elitismo e o modo demonstracao da LLM.

## 10. Conclusao

O Algoritmo Genetico encontrou uma configuracao de Arvore de Decisao com maior capacidade de identificar a classe positiva na amostra avaliada. A configuracao `max_depth=3`, `min_samples_split=2`, `min_samples_leaf=1` e `criterion=gini` elevou o recall para 92,4% e o F1-score para 71,8%.

O resultado nao significa que o modelo esta pronto para uso autonomo. Ele representa uma ferramenta experimental de apoio a triagem, dependente de monitoramento, validacao em outros recortes da base e decisao humana em qualquer caso concreto.
