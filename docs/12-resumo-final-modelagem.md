# 12 - Resumo Final da Modelagem

## 1. Objetivo

O objetivo do trabalho foi analisar dados sobre violencia contra a mulher e tentar prever a reincidencia da violencia.

A variavel alvo escolhida foi:

```text
OUT_VEZES
```

Interpretacao usada:

- `1` = houve reincidencia
- `0` = nao houve reincidencia

## 2. Preparacao da Base

Primeiro, a base foi preparada para a modelagem:

- na leitura inicial, a base tinha `477.994` registros e `33` colunas;
- a visualizacao das primeiras linhas mostrou que os dados ja estavam codificados numericamente;
- tambem foi possivel perceber valores ausentes e codigos como `9`, mostrando que a base precisava de limpeza;
- foram escolhidas as colunas mais importantes;
- foram mantidos apenas registros de mulheres;
- foram analisados nulos e inconsistencias;
- codigos como `9` e `99` foram tratados como valores ausentes;
- registros com alvo invalido foram removidos.

Neste projeto, os scripts continuam organizados em etapas separadas, com geracao de bases intermediarias em `data/processed`.

No entanto, o notebook principal de modelagem foi adaptado para permitir execucao completa desde a base bruta, usando diretamente:

- `data/raw/VIOLBR25.xlsx`
- ou `data/raw/VIOLBR25_ptbr.csv`

Assim, no notebook, todo o fluxo pode ser reproduzido sem depender manualmente dos arquivos intermediarios.

Depois do tratamento inicial, a base ficou com `368.801` registros.

Depois disso, a variavel `OUT_VEZES` ficou apenas com duas classes validas:

- `202.170` registros com reincidencia
- `166.631` registros sem reincidencia

Na limpeza fina, a coluna `NU_IDADE_N` foi removida porque ficou com muitos valores ausentes. Com isso, a base final ficou com `32` colunas.

## 3. Divisao Treino e Teste

Depois da limpeza, a base foi dividida em:

- `80%` para treino
- `20%` para teste

O conjunto de treino ficou com:

- `295.040` registros
- `31` variaveis preditoras

O conjunto de teste ficou com:

- `73.761` registros
- `31` variaveis preditoras

A proporcao entre as classes foi mantida nos dois conjuntos, o que deixou a avaliacao mais justa.

## 4. Preparacao para o Modelo

Antes de treinar o modelo, ainda existiam muitos valores ausentes nas variaveis preditoras.

Por isso, foi feita uma imputacao simples:

- mediana para `NU_IDADE_N`
- moda para as outras colunas

Depois disso:

- `X_train_modelo` ficou com `0` nulos
- `X_test_modelo` ficou com `0` nulos

## 5. Modelo Utilizado

O primeiro modelo escolhido foi a **Arvore de Decisao**, porque e mais facil de entender e interpretar.

O modelo foi treinado com:

- `max_depth = 5`
- `random_state = 42`

## 6. Resultados

As metricas principais foram:

- `accuracy = 0,6453`
- `recall = 0,8771`
- `f1-score = 0,7305`

Esses resultados mostram que o modelo teve desempenho relevante, principalmente na identificacao de casos reais de reincidencia.

O destaque foi o `recall`, indicando que a Arvore de Decisao conseguiu recuperar grande parte dos casos positivos da base de teste.

## 7. Matriz de Confusao

A matriz de confusao mostrou:

- `10.521` verdadeiros negativos
- `35.479` verdadeiros positivos
- `22.806` falsos positivos
- `4.955` falsos negativos

O principal ponto positivo foi a reducao dos falsos negativos, o que e importante neste problema porque significa perder menos casos reais de reincidencia.

## 8. Variaveis Mais Importantes

As variaveis que mais influenciaram o modelo foram:

- `LOCAL_OCOR`
- `VIOL_PSICO`
- `DEF_TRANS`
- `REL_CONJ`
- `CS_ESCOL_N`

Isso mostra que o modelo se apoiou principalmente no contexto da ocorrencia, no tipo de violencia e em fatores de vulnerabilidade.

## 9. Conclusao

Foi possivel montar e testar um modelo para prever reincidencia da violencia contra a mulher.

O modelo encontrou padroes importantes e mostrou desempenho especialmente forte no `recall`, que e a metrica mais sensivel para este tipo de problema.

Por isso, ele pode ser visto como uma ferramenta de apoio para triagem e analise inicial, mas nao deve substituir a avaliacao humana.

## 10. Regressao Logistica

Tambem foi iniciada a **Regressao Logistica** como segundo modelo de classificacao.

O resultado do treinamento mostrou que:

- o modelo foi ajustado com sucesso;
- ele trabalhou com `31` variaveis preditoras;
- as classes usadas foram `0` e `1`;
- a classe `1` representa reincidencia;
- a classe `0` representa nao reincidencia.

Esse resultado inicial confirma que o modelo conseguiu aprender com a base.

Em um teste simples com as primeiras previsoes, foi possivel ver que o modelo acertou alguns casos e errou outros, o que ja mostra que ele consegue classificar a reincidencia, mas ainda precisa ser avaliado com metricas mais completas.

As metricas principais da regressao logistica foram:

- `accuracy = 0,6588`
- `recall = 0,7477`
- `f1-score = 0,7061`

Esses resultados mostram um modelo equilibrado, com `accuracy` ligeiramente maior, mas com `recall` inferior ao da Arvore de Decisao.

No relatorio de classificacao, foi possivel observar que:

- para a classe `1` (reincidencia), o modelo teve `precision = 0,6689`, `recall = 0,7477` e `f1-score = 0,7061`;
- para a classe `0` (nao reincidencia), o modelo teve `precision = 0,6429`, `recall = 0,5511` e `f1-score = 0,5934`.

Isso mostra que a regressao logistica teve melhor desempenho para encontrar casos de reincidencia do que para identificar casos sem reincidencia.

A matriz de confusao da regressao logistica mostrou, de forma aproximada:

- `18.366` verdadeiros negativos;
- `14.961` falsos positivos;
- `10.201` falsos negativos;
- `30.233` verdadeiros positivos.

Isso mostra que a regressao logistica conseguiu identificar muitos casos reais de reincidencia, mas ainda perdeu mais casos positivos do que a Arvore de Decisao.

Nos coeficientes da regressao logistica, as variaveis com maior peso foram:

- `REL_EXCON`
- `REL_CONJ`
- `VIOL_FINAN`
- `REL_NAMO`
- `AG_FOGO`

Isso mostra que o modelo deu bastante importancia ao tipo de relacao com o agressor e a algumas formas de violencia registradas na ocorrencia.

Os coeficientes negativos e positivos indicam direcoes diferentes na previsao, mas o mais importante neste trabalho e observar quais variaveis tiveram maior influencia no resultado final.

O grafico das 10 variaveis mais relevantes ajudou a visualizar melhor esse resultado, mostrando de forma mais clara que `REL_EXCON`, `REL_CONJ` e `VIOL_FINAN` ficaram entre os fatores mais fortes da regressao logistica.

Na comparacao final entre os dois modelos, os resultados foram:

- **Arvore de Decisao**: `accuracy = 0,6453`, `recall = 0,8771`, `f1-score = 0,7305`
- **Regressao Logistica**: `accuracy = 0,6588`, `recall = 0,7477`, `f1-score = 0,7061`

Com isso, a Regressao Logistica apresentou `accuracy` um pouco maior, mas a Arvore de Decisao teve melhor `recall` e melhor `f1-score`, o que pesa mais no contexto do problema.

## 11. Escolha do Modelo Final

Com base nos resultados atualizados, a **Arvore de Decisao** foi escolhida como melhor modelo desta etapa.

Essa escolha foi feita porque, embora a Regressao Logistica tenha apresentado `accuracy` ligeiramente maior, a Arvore de Decisao teve `recall` superior e tambem melhor `f1-score`.

Como o objetivo principal e reduzir a perda de casos reais de reincidencia, a Arvore de Decisao se mostrou mais adequada neste momento.

## 12. Metrica Mais Importante

Neste problema, a metrica mais importante e o **recall**.

Isso acontece porque o objetivo nao e apenas acertar no geral, mas principalmente identificar o maior numero possivel de casos reais de reincidencia.

Se o modelo deixa de identificar um caso verdadeiro, isso pode significar a falta de um alerta importante.

## 13. Explicabilidade

A explicabilidade ajuda a entender por que o modelo chegou a determinado resultado.

Neste trabalho, isso foi feito de forma complementar:

- na arvore de decisao, pelas variaveis mais importantes e pela propria estrutura da arvore;
- na regressao logistica, pelos coeficientes das variaveis;
- nos dois modelos, por meio de analise SHAP, observando o impacto das variaveis nas previsoes.

Isso permitiu observar que fatores ligados ao relacionamento com o agressor, ao contexto da ocorrencia e aos tipos de violencia tiveram bastante peso nas previsoes.

## 14. Discussao Critica

Apesar dos resultados serem uteis, o modelo ainda tem limitacoes.

Ele pode ajudar a sinalizar casos com maior chance de reincidencia, mas ainda comete erros e nao deve ser usado sozinho para tomar decisoes.

Por isso, seu uso mais adequado seria como ferramenta de apoio para triagem inicial, ajudando assistentes sociais, equipes de saude ou seguranca publica a olhar com mais atencao para casos de maior risco.

Na pratica, o modelo pode funcionar como um sistema de alerta para priorizacao de acompanhamento, mas a interpretacao do caso concreto deve continuar dependendo de analise profissional.

Em contexto de saude, o medico e a equipe responsavel devem sempre ter a palavra final no diagnostico, no encaminhamento e na conduta.

## 15. Fechamento

De forma geral, o trabalho mostrou que e possivel usar tecnicas de classificacao para analisar padroes de reincidencia da violencia contra a mulher.

Entre os modelos testados, a Arvore de Decisao apresentou o melhor desempenho para o criterio mais importante deste problema, que foi o `recall`.

Mesmo assim, a decisao final sobre qualquer atendimento, intervencao ou encaminhamento deve continuar sendo humana.
